"""
Test suite for CFG Parser module.

Tests the HTTP request parsing using Context-Free Grammar rules,
including validation, parse tree generation, and error handling.
"""

import pytest
from typing import Dict, Any, List
import sys
import os

# Add backend to path for imports
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from cfg_parser import HTTPRequestCFGParser


class TestCFGParser:
    """Test cases for HTTP Request CFG Parser."""
    
    def test_parser_initialization(self, cfg_parser):
        """Test CFG parser initializes correctly."""
        assert cfg_parser is not None
        assert hasattr(cfg_parser, 'parse')
        assert hasattr(cfg_parser, 'validate_request')
        
    def test_valid_requests_parsing(self, cfg_parser, valid_requests):
        """Test parsing of valid HTTP requests."""
        for request in valid_requests:
            result = cfg_parser.validate_request(request)
            assert result['is_valid'] == True, f"Failed for request: {request}"
            assert len(result['errors']) == 0
            assert 'parse_trees' in result
            assert len(result['parse_trees']) > 0
            
    def test_invalid_requests_parsing(self, cfg_parser, invalid_requests):
        """Test parsing of invalid HTTP requests."""
        for request in invalid_requests:
            if request:  # Skip empty requests
                result = cfg_parser.validate_request(request)
                assert result['is_valid'] == False, f"Should fail for request: {request}"
                assert len(result['errors']) > 0
                
    def test_parse_tree_structure(self, cfg_parser, test_helpers):
        """Test parse tree has correct structure."""
        result = cfg_parser.validate_request("GET /index.html HTTP/1.1")
        assert result['is_valid'] == True
        
        parse_trees = result['parse_trees']
        assert len(parse_trees) > 0
        
        for tree in parse_trees:
            test_helpers.assert_parse_tree_structure(tree)
            node_count = test_helpers.count_parse_tree_nodes(tree)
            assert node_count >= 5  # Minimum nodes for valid parse
            
    def test_tokenization(self, cfg_parser):
        """Test request tokenization."""
        request = "GET /test.html HTTP/1.1"
        result = cfg_parser.validate_request(request)
        
        tokens = result.get('tokens', [])
        assert len(tokens) > 0
        assert 'GET' in tokens
        assert '/test.html' in tokens or any('/test.html' in token for token in tokens)
        assert 'HTTP/1.1' in tokens
        
    def test_grammar_rules_retrieval(self, cfg_parser):
        """Test grammar rules can be retrieved."""
        rules = cfg_parser.get_grammar_rules()
        assert isinstance(rules, list)
        assert len(rules) > 0
        
        # Check rule structure
        for rule in rules:
            assert 'lhs' in rule
            assert 'rhs' in rule
            assert 'rule' in rule
            
    def test_example_requests(self, cfg_parser):
        """Test example requests functionality."""
        examples = cfg_parser.get_example_requests()
        assert isinstance(examples, list)
        assert len(examples) > 0
        
        for example in examples:
            assert 'request' in example
            assert 'description' in example
            assert 'expected' in example
            assert isinstance(example['expected'], bool)
            
    def test_edge_cases(self, cfg_parser):
        """Test edge cases and boundary conditions."""
        edge_cases = [
            "",  # Empty string
            " ",  # Single space
            "GET",  # Incomplete request
            "GET /",  # Missing version
            "GET / HTTP",  # Incomplete version
            "get / http/1.1",  # Lowercase (should fail)
            "GET// HTTP/1.1",  # Invalid path
            "GET / HTTP/1.1 extra",  # Extra content
        ]
        
        for case in edge_cases:
            result = cfg_parser.validate_request(case)
            assert 'is_valid' in result
            assert 'errors' in result
            assert isinstance(result['errors'], list)
            
    def test_semantic_analysis(self, cfg_parser):
        """Test semantic analysis features."""
        result = cfg_parser.validate_request("GET /index.html HTTP/1.1")
        
        if 'semantic_analysis' in result:
            semantic = result['semantic_analysis']
            assert isinstance(semantic, dict)
            
            if 'warnings' in semantic:
                assert isinstance(semantic['warnings'], list)
                
    @pytest.mark.performance
    def test_parsing_performance(self, cfg_parser, performance_timer):
        """Test parsing performance for reasonable response times."""
        request = "GET /api/v1/users/12345/profile.json HTTP/1.1"
        
        # Warm up
        cfg_parser.validate_request(request)
        
        # Actual test
        performance_timer.start()
        for _ in range(100):
            cfg_parser.validate_request(request)
        performance_timer.stop()
        
        avg_time = performance_timer.elapsed / 100
        assert avg_time < 0.01, f"Average parsing time too slow: {avg_time:.4f}s"
        
    def test_complex_paths(self, cfg_parser):
        """Test parsing of complex URI paths."""
        complex_paths = [
            "GET /api/v1/users/123 HTTP/1.1",
            "GET /assets/css/style.min.css HTTP/1.1", 
            "GET /docs/guide.pdf HTTP/1.1",
            "GET /images/icons/logo.png HTTP/2.0"
        ]
        
        for request in complex_paths:
            result = cfg_parser.validate_request(request)
            assert result['is_valid'] == True, f"Failed for: {request}"
            
    def test_http_versions(self, cfg_parser):
        """Test different HTTP version support."""
        versions = ["HTTP/1.0", "HTTP/1.1", "HTTP/2.0"]
        
        for version in versions:
            request = f"GET /test {version}"
            result = cfg_parser.validate_request(request)
            assert result['is_valid'] == True, f"Failed for version: {version}"
            
        # Test invalid versions
        invalid_versions = ["HTTP/3.0", "HTTP/0.9", "HTTP/1.5"]
        for version in invalid_versions:
            request = f"GET /test {version}"
            result = cfg_parser.validate_request(request)
            assert result['is_valid'] == False, f"Should fail for version: {version}"


class TestCFGParserIntegration:
    """Integration tests for CFG Parser with other components."""
    
    def test_cfg_with_fsa_tokenizer(self, cfg_parser, fsa_tokenizer):
        """Test CFG parser integration with FSA tokenizer."""
        request = "GET /integration/test HTTP/1.1"
        
        # Parse with CFG
        cfg_result = cfg_parser.validate_request(request)
        
        # Tokenize with FSA
        fsa_result = fsa_tokenizer.tokenize_request(request)
        
        # Both should agree on validity
        assert cfg_result['is_valid'] == (len(fsa_result.get('lexical_errors', [])) == 0)
        
    def test_cfg_with_headers(self, cfg_parser):
        """Test CFG parser with HTTP headers (if supported)."""
        request_with_headers = """GET /api/test HTTP/1.1
Host: example.com
User-Agent: Test-Agent"""
        
        # Should handle or gracefully reject headers
        result = cfg_parser.validate_request(request_with_headers)
        assert 'is_valid' in result