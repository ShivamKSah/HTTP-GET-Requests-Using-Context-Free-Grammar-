"""
OpenAPI/Swagger Documentation for CFG QODER API

This module provides comprehensive API documentation using OpenAPI 3.0 specification
with Flask-RESTX for automatic documentation generation.
"""

from flask import Flask, Blueprint
from flask_restx import Api, Resource, fields, Namespace
from flask_cors import CORS

# Create API documentation blueprint
api_bp = Blueprint('api_docs', __name__, url_prefix='/api/docs')
api = Api(
    api_bp,
    version='2.0',
    title='CFG QODER API',
    description='''
    ## CFG-Based HTTP Request Validator API
    
    A comprehensive API for validating HTTP requests using Context-Free Grammar (CFG) rules,
    formal language automata, and advanced natural language processing.
    
    ### Features
    - **HTTP Request Validation**: Real-time validation using CFG rules
    - **Formal Automata**: NFA, DFA, and regex pattern matching
    - **Natural Language Processing**: Text summarization, classification, and query processing
    - **Analytics & Monitoring**: Request tracking and performance metrics
    - **Educational Tools**: Interactive learning modules and visualizations
    
    ### Base URL
    - **Development**: `http://localhost:5000/api`
    - **Production**: Configure via environment variables
    
    ### Authentication
    Currently no authentication required. Sessions are tracked automatically.
    
    ### Rate Limiting
    - Default: 100 requests per hour per IP
    - Configurable per endpoint
    
    ### Response Format
    All responses follow a consistent JSON structure with appropriate HTTP status codes.
    ''',
    doc='/docs/',
    authorizations={
        'apikey': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'X-API-Key'
        }
    }
)

# Namespaces for API organization
validation_ns = Namespace('validation', description='HTTP Request Validation Operations')
grammar_ns = Namespace('grammar', description='Context-Free Grammar Operations')
analytics_ns = Namespace('analytics', description='Analytics and Statistics')
automata_ns = Namespace('automata', description='Formal Automata Operations')
nlp_ns = Namespace('nlp', description='Natural Language Processing')
system_ns = Namespace('system', description='System Health and Information')

api.add_namespace(validation_ns, path='/validation')
api.add_namespace(grammar_ns, path='/grammar')
api.add_namespace(analytics_ns, path='/analytics')
api.add_namespace(automata_ns, path='/automata')
api.add_namespace(nlp_ns, path='/nlp')
api.add_namespace(system_ns, path='/system')

# Common models for request/response schemas
error_model = api.model('Error', {
    'error': fields.String(required=True, description='Error message'),
    'code': fields.String(description='Error code'),
    'timestamp': fields.DateTime(description='Error timestamp')
})

validation_request = api.model('ValidationRequest', {
    'request_line': fields.String(
        required=True,
        description='HTTP request line to validate',
        example='GET /index.html HTTP/1.1'
    )
})

validation_result = api.model('ValidationResult', {
    'is_valid': fields.Boolean(required=True, description='Whether the request is valid'),
    'request_line': fields.String(required=True, description='Original request line'),
    'tokens': fields.List(fields.String, description='Tokenized request components'),
    'parse_trees': fields.List(fields.Raw, description='CFG parse trees'),
    'errors': fields.List(fields.String, description='Validation errors'),
    'warnings': fields.List(fields.String, description='Validation warnings'),
    'timestamp': fields.DateTime(description='Validation timestamp'),
    'processing_time': fields.Float(description='Processing time in seconds')
})

batch_validation_request = api.model('BatchValidationRequest', {
    'requests': fields.List(
        fields.String,
        required=True,
        description='List of HTTP request lines to validate',
        example=['GET / HTTP/1.1', 'GET /index.html HTTP/1.0']
    )
})

batch_validation_result = api.model('BatchValidationResult', {
    'results': fields.List(fields.Nested(validation_result), description='Individual validation results'),
    'total_processed': fields.Integer(description='Total number of requests processed'),
    'processing_time': fields.Float(description='Total processing time in seconds')
})

grammar_rule = api.model('GrammarRule', {
    'lhs': fields.String(required=True, description='Left-hand side of the rule'),
    'rhs': fields.String(required=True, description='Right-hand side of the rule'),
    'rule': fields.String(required=True, description='Complete rule representation')
})

grammar_info = api.model('GrammarInfo', {
    'rules': fields.List(fields.Nested(grammar_rule), description='CFG production rules'),
    'description': fields.String(description='Grammar description'),
    'terminals': fields.Raw(description='Terminal symbols'),
    'production_rules': fields.List(fields.String, description='Production rules list')
})

example_request = api.model('ExampleRequest', {
    'request': fields.String(required=True, description='Example HTTP request'),
    'description': fields.String(required=True, description='Description of the example'),
    'expected': fields.Boolean(required=True, description='Expected validation result')
})

analytics_summary = api.model('AnalyticsSummary', {
    'total_requests': fields.Integer(description='Total number of requests'),
    'valid_requests': fields.Integer(description='Number of valid requests'),
    'invalid_requests': fields.Integer(description='Number of invalid requests'),
    'success_rate': fields.Float(description='Success rate percentage'),
    'avg_response_time': fields.Float(description='Average response time'),
    'common_errors': fields.List(fields.String, description='Most common error types')
})

health_status = api.model('HealthStatus', {
    'status': fields.String(required=True, description='Service health status'),
    'timestamp': fields.DateTime(required=True, description='Health check timestamp'),
    'version': fields.String(description='API version'),
    'uptime': fields.String(description='Service uptime'),
    'components': fields.Raw(description='Component health status')
})

# NLP Models
summarization_request = api.model('SummarizationRequest', {
    'text': fields.String(required=True, description='Text to summarize'),
    'method': fields.String(description='Summarization method', enum=['tf_idf', 'textrank', 'lsa']),
    'summary_length': fields.Integer(description='Desired summary length', default=3)
})

summarization_result = api.model('SummarizationResult', {
    'summary': fields.List(fields.String, description='Summary sentences'),
    'method_used': fields.String(description='Method used for summarization'),
    'original_length': fields.Integer(description='Original text length'),
    'summary_length': fields.Integer(description='Summary length'),
    'compression_ratio': fields.Float(description='Compression ratio')
})

query_request = api.model('QueryRequest', {
    'query': fields.String(required=True, description='Query to process'),
    'context': fields.String(description='Additional context')
})

query_result = api.model('QueryResult', {
    'response': fields.String(description='Query response'),
    'intent': fields.String(description='Detected intent'),
    'entities': fields.List(fields.String, description='Extracted entities'),
    'confidence': fields.Float(description='Confidence score')
})

classification_request = api.model('ClassificationRequest', {
    'text': fields.String(required=True, description='Text to classify'),
    'method': fields.String(description='Classification method', enum=['rule_based', 'naive_bayes', 'ensemble'])
})

classification_result = api.model('ClassificationResult', {
    'predicted_category': fields.String(description='Predicted category'),
    'confidence': fields.Float(description='Confidence score'),
    'method_used': fields.String(description='Classification method used'),
    'all_scores': fields.Raw(description='All category scores')
})

# Validation Endpoints
@validation_ns.route('/validate')
class ValidateRequest(Resource):
    @validation_ns.doc('validate_request')
    @validation_ns.expect(validation_request)
    @validation_ns.marshal_with(validation_result, code=200)
    @validation_ns.response(400, 'Invalid request format', error_model)
    @validation_ns.response(500, 'Internal server error', error_model)
    def post(self):
        """
        Validate a single HTTP request line using CFG rules
        
        Validates the syntax of an HTTP GET request according to formal grammar rules.
        Returns detailed validation results including parse trees and error information.
        """
        pass

@validation_ns.route('/validate/batch')
class ValidateBatch(Resource):
    @validation_ns.doc('validate_batch')
    @validation_ns.expect(batch_validation_request)
    @validation_ns.marshal_with(batch_validation_result, code=200)
    @validation_ns.response(400, 'Invalid request format', error_model)
    def post(self):
        """
        Validate multiple HTTP request lines in a single operation
        
        Efficiently processes multiple HTTP requests and returns validation results
        for each request along with batch processing statistics.
        """
        pass

# Grammar Endpoints
@grammar_ns.route('/')
class GrammarRules(Resource):
    @grammar_ns.doc('get_grammar')
    @grammar_ns.marshal_with(grammar_info, code=200)
    def get(self):
        """
        Get Context-Free Grammar rules and structure
        
        Returns the complete CFG specification used for HTTP request validation,
        including production rules, terminals, and grammar description.
        """
        pass

@grammar_ns.route('/examples')
class GrammarExamples(Resource):
    @grammar_ns.doc('get_examples')
    @grammar_ns.marshal_list_with(example_request, code=200)
    def get(self):
        """
        Get example HTTP requests for testing
        
        Returns a collection of valid and invalid HTTP request examples
        for testing and educational purposes.
        """
        pass

# Analytics Endpoints
@analytics_ns.route('/summary')
class AnalyticsSummary(Resource):
    @analytics_ns.doc('get_analytics')
    @analytics_ns.marshal_with(analytics_summary, code=200)
    @analytics_ns.param('days', 'Number of days to analyze', type=int, default=7)
    def get(self):
        """
        Get validation analytics and statistics
        
        Returns comprehensive analytics including success rates, common errors,
        and performance metrics for the specified time period.
        """
        pass

@analytics_ns.route('/detailed')
class DetailedAnalytics(Resource):
    @analytics_ns.doc('get_detailed_analytics')
    @analytics_ns.param('days', 'Number of days to analyze', type=int, default=7)
    @analytics_ns.param('limit', 'Maximum number of records', type=int, default=100)
    def get(self):
        """
        Get detailed analytics with individual request logs
        
        Returns detailed analytics information including individual request logs,
        error patterns, and performance metrics.
        """
        pass

# System Endpoints
@system_ns.route('/health')
class HealthCheck(Resource):
    @system_ns.doc('health_check')
    @system_ns.marshal_with(health_status, code=200)
    def get(self):
        """
        Health check endpoint
        
        Returns the current health status of the API service including
        uptime, version information, and component status.
        """
        pass

@system_ns.route('/version')
class Version(Resource):
    @system_ns.doc('get_version')
    def get(self):
        """
        Get API version information
        
        Returns version information, build details, and feature flags.
        """
        pass

# NLP Endpoints
@nlp_ns.route('/summarization/summarize')
class TextSummarization(Resource):
    @nlp_ns.doc('summarize_text')
    @nlp_ns.expect(summarization_request)
    @nlp_ns.marshal_with(summarization_result, code=200)
    @nlp_ns.response(400, 'Invalid request', error_model)
    def post(self):
        """
        Summarize text using various algorithms
        
        Generates text summaries using multiple algorithms including TF-IDF,
        TextRank, and LSA with configurable summary length.
        """
        pass

@nlp_ns.route('/query/process')
class QueryProcessing(Resource):
    @nlp_ns.doc('process_query')
    @nlp_ns.expect(query_request)
    @nlp_ns.marshal_with(query_result, code=200)
    def post(self):
        """
        Process natural language queries
        
        Analyzes queries to detect intent, extract entities, and provide
        contextual responses with confidence scoring.
        """
        pass

@nlp_ns.route('/classification/classify')
class DocumentClassification(Resource):
    @nlp_ns.doc('classify_document')
    @nlp_ns.expect(classification_request)
    @nlp_ns.marshal_with(classification_result, code=200)
    def post(self):
        """
        Classify documents into categories
        
        Classifies text documents into predefined categories using
        rule-based, machine learning, or ensemble methods.
        """
        pass

# Automata Endpoints
@automata_ns.route('/nfa/match')
class NFAMatching(Resource):
    @automata_ns.doc('nfa_match')
    @automata_ns.param('pattern', 'Regular expression pattern', required=True)
    @automata_ns.param('text', 'Text to match against', required=True)
    def post(self):
        """
        Match text using NFA (Nondeterministic Finite Automaton)
        
        Uses Thompson's Construction to build an NFA from a regular expression
        and matches it against the provided text with execution traces.
        """
        pass

@automata_ns.route('/dfa/match')
class DFAMatching(Resource):
    @automata_ns.doc('dfa_match')
    @automata_ns.param('pattern', 'Regular expression pattern', required=True)
    @automata_ns.param('text', 'Text to match against', required=True)
    def post(self):
        """
        Match text using DFA (Deterministic Finite Automaton)
        
        Converts NFA to DFA using Subset Construction algorithm and performs
        deterministic pattern matching with performance optimization.
        """
        pass

@automata_ns.route('/regex/compare')
class RegexComparison(Resource):
    @automata_ns.doc('compare_regex_methods')
    @automata_ns.param('pattern', 'Regular expression pattern', required=True)
    @automata_ns.param('text', 'Text to match against', required=True)
    def post(self):
        """
        Compare NFA, DFA, and Python regex performance
        
        Benchmarks pattern matching performance across different automata
        implementations and provides detailed performance metrics.
        """
        pass

def init_swagger_docs(app: Flask):
    """Initialize Swagger documentation with the Flask app."""
    app.register_blueprint(api_bp)
    CORS(api_bp)
    return api

# Example usage
if __name__ == '__main__':
    from flask import Flask
    
    app = Flask(__name__)
    init_swagger_docs(app)
    
    print("Swagger documentation available at: http://localhost:5000/api/docs/")
    app.run(debug=True)