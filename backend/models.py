"""
Database models for the CFG-Based HTTP GET Request Validator

This module defines the SQLAlchemy models for storing request logs,
analytics data, and user interactions.
"""

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json
from typing import Dict, Any, List, Optional

db = SQLAlchemy()

class RequestLog(db.Model):
    """
    Model for storing HTTP request validation logs.
    """
    __tablename__ = 'request_logs'
    
    id = db.Column(db.Integer, primary_key=True)
    request_line = db.Column(db.Text, nullable=False)
    is_valid = db.Column(db.Boolean, nullable=False)
    tokens = db.Column(db.Text)  # JSON string of tokens
    parse_trees = db.Column(db.Text)  # JSON string of parse trees
    errors = db.Column(db.Text)  # JSON string of error messages
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    ip_address = db.Column(db.String(45))  # IPv6 compatible
    user_agent = db.Column(db.String(500))
    session_id = db.Column(db.String(100))
    
    def __init__(self, request_line: str, is_valid: bool, tokens: List[str] = None,
                 parse_trees: List[Dict] = None, errors: List[str] = None,
                 ip_address: str = None, user_agent: str = None, session_id: str = None):
        self.request_line = request_line
        self.is_valid = is_valid
        self.tokens = json.dumps(tokens) if tokens else None
        self.parse_trees = json.dumps(parse_trees) if parse_trees else None
        self.errors = json.dumps(errors) if errors else None
        self.ip_address = ip_address
        self.user_agent = user_agent
        self.session_id = session_id
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'request_line': self.request_line,
            'is_valid': self.is_valid,
            'tokens': json.loads(self.tokens) if self.tokens else [],
            'parse_trees': json.loads(self.parse_trees) if self.parse_trees else [],
            'errors': json.loads(self.errors) if self.errors else [],
            'timestamp': self.timestamp.isoformat() if self.timestamp else None,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'session_id': self.session_id
        }
    
    @staticmethod
    def get_validation_stats(days: int = 7) -> Dict[str, Any]:
        """
        Get validation statistics for the last N days.
        
        Args:
            days (int): Number of days to look back
            
        Returns:
            Dict[str, Any]: Statistics dictionary
        """
        from datetime import timedelta
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        logs = RequestLog.query.filter(RequestLog.timestamp >= cutoff_date).all()
        
        total_requests = len(logs)
        valid_requests = sum(1 for log in logs if log.is_valid)
        invalid_requests = total_requests - valid_requests
        
        # Error analysis
        error_counts = {}
        for log in logs:
            if not log.is_valid and log.errors:
                errors = json.loads(log.errors)
                for error in errors:
                    error_counts[error] = error_counts.get(error, 0) + 1
        
        # Daily breakdown
        daily_stats = {}
        for log in logs:
            date_str = log.timestamp.strftime('%Y-%m-%d')
            if date_str not in daily_stats:
                daily_stats[date_str] = {'valid': 0, 'invalid': 0, 'total': 0}
            
            daily_stats[date_str]['total'] += 1
            if log.is_valid:
                daily_stats[date_str]['valid'] += 1
            else:
                daily_stats[date_str]['invalid'] += 1
        
        return {
            'total_requests': total_requests,
            'valid_requests': valid_requests,
            'invalid_requests': invalid_requests,
            'success_rate': (valid_requests / total_requests * 100) if total_requests > 0 else 0,
            'error_counts': error_counts,
            'daily_stats': daily_stats,
            'period_days': days
        }

class ErrorPattern(db.Model):
    """
    Model for tracking common error patterns and their explanations.
    """
    __tablename__ = 'error_patterns'
    
    id = db.Column(db.Integer, primary_key=True)
    error_message = db.Column(db.String(500), nullable=False, unique=True)
    description = db.Column(db.Text)
    solution = db.Column(db.Text)
    example_correct = db.Column(db.String(200))
    example_incorrect = db.Column(db.String(200))
    occurrence_count = db.Column(db.Integer, default=1)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def __init__(self, error_message: str, description: str = None, solution: str = None,
                 example_correct: str = None, example_incorrect: str = None):
        self.error_message = error_message
        self.description = description
        self.solution = solution
        self.example_correct = example_correct
        self.example_incorrect = example_incorrect
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'error_message': self.error_message,
            'description': self.description,
            'solution': self.solution,
            'example_correct': self.example_correct,
            'example_incorrect': self.example_incorrect,
            'occurrence_count': self.occurrence_count,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None
        }

class UserSession(db.Model):
    """
    Model for tracking user sessions and interactions.
    """
    __tablename__ = 'user_sessions'
    
    id = db.Column(db.Integer, primary_key=True)
    session_id = db.Column(db.String(100), nullable=False, unique=True)
    ip_address = db.Column(db.String(45))
    user_agent = db.Column(db.String(500))
    first_request = db.Column(db.DateTime, default=datetime.utcnow)
    last_request = db.Column(db.DateTime, default=datetime.utcnow)
    request_count = db.Column(db.Integer, default=0)
    valid_request_count = db.Column(db.Integer, default=0)
    invalid_request_count = db.Column(db.Integer, default=0)
    
    def __init__(self, session_id: str, ip_address: str = None, user_agent: str = None):
        self.session_id = session_id
        self.ip_address = ip_address
        self.user_agent = user_agent
    
    def update_activity(self, is_valid: bool):
        """Update session activity with a new request."""
        self.last_request = datetime.utcnow()
        self.request_count += 1
        if is_valid:
            self.valid_request_count += 1
        else:
            self.invalid_request_count += 1
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert the model to a dictionary for JSON serialization."""
        return {
            'id': self.id,
            'session_id': self.session_id,
            'ip_address': self.ip_address,
            'user_agent': self.user_agent,
            'first_request': self.first_request.isoformat() if self.first_request else None,
            'last_request': self.last_request.isoformat() if self.last_request else None,
            'request_count': self.request_count,
            'valid_request_count': self.valid_request_count,
            'invalid_request_count': self.invalid_request_count,
            'success_rate': (self.valid_request_count / self.request_count * 100) if self.request_count > 0 else 0
        }

def init_db(app):
    """
    Initialize the database with the Flask app.
    
    Args:
        app: Flask application instance
    """
    db.init_app(app)
    
    with app.app_context():
        # Create all tables
        db.create_all()
        
        # Populate default error patterns
        populate_default_error_patterns()

def populate_default_error_patterns():
    """Populate the database with default error patterns and explanations."""
    default_patterns = [
        {
            'error_message': 'Invalid HTTP method',
            'description': 'The request line must start with the GET method. Other HTTP methods like POST, PUT, DELETE are not supported by this validator.',
            'solution': 'Ensure your request line starts with "GET" followed by a space.',
            'example_correct': 'GET /index.html HTTP/1.1',
            'example_incorrect': 'POST /index.html HTTP/1.1'
        },
        {
            'error_message': 'Invalid request target',
            'description': 'The request target must start with a forward slash (/) and can be a root path "/" or a nested path like "/assets/style.css".',
            'solution': 'Use "/" for root requests or a valid nested path starting with "/" and ending with a filename that has an extension.',
            'example_correct': 'GET /assets/images/logo.png HTTP/1.1',
            'example_incorrect': 'GET assets/style.css HTTP/1.1'
        },
        {
            'error_message': 'Must start with',
            'description': 'The request target must begin with a forward slash ("/") to indicate it\'s an absolute path.',
            'solution': 'Add a forward slash at the beginning of your request target.',
            'example_correct': 'GET /images/logo.png HTTP/1.1',
            'example_incorrect': 'GET images/logo.png HTTP/1.1'
        },
        {
            'error_message': 'Must end with a filename',
            'description': 'The request target cannot end with a directory path. It must specify a file with an extension.',
            'solution': 'Include a filename with extension at the end of your path.',
            'example_correct': 'GET /assets/style.css HTTP/1.1',
            'example_incorrect': 'GET /assets/ HTTP/1.1'
        },
        {
            'error_message': 'Must end with a valid file extension',
            'description': 'The request target must end with a filename that includes a valid file extension (e.g., .html, .css, .js, .png).',
            'solution': 'Add a valid file extension to your filename.',
            'example_correct': 'GET /documents/readme.txt HTTP/1.1',
            'example_incorrect': 'GET /documents/readme HTTP/1.1'
        },
        {
            'error_message': 'Invalid HTTP version',
            'description': 'Only specific HTTP versions are supported according to the CFG rules.',
            'solution': 'Use one of the supported HTTP versions: HTTP/1.0, HTTP/1.1, or HTTP/2.0',
            'example_correct': 'GET /index.html HTTP/2.0',
            'example_incorrect': 'GET /index.html HTTP/3.0'
        },
        {
            'error_message': 'Missing space',
            'description': 'HTTP request components must be separated by exactly one space character.',
            'solution': 'Ensure there is exactly one space between GET and the request target, and between the request target and HTTP version.',
            'example_correct': 'GET /index.html HTTP/1.1',
            'example_incorrect': 'GET/index.html HTTP/1.1'
        },
        {
            'error_message': 'Incomplete request line',
            'description': 'The HTTP request line is missing required components. A complete request line must have three parts: method, target, and version.',
            'solution': 'Include all three components: GET, request target, and HTTP version, separated by spaces.',
            'example_correct': 'GET /assets/app.js HTTP/1.1',
            'example_incorrect': 'GET /assets/app.js'
        }
    ]
    
    for pattern_data in default_patterns:
        existing = ErrorPattern.query.filter_by(error_message=pattern_data['error_message']).first()
        if not existing:
            pattern = ErrorPattern(**pattern_data)
            db.session.add(pattern)
    
    try:
        db.session.commit()
    except Exception as e:
        db.session.rollback()
        print(f"Error populating default patterns: {e}")

def get_analytics_summary(days: int = 30) -> Dict[str, Any]:
    """
    Get a comprehensive analytics summary.
    
    Args:
        days (int): Number of days to analyze
        
    Returns:
        Dict[str, Any]: Analytics summary
    """
    stats = RequestLog.get_validation_stats(days)
    
    # Get top error patterns
    from datetime import timedelta
    cutoff_date = datetime.utcnow() - timedelta(days=days)
    recent_logs = RequestLog.query.filter(RequestLog.timestamp >= cutoff_date).all()
    
    # Get session statistics
    session_count = UserSession.query.filter(UserSession.last_request >= cutoff_date).count()
    avg_requests_per_session = stats['total_requests'] / session_count if session_count > 0 else 0
    
    return {
        **stats,
        'unique_sessions': session_count,
        'avg_requests_per_session': round(avg_requests_per_session, 2),
        'most_common_errors': sorted(stats['error_counts'].items(), key=lambda x: x[1], reverse=True)[:5]
    }