"""
Scalable API Architecture for Advanced NLP Modules

This module provides a comprehensive REST API for all the advanced NLP features
including summarization, query handling, and document classification.
"""

from flask import Flask, request, jsonify, g
from flask_cors import CORS
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge
import os
import json
import time
import uuid
from datetime import datetime, timedelta
from typing import Dict, List, Any, Optional
import threading
from concurrent.futures import ThreadPoolExecutor
import traceback
from collections import defaultdict

# Import our new NLP modules
from advanced_summarization import AdvancedTextSummarizer, SummarizationMethod, SummarizationType
from intelligent_query_handler import IntelligentQueryHandler
from document_classifier import DocumentClassifier, ClassificationMethod

app = Flask(__name__)

# Configuration
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'advanced-nlp-secret-key')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024  # 16MB max request size

# Enable CORS with specific settings
CORS(app, 
     origins=['http://localhost:3000', 'http://127.0.0.1:3000'],
     supports_credentials=True,
     allow_headers=['Content-Type', 'Authorization', 'X-Requested-With'],
     methods=['GET', 'POST', 'PUT', 'DELETE', 'OPTIONS'])

# Simple rate limiting using memory store
rate_limit_store = defaultdict(list)

def check_rate_limit(key: str, limit: int, window: int = 60) -> bool:
    """Simple rate limiting implementation."""
    now = time.time()
    # Clean old entries
    rate_limit_store[key] = [t for t in rate_limit_store[key] if now - t < window]
    
    if len(rate_limit_store[key]) >= limit:
        return False
    
    rate_limit_store[key].append(now)
    return True

def rate_limit(limit_per_minute: int = 10):
    """Decorator for rate limiting."""
    def decorator(f):
        def wrapper(*args, **kwargs):
            client_ip = request.remote_addr or 'unknown'
            key = f"{f.__name__}:{client_ip}"
            
            if not check_rate_limit(key, limit_per_minute, 60):
                return jsonify({
                    'error': 'Rate limit exceeded',
                    'status_code': 429,
                    'retry_after': 60
                }), 429
            
            return f(*args, **kwargs)
        wrapper.__name__ = f.__name__
        return wrapper
    return decorator

# Initialize NLP modules
text_summarizer = AdvancedTextSummarizer()
query_handler = IntelligentQueryHandler()
document_classifier = DocumentClassifier()

# Thread pool for async processing
executor = ThreadPoolExecutor(max_workers=4)

# Request tracking
active_requests = {}
request_stats = {
    'total_requests': 0,
    'successful_requests': 0,
    'failed_requests': 0,
    'avg_response_time': 0.0,
    'endpoints_usage': {},
    'start_time': datetime.now()
}

class APIError(Exception):
    """Custom API error class."""
    def __init__(self, message: str, status_code: int = 400, payload: Optional[Dict] = None):
        super().__init__()
        self.message = message
        self.status_code = status_code
        self.payload = payload

@app.before_request
def before_request():
    """Execute before each request."""
    g.start_time = time.time()
    g.request_id = str(uuid.uuid4())
    
    # Track request
    request_stats['total_requests'] += 1
    endpoint = request.endpoint or 'unknown'
    request_stats['endpoints_usage'][endpoint] = request_stats['endpoints_usage'].get(endpoint, 0) + 1
    
    # Add to active requests
    active_requests[g.request_id] = {
        'endpoint': endpoint,
        'start_time': g.start_time,
        'remote_addr': request.remote_addr
    }

@app.after_request
def after_request(response):
    """Execute after each request."""
    # Calculate response time
    response_time = time.time() - g.start_time
    
    # Update statistics
    if response.status_code < 400:
        request_stats['successful_requests'] += 1
    else:
        request_stats['failed_requests'] += 1
    
    # Update average response time
    total_requests = request_stats['total_requests']
    current_avg = request_stats['avg_response_time']
    request_stats['avg_response_time'] = (current_avg * (total_requests - 1) + response_time) / total_requests
    
    # Remove from active requests
    active_requests.pop(g.request_id, None)
    
    # Add response headers
    response.headers['X-Request-ID'] = g.request_id
    response.headers['X-Response-Time'] = f"{response_time:.3f}s"
    response.headers['X-API-Version'] = "2.0"
    
    return response

@app.errorhandler(APIError)
def handle_api_error(error):
    """Handle custom API errors."""
    response = {
        'error': error.message,
        'status_code': error.status_code,
        'request_id': getattr(g, 'request_id', 'unknown'),
        'timestamp': datetime.now().isoformat()
    }
    
    if error.payload:
        response.update(error.payload)
    
    return jsonify(response), error.status_code

@app.errorhandler(RequestEntityTooLarge)
def handle_large_request(error):
    """Handle requests that are too large."""
    return jsonify({
        'error': 'Request entity too large. Maximum size is 16MB.',
        'status_code': 413,
        'request_id': getattr(g, 'request_id', 'unknown')
    }), 413

@app.errorhandler(Exception)
def handle_general_error(error):
    """Handle general exceptions."""
    return jsonify({
        'error': 'Internal server error occurred',
        'status_code': 500,
        'request_id': getattr(g, 'request_id', 'unknown'),
        'timestamp': datetime.now().isoformat()
    }), 500

def validate_request_data(required_fields: List[str], data: Dict[str, Any]) -> None:
    """Validate request data contains required fields."""
    missing_fields = [field for field in required_fields if field not in data or not data[field]]
    
    if missing_fields:
        raise APIError(
            f"Missing required fields: {', '.join(missing_fields)}",
            status_code=400,
            payload={'missing_fields': missing_fields}
        )

def validate_text_input(text: str, max_length: int = 50000, min_length: int = 10) -> None:
    """Validate text input parameters."""
    if not isinstance(text, str):
        raise APIError("Text input must be a string", status_code=400)
    
    if len(text) < min_length:
        raise APIError(f"Text must be at least {min_length} characters long", status_code=400)
    
    if len(text) > max_length:
        raise APIError(f"Text exceeds maximum length of {max_length} characters", status_code=400)

# ===========================================
# SUMMARIZATION ENDPOINTS
# ===========================================

@app.route('/api/v2/summarization/summarize', methods=['POST'])
@rate_limit(10)
def summarize_text():
    """
    Summarize text using advanced algorithms.
    
    Expected JSON payload:
    {
        "text": "Text to summarize",
        "method": "tf_idf",  // Optional: frequency_based, tf_idf, textrank, lsa, luhn, edmundson
        "summary_type": "extractive",  // Optional: extractive, abstractive, hybrid
        "summary_length": 3,  // Optional: number of sentences
        "compression_ratio": 0.3  // Optional: alternative to summary_length
    }
    """
    try:
        data = request.get_json()
        validate_request_data(['text'], data)
        
        text = data['text']
        validate_text_input(text)
        
        # Parse optional parameters
        method_str = data.get('method', 'tf_idf')
        summary_type_str = data.get('summary_type', 'extractive')
        summary_length = data.get('summary_length', 3)
        compression_ratio = data.get('compression_ratio')
        
        try:
            method = SummarizationMethod(method_str)
            summary_type = SummarizationType(summary_type_str)
        except ValueError as e:
            raise APIError(f"Invalid parameter value: {str(e)}", status_code=400)
        
        # Perform summarization
        result = text_summarizer.summarize(
            text=text,
            method=method,
            summary_type=summary_type,
            summary_length=summary_length,
            compression_ratio=compression_ratio
        )
        
        # Convert result to JSON-serializable format
        response_data = {
            'summary': result.summary,
            'method': result.method.value,
            'summary_type': result.summary_type.value,
            'compression_ratio': result.compression_ratio,
            'statistics': result.statistics,
            'key_phrases': result.key_phrases,
            'processing_time': result.processing_time,
            'timestamp': result.timestamp,
            'sentence_count': len(result.sentence_scores),
            'original_length': len(result.original_text.split()),
            'summary_length': len(result.summary.split())
        }
        
        return jsonify(response_data)
        
    except APIError:
        raise
    except Exception as e:
        raise APIError(f"Summarization failed: {str(e)}", status_code=500)

@app.route('/api/v2/summarization/methods', methods=['GET'])
def get_summarization_methods():
    """Get available summarization methods and types."""
    return jsonify({
        'methods': [method.value for method in SummarizationMethod],
        'summary_types': [stype.value for stype in SummarizationType],
        'default_method': 'tf_idf',
        'default_summary_type': 'extractive',
        'max_text_length': 50000,
        'min_text_length': 10
    })

# ===========================================
# QUERY HANDLING ENDPOINTS
# ===========================================

@app.route('/api/v2/query/process', methods=['POST'])
@rate_limit(20)
def process_query():
    """
    Process an intelligent query with NLP analysis.
    
    Expected JSON payload:
    {
        "query": "What is a context-free grammar?",
        "context": {}  // Optional context information
    }
    """
    try:
        data = request.get_json()
        validate_request_data(['query'], data)
        
        query = data['query']
        context = data.get('context')
        
        validate_text_input(query, max_length=1000, min_length=3)
        
        # Process query
        result = query_handler.process_query(query, context)
        
        # Convert to JSON-serializable format
        response_data = {
            'query_analysis': {
                'original_query': result.query_analysis.original_query,
                'cleaned_query': result.query_analysis.cleaned_query,
                'query_type': result.query_analysis.query_type.value,
                'intent': {
                    'intent': result.query_analysis.intent.intent.value,
                    'confidence': result.query_analysis.intent.confidence,
                    'reasoning': result.query_analysis.intent.reasoning,
                    'parameters': result.query_analysis.intent.parameters
                },
                'entities': [
                    {
                        'text': entity.text,
                        'entity_type': entity.entity_type.value,
                        'confidence': entity.confidence,
                        'start_pos': entity.start_pos,
                        'end_pos': entity.end_pos
                    } for entity in result.query_analysis.entities
                ],
                'keywords': result.query_analysis.keywords,
                'sentiment': result.query_analysis.sentiment,
                'complexity_score': result.query_analysis.complexity_score,
                'language': result.query_analysis.language
            },
            'response_text': result.response_text,
            'confidence': result.confidence,
            'sources': result.sources,
            'suggestions': result.suggestions,
            'follow_up_questions': result.follow_up_questions,
            'processing_time': result.processing_time,
            'metadata': result.metadata
        }
        
        return jsonify(response_data)
        
    except APIError:
        raise
    except Exception as e:
        raise APIError(f"Query processing failed: {str(e)}", status_code=500)

@app.route('/api/v2/query/analyze', methods=['POST'])
@rate_limit(30)
def analyze_query():
    """Analyze query without generating response (faster analysis)."""
    try:
        data = request.get_json()
        validate_request_data(['query'], data)
        
        query = data['query']
        validate_text_input(query, max_length=1000, min_length=3)
        
        # Analyze query only
        analysis = query_handler.analyze_query(query)
        
        response_data = {
            'query_type': analysis.query_type.value,
            'intent': analysis.intent.intent.value,
            'intent_confidence': analysis.intent.confidence,
            'entities': [
                {
                    'text': entity.text,
                    'type': entity.entity_type.value,
                    'confidence': entity.confidence
                } for entity in analysis.entities
            ],
            'keywords': analysis.keywords,
            'sentiment': analysis.sentiment,
            'complexity_score': analysis.complexity_score,
            'processing_time': (datetime.now() - datetime.fromisoformat(analysis.timestamp.replace('Z', '+00:00'))).total_seconds()
        }
        
        return jsonify(response_data)
        
    except APIError:
        raise
    except Exception as e:
        raise APIError(f"Query analysis failed: {str(e)}", status_code=500)

# ===========================================
# DOCUMENT CLASSIFICATION ENDPOINTS
# ===========================================

@app.route('/api/v2/classification/classify', methods=['POST'])
@rate_limit(15)
def classify_document():
    """
    Classify a document into predefined categories.
    
    Expected JSON payload:
    {
        "text": "Document text to classify",
        "method": "rule_based"  // Optional: rule_based, naive_bayes, ensemble
    }
    """
    try:
        data = request.get_json()
        validate_request_data(['text'], data)
        
        text = data['text']
        validate_text_input(text)
        
        method_str = data.get('method', 'rule_based')
        
        try:
            method = ClassificationMethod(method_str)
        except ValueError:
            raise APIError(f"Invalid classification method: {method_str}", status_code=400)
        
        # Classify document
        result = document_classifier.classify(text, method)
        
        response_data = {
            'predicted_category': result.predicted_category.value,
            'confidence': result.confidence,
            'probability_distribution': {
                category.value: prob for category, prob in result.probability_distribution.items()
            },
            'method_used': result.method_used.value,
            'reasoning': result.reasoning,
            'processing_time': result.processing_time,
            'timestamp': result.timestamp
        }
        
        return jsonify(response_data)
        
    except APIError:
        raise
    except Exception as e:
        raise APIError(f"Document classification failed: {str(e)}", status_code=500)

@app.route('/api/v2/classification/categories', methods=['GET'])
def get_classification_categories():
    """Get available document categories and classification methods."""
    from document_classifier import DocumentCategory
    
    return jsonify({
        'categories': [category.value for category in DocumentCategory],
        'methods': [method.value for method in ClassificationMethod],
        'default_method': 'rule_based',
        'category_descriptions': {
            'technical_documentation': 'Technical specifications and documentation',
            'research_paper': 'Academic research papers and studies',
            'tutorial': 'Step-by-step tutorials and guides',
            'api_documentation': 'API reference and documentation',
            'specification': 'Technical specifications and standards',
            'user_guide': 'User manuals and guides',
            'faq': 'Frequently asked questions',
            'blog_post': 'Blog articles and posts'
        }
    })

# ===========================================
# BATCH PROCESSING ENDPOINTS
# ===========================================

@app.route('/api/v2/batch/process', methods=['POST'])
@rate_limit(5)
def batch_process():
    """
    Process multiple documents in batch.
    
    Expected JSON payload:
    {
        "documents": [
            {"id": "doc1", "text": "Document 1 text", "operations": ["summarize", "classify"]},
            {"id": "doc2", "text": "Document 2 text", "operations": ["classify"]}
        ],
        "options": {
            "summarization": {"method": "tf_idf", "summary_length": 2},
            "classification": {"method": "ensemble"}
        }
    }
    """
    try:
        data = request.get_json()
        validate_request_data(['documents'], data)
        
        documents = data['documents']
        options = data.get('options', {})
        
        if not isinstance(documents, list) or len(documents) == 0:
            raise APIError("Documents must be a non-empty array", status_code=400)
        
        if len(documents) > 10:
            raise APIError("Maximum 10 documents allowed per batch", status_code=400)
        
        results = []
        
        for doc in documents:
            if not isinstance(doc, dict) or 'text' not in doc or 'operations' not in doc:
                raise APIError("Each document must have 'text' and 'operations' fields", status_code=400)
            
            doc_id = doc.get('id', str(uuid.uuid4()))
            text = doc['text']
            operations = doc['operations']
            
            validate_text_input(text)
            
            doc_result = {'id': doc_id, 'results': {}}
            
            # Process each operation
            for operation in operations:
                try:
                    if operation == 'summarize':
                        sum_options = options.get('summarization', {})
                        method = SummarizationMethod(sum_options.get('method', 'tf_idf'))
                        summary_length = sum_options.get('summary_length', 3)
                        
                        result = text_summarizer.summarize(text, method=method, summary_length=summary_length)
                        doc_result['results']['summarization'] = {
                            'summary': result.summary,
                            'compression_ratio': result.compression_ratio,
                            'method': result.method.value
                        }
                    
                    elif operation == 'classify':
                        class_options = options.get('classification', {})
                        method = ClassificationMethod(class_options.get('method', 'rule_based'))
                        
                        result = document_classifier.classify(text, method)
                        doc_result['results']['classification'] = {
                            'category': result.predicted_category.value,
                            'confidence': result.confidence,
                            'method': result.method_used.value
                        }
                    
                    elif operation == 'query_analysis':
                        analysis = query_handler.analyze_query(text)
                        doc_result['results']['query_analysis'] = {
                            'query_type': analysis.query_type.value,
                            'intent': analysis.intent.intent.value,
                            'keywords': analysis.keywords[:5]
                        }
                    
                except Exception as e:
                    doc_result['results'][operation] = {'error': str(e)}
            
            results.append(doc_result)
        
        return jsonify({
            'batch_results': results,
            'total_documents': len(documents),
            'timestamp': datetime.now().isoformat()
        })
        
    except APIError:
        raise
    except Exception as e:
        raise APIError(f"Batch processing failed: {str(e)}", status_code=500)

# ===========================================
# SYSTEM ENDPOINTS
# ===========================================

@app.route('/api/v2/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'version': '2.0',
        'modules': {
            'summarization': 'active',
            'query_handling': 'active',
            'document_classification': 'active'
        },
        'uptime': str(datetime.now() - request_stats['start_time']),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/v2/stats', methods=['GET'])
def get_stats():
    """Get API usage statistics."""
    uptime = datetime.now() - request_stats['start_time']
    
    return jsonify({
        'statistics': {
            'uptime_seconds': uptime.total_seconds(),
            'total_requests': request_stats['total_requests'],
            'successful_requests': request_stats['successful_requests'],
            'failed_requests': request_stats['failed_requests'],
            'success_rate': request_stats['successful_requests'] / max(request_stats['total_requests'], 1) * 100,
            'average_response_time': request_stats['avg_response_time'],
            'active_requests': len(active_requests),
            'endpoints_usage': request_stats['endpoints_usage']
        },
        'limits': {
            'max_text_length': 50000,
            'max_batch_documents': 10,
            'rate_limits': {
                'summarization': '10 per minute',
                'query_processing': '20 per minute',
                'classification': '15 per minute',
                'batch_processing': '5 per minute'
            }
        },
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/v2/capabilities', methods=['GET'])
def get_capabilities():
    """Get detailed API capabilities."""
    return jsonify({
        'version': '2.0',
        'capabilities': {
            'text_summarization': {
                'methods': [method.value for method in SummarizationMethod],
                'summary_types': [stype.value for stype in SummarizationType],
                'features': ['extractive', 'abstractive', 'hybrid', 'key_phrases', 'statistics']
            },
            'query_processing': {
                'features': ['intent_detection', 'entity_extraction', 'sentiment_analysis', 'keyword_extraction'],
                'supported_languages': ['en'],
                'query_types': ['question', 'command', 'search', 'comparison', 'definition']
            },
            'document_classification': {
                'methods': [method.value for method in ClassificationMethod],
                'categories': ['technical_documentation', 'research_paper', 'tutorial', 'api_documentation', 'specification', 'user_guide', 'faq', 'blog_post'],
                'features': ['rule_based', 'naive_bayes', 'ensemble']
            },
            'batch_processing': {
                'max_documents': 10,
                'supported_operations': ['summarize', 'classify', 'query_analysis']
            }
        },
        'endpoints': {
            'summarization': ['/api/v2/summarization/summarize', '/api/v2/summarization/methods'],
            'query_handling': ['/api/v2/query/process', '/api/v2/query/analyze'],
            'classification': ['/api/v2/classification/classify', '/api/v2/classification/categories'],
            'batch': ['/api/v2/batch/process'],
            'system': ['/api/v2/health', '/api/v2/stats', '/api/v2/capabilities']
        }
    })

if __name__ == '__main__':
    print("🚀 Starting Advanced NLP API Server v2.0...")
    print("Available endpoints:")
    print("- Text Summarization: /api/v2/summarization/*")
    print("- Query Processing: /api/v2/query/*")
    print("- Document Classification: /api/v2/classification/*")
    print("- Batch Processing: /api/v2/batch/*")
    print("- System Info: /api/v2/health, /api/v2/stats, /api/v2/capabilities")
    
    app.run(debug=True, host='0.0.0.0', port=5001, threaded=True)