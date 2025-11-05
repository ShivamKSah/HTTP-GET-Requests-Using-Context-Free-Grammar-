"""
Conftest.py - Shared test fixtures and configuration for CFG QODER project.

This module provides common test fixtures, mock objects, and test utilities
used across all test modules.
"""

import pytest
import sys
import os
from unittest.mock import Mock, MagicMock
from typing import Dict, Any, List

# Add backend directory to path
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Test data constants
VALID_HTTP_REQUESTS = [
    "GET / HTTP/1.1",
    "GET /index.html HTTP/1.0", 
    "GET /api/users HTTP/2.0",
    "GET /assets/style.css HTTP/1.1",
    "GET /docs/guide.pdf HTTP/1.1"
]

INVALID_HTTP_REQUESTS = [
    "POST /index.html HTTP/1.1",  # Invalid method
    "GET invalid_path HTTP/1.1",  # Invalid path
    "GET /index.html HTTP/3.0",   # Invalid version
    "INVALID REQUEST",            # Completely invalid
    ""                           # Empty request
]

SAMPLE_HTTP_HEADERS = """Host: example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64)
Accept: text/html,application/xhtml+xml
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Connection: keep-alive"""

SAMPLE_REGEX_PATTERNS = [
    ("GET", r"^GET$"),
    ("HTTP_VERSION", r"^HTTP/[12]\.[01]$"),
    ("URI_PATH", r"^/[\w\./]*$"),
    ("EMAIL", r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")
]

@pytest.fixture
def cfg_parser():
    """Fixture providing a CFG parser instance."""
    from cfg_parser import HTTPRequestCFGParser
    return HTTPRequestCFGParser()

@pytest.fixture
def nfa_engine():
    """Fixture providing an NFA engine instance."""
    from nfa_engine import NFAEngine
    return NFAEngine()

@pytest.fixture
def dfa_engine():
    """Fixture providing a DFA engine instance."""
    from dfa_engine import DFAEngine
    return DFAEngine()

@pytest.fixture
def regex_matcher():
    """Fixture providing a regex pattern matcher instance."""
    from regex_pattern_matcher import RegexPatternMatcher
    return RegexPatternMatcher()

@pytest.fixture
def fsa_tokenizer():
    """Fixture providing an FSA tokenizer instance."""
    from fsa_tokenizer import HTTPRequestFSA
    return HTTPRequestFSA()

@pytest.fixture
def pda_parser():
    """Fixture providing a PDA parser instance."""
    from pda_parser import HTTPRequestPDA
    return HTTPRequestPDA()

@pytest.fixture
def valid_requests():
    """Fixture providing valid HTTP request test data."""
    return VALID_HTTP_REQUESTS.copy()

@pytest.fixture
def invalid_requests():
    """Fixture providing invalid HTTP request test data."""
    return INVALID_HTTP_REQUESTS.copy()

@pytest.fixture
def sample_headers():
    """Fixture providing sample HTTP headers."""
    return SAMPLE_HTTP_HEADERS

@pytest.fixture
def regex_patterns():
    """Fixture providing sample regex patterns for testing."""
    return SAMPLE_REGEX_PATTERNS.copy()

@pytest.fixture
def flask_app():
    """Fixture providing Flask app for API testing."""
    from app import app
    app.config['TESTING'] = True
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///:memory:'
    return app

@pytest.fixture
def client(flask_app):
    """Fixture providing Flask test client."""
    return flask_app.test_client()

@pytest.fixture
def mock_database():
    """Fixture providing mock database for testing."""
    return MagicMock()

@pytest.fixture
def performance_test_data():
    """Fixture providing performance test data."""
    return {
        'small_input': "GET / HTTP/1.1",
        'medium_input': "GET " + "/path" * 10 + " HTTP/1.1", 
        'large_input': "GET " + "/very/long/path" * 100 + " HTTP/1.1",
        'regex_patterns': [
            r"^GET\s+/.*\s+HTTP/[12]\.[01]$",
            r"^(GET|POST|PUT|DELETE)\s+",
            r"HTTP/[12]\.[01]$"
        ]
    }

class TestHelpers:
    """Helper class with utility methods for testing."""
    
    @staticmethod
    def assert_validation_result(result: Dict[str, Any], expected_valid: bool):
        """Assert validation result structure and validity."""
        assert isinstance(result, dict)
        assert 'is_valid' in result
        assert result['is_valid'] == expected_valid
        assert 'errors' in result
        assert isinstance(result['errors'], list)
        
    @staticmethod
    def assert_parse_tree_structure(parse_tree: Dict[str, Any]):
        """Assert parse tree has correct structure."""
        assert isinstance(parse_tree, dict)
        assert 'label' in parse_tree
        assert 'children' in parse_tree
        assert isinstance(parse_tree['children'], list)
        
    @staticmethod
    def count_parse_tree_nodes(parse_tree: Dict[str, Any]) -> int:
        """Count nodes in a parse tree recursively."""
        if not parse_tree or 'children' not in parse_tree:
            return 1
        return 1 + sum(TestHelpers.count_parse_tree_nodes(child) 
                      for child in parse_tree['children'])

@pytest.fixture
def test_helpers():
    """Fixture providing test helper methods."""
    return TestHelpers

# Performance measurement utilities
@pytest.fixture
def performance_timer():
    """Fixture providing performance measurement utilities."""
    import time
    
    class Timer:
        def __init__(self):
            self.start_time = None
            self.end_time = None
            
        def start(self):
            self.start_time = time.perf_counter()
            
        def stop(self):
            self.end_time = time.perf_counter()
            
        @property
        def elapsed(self):
            if self.start_time and self.end_time:
                return self.end_time - self.start_time
            return None
            
    return Timer()

# Parameterized test data
@pytest.fixture(params=VALID_HTTP_REQUESTS)
def valid_request_param(request):
    """Parameterized fixture for valid HTTP requests."""
    return request.param

@pytest.fixture(params=INVALID_HTTP_REQUESTS)
def invalid_request_param(request):
    """Parameterized fixture for invalid HTTP requests."""
    return request.param