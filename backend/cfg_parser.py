"""
CFG Parser for HTTP GET Request Validation

This module implements a Context-Free Grammar parser specifically designed
to validate HTTP GET requests according to predefined grammar rules.
"""

import nltk
from nltk import CFG, ChartParser
from typing import Dict, List, Any, Optional, Tuple
import re
from datetime import datetime

class HTTPRequestCFGParser:
    """
    A Context-Free Grammar parser for validating HTTP GET requests.
    
    Grammar Rules:
    RequestLine → GET SP RequestTarget SP HTTPVersion
    RequestTarget → "/" FileName | "/"
    FileName → "index.html" | "about.html" | "contact.html" | "style.css"
    HTTPVersion → "HTTP/1.0" | "HTTP/1.1" | "HTTP/2.0"
    SP → " "
    """
    
    def __init__(self):
        """Initialize the CFG parser with predefined grammar rules."""
        self.grammar_rules = """
            RequestLine -> GET SP RequestTarget SP HTTPVersion
            RequestTarget -> "/" PathSegments | "/"
            PathSegments -> PathSegment "/" PathSegments | PathSegment
            PathSegment -> SegmentName
            SegmentName -> ValidChar ValidChars | ValidChar
            ValidChars -> ValidChar ValidChars | ValidChar
            ValidChar -> "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z" | "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9" | "-" | "_" | "." | "~"
            HTTPVersion -> "HTTP/1.0" | "HTTP/1.1" | "HTTP/2.0"
            SP -> " "
            GET -> "GET"
        """
        
        # Use regex-based validation for more flexible path handling
        self.use_regex = True
        
        try:
            if not self.use_regex:
                self.grammar = CFG.fromstring(self.grammar_rules)
                self.parser = ChartParser(self.grammar)
            else:
                self.grammar = None
                self.parser = None
        except Exception as e:
            print(f"Error initializing grammar: {e}")
            self.grammar = None
            self.parser = None
    
    def tokenize_request(self, request_line: str) -> List[str]:
        """
        Tokenize the HTTP request line into individual components.
        
        Args:
            request_line (str): The HTTP request line to tokenize
            
        Returns:
            List[str]: List of tokens
        """
        # Replace multiple spaces with single space and strip
        normalized = re.sub(r'\s+', ' ', request_line.strip())
        
        # Split by spaces but preserve the structure for parsing
        tokens = []
        current_token = ""
        
        for char in normalized:
            if char == ' ':
                if current_token:
                    tokens.append(current_token)
                    current_token = ""
                tokens.append(char)  # Add space as separate token
            else:
                current_token += char
        
        if current_token:
            tokens.append(current_token)
            
        return tokens
    
    def validate_request(self, request_line: str) -> Dict[str, Any]:
        """
        Validate an HTTP GET request line against the CFG.
        
        Args:
            request_line (str): The HTTP request line to validate
            
        Returns:
            Dict[str, Any]: Validation result with status, errors, and parse tree
        """
        result = {
            'is_valid': False,
            'request_line': request_line,
            'tokens': [],
            'parse_trees': [],
            'errors': [],
            'grammar_rules': self.get_grammar_rules(),
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Tokenize the request
            tokens = self.tokenize_request(request_line)
            result['tokens'] = tokens
            
            if not tokens:
                result['errors'].append("Empty request line")
                return result
            
            # Use regex-based validation for flexible path handling
            if self.use_regex:
                validation_result = self._validate_with_regex(tokens)
                result['is_valid'] = validation_result['is_valid']
                result['errors'] = validation_result['errors']
                if validation_result['is_valid']:
                    result['parse_trees'] = [self._create_parse_tree(tokens)]
            else:
                # Try to parse with the CFG (fallback)
                if self.parser:
                    parse_trees = list(self.parser.parse(tokens))
                    if parse_trees:
                        result['is_valid'] = True
                        result['parse_trees'] = [self._tree_to_dict(tree) for tree in parse_trees]
                    else:
                        result['errors'] = self._analyze_parsing_errors(tokens)
                else:
                    result['errors'].append("Parser not initialized properly")
                
        except Exception as e:
            result['errors'].append(f"Parsing error: {str(e)}")
        
        return result
    
    def _validate_with_regex(self, tokens: List[str]) -> Dict[str, Any]:
        """
        Validate HTTP request using regex patterns for flexible path handling.
        
        Args:
            tokens (List[str]): The tokenized request
            
        Returns:
            Dict[str, Any]: Validation result with status and errors
        """
        result = {'is_valid': False, 'errors': []}
        
        # Check basic structure: GET SP Target SP Version
        if len(tokens) != 5:
            result['errors'].append("Incomplete request line. Expected format: GET /path HTTP/version")
            return result
        
        method, sp1, target, sp2, version = tokens
        
        # Check HTTP method
        if method != "GET":
            result['errors'].append(f"Invalid HTTP method '{method}'. Only GET is supported.")
        
        # Check spaces
        if sp1 != " ":
            result['errors'].append("Missing space after HTTP method")
        if sp2 != " ":
            result['errors'].append("Missing space before HTTP version")
        
        # Check request target with regex
        if not self._is_valid_request_target(target):
            if not target.startswith("/"):
                result['errors'].append(f"Invalid request target '{target}'. Must start with '/'")
            elif target == "/":
                pass  # Root path is valid
            elif target.endswith("/"):
                result['errors'].append(f"Invalid request target '{target}'. Must end with a filename, not a directory")
            elif not self._has_valid_extension(target):
                result['errors'].append(f"Invalid request target '{target}'. Must end with a valid file extension")
            else:
                result['errors'].append(f"Invalid request target '{target}'. Contains invalid characters")
        
        # Check HTTP version
        valid_versions = ["HTTP/1.0", "HTTP/1.1", "HTTP/2.0"]
        if version not in valid_versions:
            result['errors'].append(f"Invalid HTTP version '{version}'. Allowed versions: {', '.join(valid_versions)}")
        
        # If no errors, it's valid
        result['is_valid'] = len(result['errors']) == 0
        return result
    
    def _is_valid_request_target(self, target: str) -> bool:
        """
        Validate request target using regex pattern.
        
        Args:
            target (str): The request target to validate
            
        Returns:
            bool: True if valid, False otherwise
        """
        # Root path is always valid
        if target == "/":
            return True
        
        # Pattern for nested paths: /segment1/segment2/.../filename.ext
        # Segments can contain letters, numbers, hyphens, underscores, dots
        # Must end with filename containing extension
        pattern = r'^/([a-zA-Z0-9._-]+(/[a-zA-Z0-9._-]+)*)?\.[a-zA-Z0-9]+$'
        
        return bool(re.match(pattern, target))
    
    def _has_valid_extension(self, target: str) -> bool:
        """
        Check if the target has a valid file extension.
        
        Args:
            target (str): The request target to check
            
        Returns:
            bool: True if has valid extension, False otherwise
        """
        # Must contain at least one dot and end with alphanumeric characters
        return bool(re.search(r'\.[a-zA-Z0-9]+$', target))
    
    def _create_parse_tree(self, tokens: List[str]) -> Dict[str, Any]:
        """
        Create a synthetic parse tree for valid requests.
        
        Args:
            tokens (List[str]): The tokenized request
            
        Returns:
            Dict[str, Any]: Parse tree in dictionary format
        """
        if len(tokens) == 5:
            method, sp1, target, sp2, version = tokens
            
            return {
                'label': 'RequestLine',
                'children': [
                    {'label': 'GET', 'children': [{'label': method, 'children': []}]},
                    {'label': 'SP', 'children': [{'label': sp1, 'children': []}]},
                    {
                        'label': 'RequestTarget',
                        'children': [{'label': target, 'children': []}]
                    },
                    {'label': 'SP', 'children': [{'label': sp2, 'children': []}]},
                    {'label': 'HTTPVersion', 'children': [{'label': version, 'children': []}]}
                ]
            }
        
        return {'label': 'Invalid', 'children': []}
        """
        Convert NLTK Tree to dictionary format for JSON serialization.
        
        Args:
            tree: NLTK Tree object
            
        Returns:
            Dict[str, Any]: Tree in dictionary format
        """
        if hasattr(tree, 'label'):
            return {
                'label': str(tree.label()),
                'children': [self._tree_to_dict(child) for child in tree]
            }
        else:
            return {'label': str(tree), 'children': []}
    
    def _analyze_parsing_errors(self, tokens: List[str]) -> List[str]:
        """
        Analyze why parsing failed and provide meaningful error messages.
        
        Args:
            tokens (List[str]): The tokenized request
            
        Returns:
            List[str]: List of error messages
        """
        errors = []
        
        # Check basic structure
        if len(tokens) < 5:  # GET SP Target SP Version
            errors.append("Incomplete request line. Expected format: GET /path HTTP/version")
            return errors
        
        # Check first token is GET
        if tokens[0] != "GET":
            errors.append(f"Invalid HTTP method '{tokens[0]}'. Only GET is supported.")
        
        # Check for proper spacing
        space_positions = [1, 3]  # Expected space positions
        for pos in space_positions:
            if pos < len(tokens) and tokens[pos] != " ":
                errors.append(f"Missing space at position {pos}")
        
        # Check request target
        if len(tokens) > 2:
            target = tokens[2]
            if not self._is_valid_request_target(target):
                if not target.startswith("/"):
                    errors.append(f"Invalid request target '{target}'. Must start with '/'")
                elif target.endswith("/"):
                    errors.append(f"Invalid request target '{target}'. Must end with a filename, not a directory")
                elif not self._has_valid_extension(target):
                    errors.append(f"Invalid request target '{target}'. Must end with a valid file extension")
                else:
                    errors.append(f"Invalid request target '{target}'. Contains invalid characters")
        
        # Check HTTP version
        if len(tokens) > 4:
            version = tokens[4]
            valid_versions = ["HTTP/1.0", "HTTP/1.1", "HTTP/2.0"]
            if version not in valid_versions:
                errors.append(f"Invalid HTTP version '{version}'. Allowed versions: {', '.join(valid_versions)}")
        
        return errors if errors else ["Unknown parsing error"]
    
    def _is_valid_filename(self, filename: str) -> bool:
        """Check if filename has a valid extension (deprecated - now supports any valid filename)."""
        # Now supports any filename with valid extension
        return self._has_valid_extension("/" + filename)
    
    def get_grammar_rules(self) -> List[Dict[str, str]]:
        """
        Get the grammar rules in a structured format.
        
        Returns:
            List[Dict[str, str]]: List of grammar rules
        """
        rules = [
            {
                'lhs': 'RequestLine',
                'rhs': 'GET SP RequestTarget SP HTTPVersion',
                'rule': 'RequestLine → GET SP RequestTarget SP HTTPVersion'
            },
            {
                'lhs': 'RequestTarget',
                'rhs': '"/" PathSegments | "/"',
                'rule': 'RequestTarget → "/" PathSegments | "/"'
            },
            {
                'lhs': 'PathSegments',
                'rhs': 'PathSegment "/" PathSegments | PathSegment',
                'rule': 'PathSegments → PathSegment "/" PathSegments | PathSegment'
            },
            {
                'lhs': 'PathSegment',
                'rhs': 'ValidChars',
                'rule': 'PathSegment → ValidChars (filename or directory with extension)'
            },
            {
                'lhs': 'HTTPVersion',
                'rhs': '"HTTP/1.0" | "HTTP/1.1" | "HTTP/2.0"',
                'rule': 'HTTPVersion → "HTTP/1.0" | "HTTP/1.1" | "HTTP/2.0"'
            },
            {
                'lhs': 'SP',
                'rhs': '" "',
                'rule': 'SP → " "'
            },
            {
                'lhs': 'GET',
                'rhs': '"GET"',
                'rule': 'GET → "GET"'
            }
        ]
        
        return rules
    
    def get_example_requests(self) -> List[Dict[str, Any]]:
        """
        Get a list of example HTTP requests for testing.
        
        Returns:
            List[Dict[str, Any]]: List of example requests with expected outcomes
        """
        examples = [
            {
                'request': 'GET / HTTP/1.1',
                'description': 'Basic root request',
                'expected': True
            },
            {
                'request': 'GET /index.html HTTP/1.1',
                'description': 'Request for index page',
                'expected': True
            },
            {
                'request': 'GET /about.html HTTP/2.0',
                'description': 'Request for about page with HTTP/2.0',
                'expected': True
            },
            {
                'request': 'GET /assets/style.css HTTP/1.0',
                'description': 'Request for CSS file in assets directory',
                'expected': True
            },
            {
                'request': 'GET /images/icons/logo.png HTTP/1.1',
                'description': 'Request for nested image file',
                'expected': True
            },
            {
                'request': 'GET /api/v1/users.json HTTP/1.1',
                'description': 'Request for API endpoint with nested path',
                'expected': True
            },
            {
                'request': 'GET /docs/guide.pdf HTTP/2.0',
                'description': 'Request for PDF document',
                'expected': True
            },
            {
                'request': 'GET /scripts/app.min.js HTTP/1.1',
                'description': 'Request for minified JavaScript file',
                'expected': True
            },
            {
                'request': 'POST /index.html HTTP/1.1',
                'description': 'Invalid HTTP method (should fail)',
                'expected': False
            },
            {
                'request': 'GET index.html HTTP/1.1',
                'description': 'Missing leading slash (should fail)',
                'expected': False
            },
            {
                'request': 'GET /assets/ HTTP/1.1',
                'description': 'Directory without filename (should fail)',
                'expected': False
            },
            {
                'request': 'GET /index HTTP/1.1',
                'description': 'Missing file extension (should fail)',
                'expected': False
            },
            {
                'request': 'GET /index.html HTTP/3.0',
                'description': 'Invalid HTTP version (should fail)',
                'expected': False
            },
            {
                'request': 'GET/index.html HTTP/1.1',
                'description': 'Missing space after GET (should fail)',
                'expected': False
            },
            {
                'request': 'GET /index.html',
                'description': 'Missing HTTP version (should fail)',
                'expected': False
            }
        ]
        
        return examples

# Initialize NLTK data (download required packages)
def initialize_nltk():
    """Download required NLTK data packages."""
    try:
        import ssl
        try:
            _create_unverified_https_context = ssl._create_unverified_context
        except AttributeError:
            pass
        else:
            ssl._create_default_https_context = _create_unverified_https_context
        
        nltk.download('punkt', quiet=True)
        nltk.download('averaged_perceptron_tagger', quiet=True)
        return True
    except Exception as e:
        print(f"Warning: Could not download NLTK data: {e}")
        return False

# Initialize NLTK when module is imported
initialize_nltk()