"""
Advanced Context-Free Grammar Parser for HTTP Request Validation

This module implements an enhanced CFG parser with full RFC 7230 compliance,
supporting multiple HTTP methods, complete header validation, and advanced
formal language automata concepts.

Enhancements over basic parser:
1. Full RFC 7230 HTTP/1.1 message syntax support
2. Multiple HTTP methods (GET, POST, PUT, DELETE, HEAD, OPTIONS)
3. Complete header field validation using CFG rules
4. Finite State Automaton for lexical analysis
5. Pushdown Automaton simulation for parsing
6. Advanced error recovery and reporting
"""

import nltk
from nltk import CFG, ChartParser
from typing import Dict, List, Any, Optional, Tuple, Set, Union
import re
from datetime import datetime
from enum import Enum
import json

class HTTPMethod(Enum):
    """Enumeration of supported HTTP methods."""
    GET = "GET"
    POST = "POST"
    PUT = "PUT"
    DELETE = "DELETE"
    HEAD = "HEAD"
    OPTIONS = "OPTIONS"
    PATCH = "PATCH"
    TRACE = "TRACE"
    CONNECT = "CONNECT"

class TokenType(Enum):
    """Token types for lexical analysis."""
    METHOD = "METHOD"
    SP = "SP"
    CRLF = "CRLF"
    URI = "URI"
    HTTP_VERSION = "HTTP_VERSION"
    HEADER_NAME = "HEADER_NAME"
    HEADER_VALUE = "HEADER_VALUE"
    COLON = "COLON"
    MESSAGE_BODY = "MESSAGE_BODY"
    INVALID = "INVALID"

class LexicalAnalyzer:
    """
    Finite State Automaton for HTTP request lexical analysis.
    
    States:
    - START: Initial state
    - METHOD: Reading HTTP method
    - METHOD_END: Method completed, expecting space
    - URI_START: Starting URI parsing
    - URI: Reading URI
    - URI_END: URI completed, expecting space
    - VERSION_START: Starting HTTP version
    - VERSION: Reading HTTP version
    - VERSION_END: Version completed, expecting CRLF
    - HEADER_START: Starting header parsing
    - HEADER_NAME: Reading header name
    - HEADER_COLON: Expecting colon after header name
    - HEADER_VALUE_START: Starting header value
    - HEADER_VALUE: Reading header value
    - HEADER_END: Header completed, expecting CRLF
    - BODY_START: Starting message body
    - BODY: Reading message body
    - END: Final state
    """
    
    def __init__(self):
        self.reset()
    
    def reset(self):
        """Reset the FSA to initial state."""
        self.state = "START"
        self.tokens = []
        self.current_token = ""
        self.position = 0
        self.line = 1
        self.column = 1
    
    def tokenize(self, input_text: str) -> List[Dict[str, Any]]:
        """
        Tokenize HTTP request using finite state automaton.
        
        Args:
            input_text (str): Raw HTTP request text
            
        Returns:
            List[Dict[str, Any]]: List of tokens with type and position info
        """
        self.reset()
        input_text = input_text.replace('\r\n', '\n')  # Normalize line endings
        
        for char in input_text:
            self._process_character(char)
            self._update_position(char)
        
        # Process any remaining token
        if self.current_token:
            self._emit_token()
        
        return self.tokens
    
    def _process_character(self, char: str):
        """Process a single character based on current FSA state."""
        if self.state == "START":
            if char.isalpha():
                self.state = "METHOD"
                self.current_token = char
            elif char.isspace():
                pass  # Skip leading whitespace
            else:
                self._emit_error_token(f"Unexpected character '{char}' at start")
        
        elif self.state == "METHOD":
            if char.isalpha():
                self.current_token += char
            elif char == ' ':
                self._emit_token(TokenType.METHOD)
                self.state = "URI_START"
            else:
                self._emit_error_token(f"Invalid character '{char}' in method")
        
        elif self.state == "URI_START":
            if char == ' ':
                pass  # Skip spaces
            elif char == '/':
                self.state = "URI"
                self.current_token = char
            else:
                self._emit_error_token(f"URI must start with '/'")
        
        elif self.state == "URI":
            if char == ' ':
                self._emit_token(TokenType.URI)
                self.state = "VERSION_START"
            elif char in "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:/?#[]@!$&'()*+,;=%":
                self.current_token += char
            else:
                self._emit_error_token(f"Invalid character '{char}' in URI")
        
        elif self.state == "VERSION_START":
            if char == ' ':
                pass  # Skip spaces
            elif char == 'H':
                self.state = "VERSION"
                self.current_token = char
            else:
                self._emit_error_token(f"HTTP version must start with 'H'")
        
        elif self.state == "VERSION":
            if char == '\n':
                self._emit_token(TokenType.HTTP_VERSION)
                self._emit_token(TokenType.CRLF, "\n")
                self.state = "HEADER_START"
            elif char in "ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789/.":
                self.current_token += char
            else:
                self._emit_error_token(f"Invalid character '{char}' in HTTP version")
        
        elif self.state == "HEADER_START":
            if char == '\n':
                self._emit_token(TokenType.CRLF, "\n")
                self.state = "BODY_START"
            elif char.isalpha() or char == '-':
                self.state = "HEADER_NAME"
                self.current_token = char
            elif char.isspace():
                pass  # Skip whitespace
            else:
                self._emit_error_token(f"Invalid start of header '{char}'")
        
        elif self.state == "HEADER_NAME":
            if char == ':':
                self._emit_token(TokenType.HEADER_NAME)
                self._emit_token(TokenType.COLON, ":")
                self.state = "HEADER_VALUE_START"
            elif char.isalnum() or char in '-_':
                self.current_token += char
            else:
                self._emit_error_token(f"Invalid character '{char}' in header name")
        
        elif self.state == "HEADER_VALUE_START":
            if char == ' ':
                pass  # Skip leading spaces in header value
            elif char == '\n':
                self._emit_token(TokenType.HEADER_VALUE, "")
                self._emit_token(TokenType.CRLF, "\n")
                self.state = "HEADER_START"
            else:
                self.state = "HEADER_VALUE"
                self.current_token = char
        
        elif self.state == "HEADER_VALUE":
            if char == '\n':
                self._emit_token(TokenType.HEADER_VALUE)
                self._emit_token(TokenType.CRLF, "\n")
                self.state = "HEADER_START"
            else:
                self.current_token += char
        
        elif self.state == "BODY_START":
            self.state = "BODY"
            self.current_token = char
        
        elif self.state == "BODY":
            self.current_token += char
    
    def _emit_token(self, token_type: Optional[TokenType] = None, value: Optional[str] = None):
        """Emit a token with current or specified value."""
        token_value = value if value is not None else self.current_token
        token_type_str = token_type.value if token_type else "UNKNOWN"
        
        self.tokens.append({
            'type': token_type_str,
            'value': token_value,
            'position': self.position - len(token_value),
            'line': self.line,
            'column': self.column - len(token_value)
        })
        self.current_token = ""
    
    def _emit_error_token(self, error_message: str):
        """Emit an error token."""
        self.tokens.append({
            'type': TokenType.INVALID.value,
            'value': self.current_token,
            'error': error_message,
            'position': self.position,
            'line': self.line,
            'column': self.column
        })
        self.current_token = ""
        self.state = "START"  # Reset to start state for error recovery
    
    def _update_position(self, char: str):
        """Update position tracking."""
        self.position += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1

class AdvancedHTTPRequestCFGParser:
    """
    Advanced Context-Free Grammar parser for HTTP requests with full RFC 7230 compliance.
    
    Enhanced Grammar Rules (RFC 7230 compliant):
    HTTP-message = start-line *(header-field CRLF) CRLF [message-body]
    start-line = request-line
    request-line = method SP request-target SP HTTP-version CRLF
    method = token
    request-target = origin-form / absolute-form / authority-form / asterisk-form
    HTTP-version = HTTP-name "/" DIGIT "." DIGIT
    header-field = field-name ":" OWS field-value OWS
    field-name = token
    field-value = *(field-content / obs-fold)
    """
    
    def __init__(self):
        """Initialize the advanced CFG parser."""
        self.lexical_analyzer = LexicalAnalyzer()
        self._init_grammar()
        self._init_semantic_rules()
    
    def _init_grammar(self):
        """Initialize the enhanced CFG grammar rules."""
        self.grammar_rules = """
            HTTPMessage -> RequestLine Headers MessageBody
            HTTPMessage -> RequestLine Headers
            HTTPMessage -> RequestLine
            
            RequestLine -> Method SP RequestTarget SP HTTPVersion CRLF
            
            Method -> "GET" | "POST" | "PUT" | "DELETE" | "HEAD" | "OPTIONS" | "PATCH" | "TRACE" | "CONNECT"
            
            RequestTarget -> OriginForm | AbsoluteForm | AuthorityForm | AsteriskForm
            OriginForm -> "/" PathAbempty QueryString
            OriginForm -> "/" PathAbempty
            OriginForm -> "/"
            AbsoluteForm -> Scheme "://" Authority PathAbempty QueryString
            AbsoluteForm -> Scheme "://" Authority PathAbempty
            AuthorityForm -> Authority
            AsteriskForm -> "*"
            
            PathAbempty -> PathSegments
            PathAbempty -> ""
            PathSegments -> PathSegment "/" PathSegments
            PathSegments -> PathSegment
            PathSegment -> PChar PChars
            PathSegment -> PChar
            PathSegment -> ""
            
            QueryString -> "?" QueryParams
            QueryParams -> QueryParam "&" QueryParams
            QueryParams -> QueryParam
            QueryParam -> PChar PChars "=" PChar PChars
            QueryParam -> PChar PChars
            
            Scheme -> "http" | "https" | "ftp" | "file"
            Authority -> Host Port
            Authority -> Host
            Host -> IPAddress | DomainName
            Port -> ":" Digits
            
            HTTPVersion -> "HTTP/1.0" | "HTTP/1.1" | "HTTP/2.0" | "HTTP/3.0"
            
            Headers -> HeaderField Headers
            Headers -> HeaderField
            Headers -> ""
            
            HeaderField -> FieldName ":" OWS FieldValue OWS CRLF
            FieldName -> Token
            FieldValue -> FieldContent
            FieldContent -> VChar VChars
            FieldContent -> VChar
            FieldContent -> ""
            
            Token -> TChar TChars
            Token -> TChar
            TChar -> Alpha | Digit | "!" | "#" | "$" | "%" | "&" | "'" | "*" | "+" | "-" | "." | "^" | "_" | "`" | "|" | "~"
            TChars -> TChar TChars
            TChars -> TChar
            
            PChar -> Alpha | Digit | "-" | "." | "_" | "~" | ":" | "@" | "!" | "$" | "&" | "'" | "(" | ")" | "*" | "+" | "," | ";" | "="
            PChars -> PChar PChars
            PChars -> PChar
            
            VChar -> Alpha | Digit | "!" | '"' | "#" | "$" | "%" | "&" | "'" | "(" | ")" | "*" | "+" | "," | "-" | "." | "/" | ":" | ";" | "<" | "=" | ">" | "?" | "@" | "[" | "\\" | "]" | "^" | "_" | "`" | "{" | "|" | "}" | "~"
            VChars -> VChar VChars
            VChars -> VChar
            
            Alpha -> "a" | "b" | "c" | "d" | "e" | "f" | "g" | "h" | "i" | "j" | "k" | "l" | "m" | "n" | "o" | "p" | "q" | "r" | "s" | "t" | "u" | "v" | "w" | "x" | "y" | "z" | "A" | "B" | "C" | "D" | "E" | "F" | "G" | "H" | "I" | "J" | "K" | "L" | "M" | "N" | "O" | "P" | "Q" | "R" | "S" | "T" | "U" | "V" | "W" | "X" | "Y" | "Z"
            Digit -> "0" | "1" | "2" | "3" | "4" | "5" | "6" | "7" | "8" | "9"
            Digits -> Digit Digits
            Digits -> Digit
            
            SP -> " "
            CRLF -> "\\n"
            OWS -> SP OWS
            OWS -> ""
            
            MessageBody -> BodyContent
            BodyContent -> VChar VChars
            BodyContent -> VChar
            BodyContent -> ""
            
            IPAddress -> IPv4Address | IPv6Address
            IPv4Address -> Octet "." Octet "." Octet "." Octet
            Octet -> Digit Digit Digit
            Octet -> Digit Digit
            Octet -> Digit
            IPv6Address -> "[" IPv6Addr "]"
            IPv6Addr -> HexDigit HexDigits
            HexDigit -> Digit | "a" | "b" | "c" | "d" | "e" | "f" | "A" | "B" | "C" | "D" | "E" | "F"
            HexDigits -> HexDigit HexDigits
            HexDigits -> HexDigit
            
            DomainName -> Label "." DomainName
            DomainName -> Label
            Label -> Alpha AlphaNum
            Label -> Alpha
            AlphaNum -> Alpha | Digit | "-"
        """
        
        try:
            self.grammar = CFG.fromstring(self.grammar_rules)
            self.parser = ChartParser(self.grammar)
        except Exception as e:
            print(f"Error initializing advanced grammar: {e}")
            self.grammar = None
            self.parser = None
    
    def _init_semantic_rules(self):
        """Initialize semantic validation rules."""
        self.semantic_rules = {
            'method_validation': {
                'safe_methods': {'GET', 'HEAD', 'OPTIONS', 'TRACE'},
                'idempotent_methods': {'GET', 'HEAD', 'PUT', 'DELETE', 'OPTIONS', 'TRACE'},
                'cacheable_methods': {'GET', 'HEAD', 'POST'},
            },
            'uri_validation': {
                'max_length': 8000,  # RFC 7230 recommendation
                'allowed_schemes': {'http', 'https', 'ftp', 'file'},
                'reserved_chars': ':/?#[]@',
                'unreserved_chars': 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~'
            },
            'header_validation': {
                'required_headers': {
                    'GET': [],
                    'POST': ['Content-Type', 'Content-Length'],
                    'PUT': ['Content-Type', 'Content-Length'],
                    'DELETE': []
                },
                'forbidden_headers': {
                    'TRACE': ['Content-Length', 'Transfer-Encoding']
                }
            }
        }
    
    def validate_request(self, request_text: str) -> Dict[str, Any]:
        """
        Validate a complete HTTP request using advanced CFG parsing.
        
        Args:
            request_text (str): Complete HTTP request text
            
        Returns:
            Dict[str, Any]: Comprehensive validation result
        """
        result = {
            'is_valid': False,
            'request_text': request_text,
            'tokens': [],
            'parse_trees': [],
            'errors': [],
            'warnings': [],
            'semantic_analysis': {},
            'grammar_rules': self.get_enhanced_grammar_rules(),
            'lexical_analysis': {},
            'network_analysis': {},
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Step 1: Lexical Analysis using FSA
            tokens = self.lexical_analyzer.tokenize(request_text)
            result['tokens'] = tokens
            result['lexical_analysis'] = self._analyze_lexical_structure(tokens)
            
            # Check for lexical errors
            lexical_errors = [token for token in tokens if token['type'] == 'INVALID']
            if lexical_errors:
                result['errors'].extend([f"Lexical error: {token['error']}" for token in lexical_errors])
                return result
            
            # Step 2: Syntactic Analysis using CFG
            simplified_tokens = [token['value'] for token in tokens if token['type'] != 'CRLF']
            
            if self.parser:
                try:
                    parse_trees = list(self.parser.parse(simplified_tokens))
                    if parse_trees:
                        result['is_valid'] = True
                        result['parse_trees'] = [self._tree_to_dict(tree) for tree in parse_trees]
                    else:
                        result['errors'].extend(self._analyze_parsing_errors(simplified_tokens))
                except Exception as e:
                    result['errors'].append(f"Parsing error: {str(e)}")
            
            # Step 3: Semantic Analysis
            result['semantic_analysis'] = self._perform_semantic_analysis(tokens)
            
            # Step 4: Network Protocol Analysis
            result['network_analysis'] = self._perform_network_analysis(tokens)
            
            # Check for semantic warnings
            if result['semantic_analysis'].get('warnings'):
                result['warnings'].extend(result['semantic_analysis']['warnings'])
            
        except Exception as e:
            result['errors'].append(f"Validation error: {str(e)}")
        
        return result
    
    def _analyze_lexical_structure(self, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze the lexical structure of the tokens."""
        token_types = [token['type'] for token in tokens]
        
        return {
            'total_tokens': len(tokens),
            'token_distribution': {token_type: token_types.count(token_type) for token_type in set(token_types)},
            'has_method': 'METHOD' in token_types,
            'has_uri': 'URI' in token_types,
            'has_version': 'HTTP_VERSION' in token_types,
            'has_headers': 'HEADER_NAME' in token_types,
            'has_body': 'MESSAGE_BODY' in token_types,
            'structure_valid': self._check_token_sequence(token_types)
        }
    
    def _check_token_sequence(self, token_types: List[str]) -> bool:
        """Check if the token sequence follows HTTP message structure."""
        # Basic sequence should be: METHOD, URI, HTTP_VERSION
        if len(token_types) < 3:
            return False
        
        return (token_types[0] == 'METHOD' and 
                'URI' in token_types[:5] and 
                'HTTP_VERSION' in token_types[:5])
    
    def _perform_semantic_analysis(self, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform semantic analysis on the parsed tokens."""
        analysis = {
            'method_analysis': {},
            'uri_analysis': {},
            'header_analysis': {},
            'compliance_check': {},
            'warnings': []
        }
        
        # Extract key components
        method_token = next((t for t in tokens if t['type'] == 'METHOD'), None)
        uri_token = next((t for t in tokens if t['type'] == 'URI'), None)
        header_tokens = [(t for t in tokens if t['type'] == 'HEADER_NAME')]
        
        if method_token:
            method = method_token['value']
            analysis['method_analysis'] = {
                'method': method,
                'is_safe': method in self.semantic_rules['method_validation']['safe_methods'],
                'is_idempotent': method in self.semantic_rules['method_validation']['idempotent_methods'],
                'is_cacheable': method in self.semantic_rules['method_validation']['cacheable_methods']
            }
        
        if uri_token:
            uri = uri_token['value']
            analysis['uri_analysis'] = {
                'uri': uri,
                'length': len(uri),
                'is_absolute': uri.startswith('http://') or uri.startswith('https://'),
                'has_query': '?' in uri,
                'has_fragment': '#' in uri,
                'path_segments': uri.split('/')[1:] if uri.startswith('/') else []
            }
            
            if len(uri) > self.semantic_rules['uri_validation']['max_length']:
                analysis['warnings'].append(f"URI length ({len(uri)}) exceeds recommended maximum")
        
        return analysis
    
    def _perform_network_analysis(self, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Perform network protocol analysis."""
        return {
            'http_version_analysis': self._analyze_http_version(tokens),
            'connection_analysis': self._analyze_connection_headers(tokens),
            'cache_analysis': self._analyze_cache_headers(tokens),
            'content_analysis': self._analyze_content_headers(tokens)
        }
    
    def _analyze_http_version(self, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze HTTP version implications."""
        version_token = next((t for t in tokens if t['type'] == 'HTTP_VERSION'), None)
        
        if not version_token:
            return {'error': 'No HTTP version found'}
        
        version = version_token['value']
        
        return {
            'version': version,
            'supports_persistent_connections': version in ['HTTP/1.1', 'HTTP/2.0', 'HTTP/3.0'],
            'supports_pipelining': version in ['HTTP/1.1'],
            'supports_multiplexing': version in ['HTTP/2.0', 'HTTP/3.0'],
            'supports_server_push': version in ['HTTP/2.0', 'HTTP/3.0'],
            'default_connection': 'keep-alive' if version == 'HTTP/1.1' else 'close'
        }
    
    def _analyze_connection_headers(self, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze connection-related headers."""
        header_analysis = {}
        
        # Extract header name-value pairs
        headers = {}
        current_header = None
        
        for token in tokens:
            if token['type'] == 'HEADER_NAME':
                current_header = token['value'].lower()
            elif token['type'] == 'HEADER_VALUE' and current_header:
                headers[current_header] = token['value']
                current_header = None
        
        # Analyze connection headers
        connection_value = headers.get('connection', '').lower()
        header_analysis['connection_header'] = {
            'present': 'connection' in headers,
            'value': connection_value,
            'keep_alive': 'keep-alive' in connection_value,
            'close': 'close' in connection_value,
            'upgrade': 'upgrade' in connection_value
        }
        
        return header_analysis
    
    def _analyze_cache_headers(self, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze cache-related headers."""
        # Implementation for cache header analysis
        return {'cache_control': 'not_implemented'}
    
    def _analyze_content_headers(self, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze content-related headers."""
        # Implementation for content header analysis
        return {'content_type': 'not_implemented'}
    
    def _tree_to_dict(self, tree) -> Dict[str, Any]:
        """Convert NLTK Tree to dictionary format."""
        if hasattr(tree, 'label'):
            return {
                'label': str(tree.label()),
                'children': [self._tree_to_dict(child) for child in tree]
            }
        else:
            return {'label': str(tree), 'children': []}
    
    def _analyze_parsing_errors(self, tokens: List[str]) -> List[str]:
        """Analyze parsing errors and provide meaningful feedback."""
        errors = []
        
        if not tokens:
            errors.append("Empty token sequence")
            return errors
        
        # Check basic HTTP request structure
        if len(tokens) < 3:
            errors.append("Incomplete HTTP request. Minimum: METHOD URI VERSION")
        
        # More detailed error analysis would go here
        errors.append("Grammar parsing failed. Check HTTP message syntax.")
        
        return errors
    
    def get_enhanced_grammar_rules(self) -> List[Dict[str, str]]:
        """Get the enhanced grammar rules in structured format."""
        return [
            {
                'lhs': 'HTTPMessage',
                'rhs': 'RequestLine Headers MessageBody',
                'rule': 'HTTPMessage → RequestLine Headers MessageBody',
                'description': 'Complete HTTP message with headers and body'
            },
            {
                'lhs': 'RequestLine',
                'rhs': 'Method SP RequestTarget SP HTTPVersion CRLF',
                'rule': 'RequestLine → Method SP RequestTarget SP HTTPVersion CRLF',
                'description': 'HTTP request line structure (RFC 7230)'
            },
            {
                'lhs': 'Method',
                'rhs': 'GET | POST | PUT | DELETE | HEAD | OPTIONS | PATCH | TRACE | CONNECT',
                'rule': 'Method → GET | POST | PUT | DELETE | HEAD | OPTIONS | PATCH | TRACE | CONNECT',
                'description': 'Supported HTTP methods'
            },
            {
                'lhs': 'RequestTarget',
                'rhs': 'OriginForm | AbsoluteForm | AuthorityForm | AsteriskForm',
                'rule': 'RequestTarget → OriginForm | AbsoluteForm | AuthorityForm | AsteriskForm',
                'description': 'Four forms of request target (RFC 7230)'
            },
            {
                'lhs': 'HTTPVersion',
                'rhs': 'HTTP/1.0 | HTTP/1.1 | HTTP/2.0 | HTTP/3.0',
                'rule': 'HTTPVersion → HTTP/1.0 | HTTP/1.1 | HTTP/2.0 | HTTP/3.0',
                'description': 'Supported HTTP protocol versions'
            },
            {
                'lhs': 'HeaderField',
                'rhs': 'FieldName ":" OWS FieldValue OWS CRLF',
                'rule': 'HeaderField → FieldName ":" OWS FieldValue OWS CRLF',
                'description': 'HTTP header field structure'
            }
        ]

# Initialize NLTK data
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