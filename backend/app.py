"""
Flask Application for CFG-Based HTTP GET Request Validator

This is the main Flask application that provides REST API endpoints
for validating HTTP requests, managing analytics, and serving the frontend.
"""

from flask import Flask, request, jsonify, session
from flask_cors import CORS
from werkzeug.exceptions import BadRequest
import os
import uuid
from datetime import datetime, timedelta
import json

from cfg_parser import HTTPRequestCFGParser
from models import db, RequestLog, ErrorPattern, UserSession, init_db, get_analytics_summary

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your-secret-key-here')
app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get('DATABASE_URL', 'sqlite:///cfg_validator.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = False

# Enable CORS for frontend communication
CORS(app, supports_credentials=True)

# Initialize extensions
init_db(app)

# Initialize the CFG parser
cfg_parser = HTTPRequestCFGParser()

def get_session_id():
    """Get or create a session ID for the current user."""
    if 'session_id' not in session:
        session['session_id'] = str(uuid.uuid4())
    return session['session_id']

def get_or_create_user_session():
    """Get or create a user session record."""
    session_id = get_session_id()
    user_session = UserSession.query.filter_by(session_id=session_id).first()
    
    if not user_session:
        user_session = UserSession(
            session_id=session_id,
            ip_address=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')[:500]
        )
        db.session.add(user_session)
        db.session.commit()
    
    return user_session

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat(),
        'version': '1.0.0'
    })

@app.route('/api/validate', methods=['POST'])
def validate_request():
    """
    Validate an HTTP GET request line using CFG parser.
    
    Expected JSON payload:
    {
        "request_line": "GET /index.html HTTP/1.1"
    }
    """
    try:
        data = request.get_json()
        if not data or 'request_line' not in data:
            return jsonify({'error': 'Missing request_line in payload'}), 400
        
        request_line = data['request_line'].strip()
        if not request_line:
            return jsonify({'error': 'Empty request_line'}), 400
        
        # Validate the request using CFG parser
        validation_result = cfg_parser.validate_request(request_line)
        
        # Log the request to database
        try:
            request_log = RequestLog(
                request_line=request_line,
                is_valid=validation_result['is_valid'],
                tokens=validation_result['tokens'],
                parse_trees=validation_result['parse_trees'],
                errors=validation_result['errors'],
                ip_address=request.remote_addr,
                user_agent=request.headers.get('User-Agent', '')[:500],
                session_id=get_session_id()
            )
            db.session.add(request_log)
            
            # Update user session
            user_session = get_or_create_user_session()
            user_session.update_activity(validation_result['is_valid'])
            
            # Update error pattern counts
            if not validation_result['is_valid']:
                for error_msg in validation_result['errors']:
                    error_pattern = ErrorPattern.query.filter_by(error_message=error_msg).first()
                    if error_pattern:
                        error_pattern.occurrence_count += 1
                    else:
                        # Create new error pattern (basic entry)
                        error_pattern = ErrorPattern(
                            error_message=error_msg,
                            description=f"Error: {error_msg}"
                        )
                        db.session.add(error_pattern)
            
            db.session.commit()
            
        except Exception as e:
            db.session.rollback()
            print(f"Database error: {e}")
        
        return jsonify(validation_result)
        
    except Exception as e:
        return jsonify({'error': f'Validation error: {str(e)}'}), 500

@app.route('/api/grammar', methods=['GET'])
def get_grammar():
    """Get the CFG grammar rules and information."""
    try:
        grammar_info = {
            'rules': cfg_parser.get_grammar_rules(),
            'description': 'Context-Free Grammar for HTTP GET Request Validation with Nested Path Support',
            'terminals': {
                'HTTP_METHODS': ['GET'],
                'PATH_STRUCTURE': 'Nested paths supported (e.g., /assets/images/logo.png)',
                'FILE_EXTENSIONS': 'Any valid file extension (e.g., .html, .css, .js, .png, .json)',
                'HTTP_VERSIONS': ['HTTP/1.0', 'HTTP/1.1', 'HTTP/2.0'],
                'SYMBOLS': ['/', ' ']
            },
            'production_rules': [
                'RequestLine → GET SP RequestTarget SP HTTPVersion',
                'RequestTarget → "/" PathSegments | "/"',
                'PathSegments → PathSegment "/" PathSegments | PathSegment',
                'PathSegment → ValidChars (filename or directory with extension)',
                'HTTPVersion → "HTTP/1.0" | "HTTP/1.1" | "HTTP/2.0"',
                'SP → " "',
                'GET → "GET"'
            ],
            'examples': {
                'valid': [
                    'GET / HTTP/1.1',
                    'GET /index.html HTTP/1.1',
                    'GET /assets/style.css HTTP/1.0',
                    'GET /images/icons/logo.png HTTP/2.0',
                    'GET /api/v1/users.json HTTP/1.1'
                ],
                'invalid': [
                    'GET index.html HTTP/1.1  # Missing leading slash',
                    'GET /assets/ HTTP/1.1     # Missing filename',
                    'GET /index HTTP/1.1       # Missing file extension',
                    'POST /index.html HTTP/1.1 # Wrong HTTP method'
                ]
            }
        }
        return jsonify(grammar_info)
    except Exception as e:
        return jsonify({'error': f'Grammar error: {str(e)}'}), 500

@app.route('/api/examples', methods=['GET'])
def get_examples():
    """Get example HTTP requests for testing."""
    try:
        examples = cfg_parser.get_example_requests()
        return jsonify({'examples': examples})
    except Exception as e:
        return jsonify({'error': f'Examples error: {str(e)}'}), 500

@app.route('/api/analytics', methods=['GET'])
def get_analytics():
    """Get analytics data for the dashboard."""
    try:
        days = request.args.get('days', 7, type=int)
        if days < 1 or days > 365:
            days = 7
        
        analytics = get_analytics_summary(days)
        return jsonify(analytics)
    except Exception as e:
        return jsonify({'error': f'Analytics error: {str(e)}'}), 500

@app.route('/api/analytics/detailed', methods=['GET'])
def get_detailed_analytics():
    """Get detailed analytics including request logs."""
    try:
        days = request.args.get('days', 7, type=int)
        limit = request.args.get('limit', 100, type=int)
        
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        # Get recent logs
        logs = RequestLog.query.filter(
            RequestLog.timestamp >= cutoff_date
        ).order_by(RequestLog.timestamp.desc()).limit(limit).all()
        
        # Get analytics summary
        analytics = get_analytics_summary(days)
        
        return jsonify({
            'analytics': analytics,
            'recent_logs': [log.to_dict() for log in logs],
            'total_logs': len(logs)
        })
    except Exception as e:
        return jsonify({'error': f'Detailed analytics error: {str(e)}'}), 500

@app.route('/api/errors', methods=['GET'])
def get_error_patterns():
    """Get error patterns and their explanations."""
    try:
        patterns = ErrorPattern.query.order_by(ErrorPattern.occurrence_count.desc()).all()
        return jsonify({
            'error_patterns': [pattern.to_dict() for pattern in patterns]
        })
    except Exception as e:
        return jsonify({'error': f'Error patterns error: {str(e)}'}), 500

@app.route('/api/errors/<int:error_id>', methods=['GET'])
def get_error_pattern(error_id):
    """Get a specific error pattern by ID."""
    try:
        pattern = ErrorPattern.query.get_or_404(error_id)
        return jsonify(pattern.to_dict())
    except Exception as e:
        return jsonify({'error': f'Error pattern error: {str(e)}'}), 500

@app.route('/api/session', methods=['GET'])
def get_session_info():
    """Get current session information."""
    try:
        user_session = get_or_create_user_session()
        return jsonify(user_session.to_dict())
    except Exception as e:
        return jsonify({'error': f'Session error: {str(e)}'}), 500

@app.route('/api/stats/summary', methods=['GET'])
def get_stats_summary():
    """Get quick statistics summary."""
    try:
        total_requests = RequestLog.query.count()
        valid_requests = RequestLog.query.filter_by(is_valid=True).count()
        total_sessions = UserSession.query.count()
        
        # Recent activity (last 24 hours)
        recent_cutoff = datetime.utcnow() - timedelta(hours=24)
        recent_requests = RequestLog.query.filter(RequestLog.timestamp >= recent_cutoff).count()
        
        return jsonify({
            'total_requests': total_requests,
            'valid_requests': valid_requests,
            'invalid_requests': total_requests - valid_requests,
            'success_rate': (valid_requests / total_requests * 100) if total_requests > 0 else 0,
            'total_sessions': total_sessions,
            'recent_requests_24h': recent_requests
        })
    except Exception as e:
        return jsonify({'error': f'Stats error: {str(e)}'}), 500

@app.route('/api/validate/batch', methods=['POST'])
def validate_batch():
    """
    Validate multiple HTTP request lines at once.
    
    Expected JSON payload:
    {
        "requests": ["GET / HTTP/1.1", "GET /index.html HTTP/1.1", ...]
    }
    """
    try:
        data = request.get_json()
        if not data or 'requests' not in data:
            return jsonify({'error': 'Missing requests array in payload'}), 400
        
        requests_list = data['requests']
        if not isinstance(requests_list, list):
            return jsonify({'error': 'Requests must be an array'}), 400
        
        if len(requests_list) > 50:  # Limit batch size
            return jsonify({'error': 'Maximum 50 requests per batch'}), 400
        
        results = []
        for req_line in requests_list:
            if isinstance(req_line, str) and req_line.strip():
                validation_result = cfg_parser.validate_request(req_line.strip())
                results.append(validation_result)
                
                # Log to database (simplified for batch)
                try:
                    request_log = RequestLog(
                        request_line=req_line.strip(),
                        is_valid=validation_result['is_valid'],
                        tokens=validation_result['tokens'],
                        parse_trees=validation_result['parse_trees'],
                        errors=validation_result['errors'],
                        ip_address=request.remote_addr,
                        user_agent=request.headers.get('User-Agent', '')[:500],
                        session_id=get_session_id()
                    )
                    db.session.add(request_log)
                except Exception as e:
                    print(f"Error logging batch request: {e}")
        
        try:
            db.session.commit()
        except Exception as e:
            db.session.rollback()
            print(f"Error committing batch: {e}")
        
        return jsonify({
            'results': results,
            'total_processed': len(results)
        })
        
    except Exception as e:
        return jsonify({'error': f'Batch validation error: {str(e)}'}), 500

@app.route('/api/ai/help', methods=['POST'])
def ai_help():
    """
    Provide AI assistance for CFG rules and HTTP syntax.
    This is a mock endpoint - in a real implementation, this would integrate with an AI service.
    """
    try:
        data = request.get_json()
        if not data or 'question' not in data:
            return jsonify({'error': 'Missing question in payload'}), 400
        
        question = data['question'].lower().strip()
        
        # Simple rule-based responses (mock AI)
        responses = {
            'cfg': "CFG (Context-Free Grammar) is a formal grammar where each production rule has a single non-terminal on the left side. In our HTTP validator, we use CFG to define the structure of valid HTTP GET requests.",
            'http': "HTTP (HyperText Transfer Protocol) is the foundation of data communication on the web. A GET request retrieves data from a server using the format: GET /path HTTP/version",
            'grammar': "Our grammar defines: RequestLine → GET SP RequestTarget SP HTTPVersion, where SP is a space, RequestTarget can be '/' or '/filename', and HTTPVersion is HTTP/1.0, HTTP/1.1, or HTTP/2.0",
            'error': "Common errors include: missing spaces, invalid HTTP methods (only GET is supported), invalid filenames (only index.html, about.html, contact.html, style.css are allowed), and invalid HTTP versions.",
            'example': "Valid examples: 'GET / HTTP/1.1', 'GET /index.html HTTP/2.0'. Invalid examples: 'POST /index.html HTTP/1.1', 'GET index.html HTTP/1.1'"
        }
        
        response = "I'm here to help with CFG rules and HTTP syntax! You can ask about CFG concepts, HTTP request structure, grammar rules, common errors, or request examples."
        
        for keyword, answer in responses.items():
            if keyword in question:
                response = answer
                break
        
        return jsonify({
            'question': data['question'],
            'answer': response,
            'helpful_links': [
                {'title': 'CFG Grammar Rules', 'url': '/grammar'},
                {'title': 'Request Examples', 'url': '/examples'},
                {'title': 'Error Patterns', 'url': '/errors'}
            ]
        })
        
    except Exception as e:
        return jsonify({'error': f'AI help error: {str(e)}'}), 500

@app.errorhandler(404)
def not_found(error):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404

@app.errorhandler(500)
def internal_error(error):
    """Handle 500 errors."""
    db.session.rollback()
    return jsonify({'error': 'Internal server error'}), 500

if __name__ == '__main__':
    # Development server
    port = int(os.environ.get('PORT', 5000))
    debug = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    
    print(f"Starting CFG Validator API server on port {port}")
    print(f"Debug mode: {debug}")
    
    app.run(host='0.0.0.0', port=port, debug=debug)