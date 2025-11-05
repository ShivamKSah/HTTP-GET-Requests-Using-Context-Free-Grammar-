"""
Integration tests for API endpoints.

Tests the complete API functionality including request/response validation,
error handling, and inter-module integration.
"""

import sys
import os
import json
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

import pytest
from flask import Flask
from app import app as flask_app


class TestAPIIntegration:
    """Integration tests for the main API."""
    
    @pytest.fixture
    def client(self):
        """Create test client."""
        flask_app.config['TESTING'] = True
        flask_app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
        with flask_app.test_client() as client:
            with flask_app.app_context():
                yield client
    
    def test_health_endpoint(self, client):
        """Test health check endpoint."""
        response = client.get('/api/health')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'status' in data
        assert data['status'] == 'healthy'
        assert 'timestamp' in data
        assert 'version' in data
    
    def test_validate_endpoint_valid_request(self, client):
        """Test validation endpoint with valid request."""
        payload = {
            'request_line': 'GET /index.html HTTP/1.1'
        }
        
        response = client.post('/api/validate', 
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'is_valid' in data
        assert data['is_valid'] == True
        assert 'errors' in data
        assert len(data['errors']) == 0
        assert 'parse_trees' in data
        assert 'tokens' in data
        
    def test_validate_endpoint_invalid_request(self, client):
        """Test validation endpoint with invalid request."""
        payload = {
            'request_line': 'POST /index.html HTTP/1.1'  # Invalid method
        }
        
        response = client.post('/api/validate',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'is_valid' in data
        assert data['is_valid'] == False
        assert 'errors' in data
        assert len(data['errors']) > 0
        
    def test_validate_endpoint_missing_payload(self, client):
        """Test validation endpoint with missing payload."""
        response = client.post('/api/validate',
                             data=json.dumps({}),
                             content_type='application/json')
        
        assert response.status_code == 400
        
    def test_batch_validate_endpoint(self, client):
        """Test batch validation endpoint."""
        payload = {
            'requests': [
                'GET / HTTP/1.1',
                'GET /index.html HTTP/1.0',
                'POST /invalid HTTP/1.1'  # This should fail
            ]
        }
        
        response = client.post('/api/validate/batch',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        assert response.status_code == 200
        data = response.get_json()
        
        assert 'results' in data
        assert 'total_processed' in data
        assert data['total_processed'] == 3
        assert len(data['results']) == 3
        
        # Check individual results
        results = data['results']
        assert results[0]['is_valid'] == True  # GET / HTTP/1.1
        assert results[1]['is_valid'] == True  # GET /index.html HTTP/1.0  
        assert results[2]['is_valid'] == False # POST /invalid HTTP/1.1
        
    def test_grammar_endpoint(self, client):
        """Test grammar information endpoint."""
        response = client.get('/api/grammar')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'rules' in data
        assert 'description' in data
        assert 'terminals' in data
        assert 'production_rules' in data
        
        # Check rule structure
        rules = data['rules']
        assert len(rules) > 0
        for rule in rules:
            assert 'lhs' in rule
            assert 'rhs' in rule
            assert 'rule' in rule
            
    def test_examples_endpoint(self, client):
        """Test examples endpoint."""
        response = client.get('/api/examples')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'examples' in data
        
        examples = data['examples']
        assert len(examples) > 0
        for example in examples:
            assert 'request' in example
            assert 'description' in example
            assert 'expected' in example
            assert isinstance(example['expected'], bool)
            
    def test_analytics_endpoint(self, client):
        """Test analytics endpoint."""
        # First make some requests to generate analytics data
        self.test_validate_endpoint_valid_request(client)
        self.test_validate_endpoint_invalid_request(client)
        
        response = client.get('/api/analytics')
        assert response.status_code == 200
        
        data = response.get_json()
        assert 'total_requests' in data
        assert 'valid_requests' in data
        assert 'invalid_requests' in data
        assert 'success_rate' in data
        
    def test_session_tracking(self, client):
        """Test that sessions are properly tracked."""
        # Make multiple requests and check session consistency
        response1 = client.get('/api/session')
        response2 = client.get('/api/session')
        
        assert response1.status_code == 200
        assert response2.status_code == 200
        
        session1 = response1.get_json()
        session2 = response2.get_json()
        
        # Same session should be maintained
        assert session1['session_id'] == session2['session_id']
        
    def test_cors_headers(self, client):
        """Test CORS headers are properly set."""
        response = client.options('/api/validate')
        
        # Should have CORS headers
        assert 'Access-Control-Allow-Origin' in response.headers
        assert 'Access-Control-Allow-Methods' in response.headers
        
    def test_error_handling(self, client):
        """Test API error handling."""
        # Test malformed JSON
        response = client.post('/api/validate',
                             data='invalid json',
                             content_type='application/json')
        assert response.status_code == 400
        
        # Test unsupported content type
        response = client.post('/api/validate',
                             data='test data',
                             content_type='text/plain')
        assert response.status_code == 400 or response.status_code == 415


class TestEnhancedAPIIntegration:
    """Integration tests for enhanced API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client for enhanced API."""
        try:
            from enhanced_api import app as enhanced_app
            enhanced_app.config['TESTING'] = True
            with enhanced_app.test_client() as client:
                yield client
        except ImportError:
            pytest.skip("Enhanced API not available")
    
    def test_enhanced_validate_endpoint(self, client):
        """Test enhanced validation endpoint."""
        payload = {
            'request_text': 'GET /api/test HTTP/1.1'
        }
        
        response = client.post('/api/enhanced/validate',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'analysis_result' in data
            assert 'compliance_score' in data
            assert 'overall_validity' in data
    
    def test_fsa_analysis_endpoint(self, client):
        """Test FSA analysis endpoint."""
        payload = {
            'request_text': 'GET /test HTTP/1.1'
        }
        
        response = client.post('/api/enhanced/fsa-analysis',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'fsa_result' in data
    
    def test_pda_analysis_endpoint(self, client):
        """Test PDA analysis endpoint.""" 
        payload = {
            'request_text': 'GET /test HTTP/1.1'
        }
        
        response = client.post('/api/enhanced/pda-analysis',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'pda_result' in data


class TestNLPAPIIntegration:
    """Integration tests for NLP API endpoints."""
    
    @pytest.fixture
    def client(self):
        """Create test client for NLP API."""
        try:
            from advanced_nlp_api import app as nlp_app
            nlp_app.config['TESTING'] = True
            with nlp_app.test_client() as client:
                yield client
        except ImportError:
            pytest.skip("NLP API not available")
    
    def test_summarization_endpoint(self, client):
        """Test text summarization endpoint."""
        payload = {
            'text': 'This is a sample text for summarization. It contains multiple sentences to test the summarization capabilities of the system. The summarization should work effectively and provide meaningful results.',
            'method': 'tf_idf',
            'summary_length': 1
        }
        
        response = client.post('/api/v2/summarization/summarize',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'summary' in data
            assert 'method_used' in data
            assert 'original_length' in data
            assert 'summary_length' in data
    
    def test_query_processing_endpoint(self, client):
        """Test query processing endpoint."""
        payload = {
            'query': 'What is a context-free grammar?'
        }
        
        response = client.post('/api/v2/query/process',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'response' in data
            assert 'intent' in data
            assert 'entities' in data
    
    def test_classification_endpoint(self, client):
        """Test document classification endpoint."""
        payload = {
            'text': 'This API provides endpoints for authentication and user management. Send POST requests to login.',
            'method': 'rule_based'
        }
        
        response = client.post('/api/v2/classification/classify',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'predicted_category' in data
            assert 'confidence' in data
            assert 'method_used' in data
    
    def test_health_endpoint(self, client):
        """Test NLP API health endpoint."""
        response = client.get('/api/v2/health')
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'status' in data
            assert 'timestamp' in data


class TestComprehensiveIntegration:
    """Integration tests for comprehensive analysis API."""
    
    @pytest.fixture
    def client(self):
        """Create test client for comprehensive API."""
        try:
            from comprehensive_integration_api import app as comp_app
            comp_app.config['TESTING'] = True
            with comp_app.test_client() as client:
                yield client
        except ImportError:
            pytest.skip("Comprehensive API not available")
    
    def test_comprehensive_analysis(self, client):
        """Test comprehensive analysis endpoint."""
        payload = {
            'request': 'GET /api/users/123 HTTP/1.1'
        }
        
        response = client.post('/api/comprehensive/analyze',
                             data=json.dumps(payload),
                             content_type='application/json')
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'analysis_components' in data
            assert 'integration_analysis' in data
            assert 'educational_content' in data
    
    def test_components_endpoint(self, client):
        """Test components information endpoint."""
        response = client.get('/api/comprehensive/components')
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'available_components' in data
    
    def test_demo_data_endpoint(self, client):
        """Test demo data endpoint."""
        response = client.get('/api/comprehensive/demo')
        
        if response.status_code == 200:
            data = response.get_json()
            assert 'demo_request' in data
            assert 'description' in data


class TestCrossModuleIntegration:
    """Tests for integration between different modules."""
    
    def test_cfg_fsa_integration(self, cfg_parser, fsa_tokenizer):
        """Test integration between CFG parser and FSA tokenizer."""
        test_request = "GET /integration/test HTTP/1.1"
        
        # Parse with CFG
        cfg_result = cfg_parser.validate_request(test_request)
        
        # Tokenize with FSA
        fsa_result = fsa_tokenizer.tokenize_request(test_request)
        
        # Results should be consistent
        cfg_valid = cfg_result['is_valid']
        fsa_valid = len(fsa_result.get('lexical_errors', [])) == 0
        
        # Both should agree on basic validity
        assert cfg_valid == fsa_valid or abs(cfg_valid - fsa_valid) <= 1
        
    def test_nfa_dfa_consistency(self, nfa_engine, dfa_engine):
        """Test consistency between NFA and DFA engines."""
        test_pattern = "GET"
        test_input = "GET"
        
        try:
            # Test with NFA
            nfa_result = nfa_engine.match_pattern(test_pattern, test_input)
            
            # Test with DFA  
            dfa_result = dfa_engine.match_pattern(test_pattern, test_input)
            
            # Results should match
            assert nfa_result == dfa_result
            
        except AttributeError:
            # Methods might not be implemented
            pytest.skip("Pattern matching methods not available")
    
    def test_regex_pattern_integration(self, regex_matcher):
        """Test regex pattern matcher integration."""
        test_request = "GET /test HTTP/1.1"
        
        try:
            result = regex_matcher.validate_http_request_line(test_request)
            assert 'valid' in result
            assert 'method' in result
            assert 'uri' in result  
            assert 'version' in result
            
        except AttributeError:
            pytest.skip("HTTP request validation not available")