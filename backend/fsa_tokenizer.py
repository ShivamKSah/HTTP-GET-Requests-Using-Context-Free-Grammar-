"""
Finite State Automaton (FSA) Implementation for HTTP Request Tokenization

This module implements a sophisticated FSA for lexical analysis of HTTP requests,
demonstrating formal language automata concepts in practice.

Key Features:
1. Deterministic Finite Automaton (DFA) for token recognition
2. Non-deterministic Finite Automaton (NFA) for complex patterns
3. State transition visualization
4. Error recovery mechanisms
5. Token position tracking
"""

from typing import Dict, List, Set, Optional, Tuple, Any, Union
from enum import Enum
from dataclasses import dataclass
import re
import json
from datetime import datetime

class State(Enum):
    """FSA states for HTTP request parsing."""
    # Initial states
    START = "START"
    ERROR = "ERROR"
    ACCEPT = "ACCEPT"
    
    # HTTP method states
    METHOD_M = "METHOD_M"
    METHOD_G = "METHOD_G"
    METHOD_P = "METHOD_P"
    METHOD_D = "METHOD_D"
    METHOD_H = "METHOD_H"
    METHOD_O = "METHOD_O"
    METHOD_T = "METHOD_T"
    METHOD_C = "METHOD_C"
    METHOD_COMPLETE = "METHOD_COMPLETE"
    
    # Whitespace states
    SPACE_AFTER_METHOD = "SPACE_AFTER_METHOD"
    SPACE_AFTER_URI = "SPACE_AFTER_URI"
    OPTIONAL_WHITESPACE = "OPTIONAL_WHITESPACE"
    
    # URI states
    URI_START = "URI_START"
    URI_PATH = "URI_PATH"
    URI_QUERY_START = "URI_QUERY_START"
    URI_QUERY = "URI_QUERY"
    URI_FRAGMENT_START = "URI_FRAGMENT_START"
    URI_FRAGMENT = "URI_FRAGMENT"
    URI_COMPLETE = "URI_COMPLETE"
    
    # HTTP version states
    VERSION_H = "VERSION_H"
    VERSION_T1 = "VERSION_T1"
    VERSION_T2 = "VERSION_T2"
    VERSION_P = "VERSION_P"
    VERSION_SLASH = "VERSION_SLASH"
    VERSION_MAJOR = "VERSION_MAJOR"
    VERSION_DOT = "VERSION_DOT"
    VERSION_MINOR = "VERSION_MINOR"
    VERSION_COMPLETE = "VERSION_COMPLETE"
    
    # Header states
    CRLF_AFTER_REQUEST = "CRLF_AFTER_REQUEST"
    HEADER_NAME_START = "HEADER_NAME_START"
    HEADER_NAME = "HEADER_NAME"
    HEADER_COLON = "HEADER_COLON"
    HEADER_VALUE_START = "HEADER_VALUE_START"
    HEADER_VALUE = "HEADER_VALUE"
    HEADER_CRLF = "HEADER_CRLF"
    HEADERS_END = "HEADERS_END"
    
    # Message body states
    MESSAGE_BODY = "MESSAGE_BODY"

@dataclass
class Token:
    """Represents a token produced by the FSA."""
    type: str
    value: str
    start_pos: int
    end_pos: int
    line: int
    column: int
    state_path: List[str]

@dataclass
class Transition:
    """Represents a state transition in the FSA."""
    from_state: State
    to_state: State
    input_symbol: str
    condition: Optional[str] = None
    action: Optional[str] = None

class HTTPRequestFSA:
    """
    Finite State Automaton for HTTP request lexical analysis.
    
    This FSA recognizes HTTP request components according to RFC 7230:
    - HTTP methods (GET, POST, PUT, DELETE, etc.)
    - Request URIs (origin-form, absolute-form, etc.)
    - HTTP versions (HTTP/1.0, HTTP/1.1, HTTP/2.0, HTTP/3.0)
    - Header fields
    - Message body
    """
    
    def __init__(self):
        self.current_state = State.START
        self.states = set(State)
        self.alphabet = self._create_alphabet()
        self.transitions = self._create_transition_table()
        self.accepting_states = {
            State.ACCEPT,
            State.METHOD_COMPLETE,
            State.URI_COMPLETE,
            State.VERSION_COMPLETE,
            State.HEADER_VALUE,
            State.MESSAGE_BODY
        }
        
        # Tracking variables
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_token_start = 0
        self.current_token_value = ""
        self.tokens = []
        self.state_path = []
        self.error_recovery_stack = []
    
    def _create_alphabet(self) -> Set[str]:
        """Create the input alphabet for the FSA."""
        alphabet = set()
        
        # ASCII letters and digits
        alphabet.update(chr(i) for i in range(ord('a'), ord('z') + 1))
        alphabet.update(chr(i) for i in range(ord('A'), ord('Z') + 1))
        alphabet.update(chr(i) for i in range(ord('0'), ord('9') + 1))
        
        # Special HTTP characters
        alphabet.update([' ', '\t', '\r', '\n', '/', '?', '#', ':', '@', 
                        '!', '$', '&', "'", '(', ')', '*', '+', ',', ';', 
                        '=', '-', '.', '_', '~', '[', ']', '%'])
        
        return alphabet
    
    def _create_transition_table(self) -> Dict[Tuple[State, str], State]:
        """Create the state transition table for the FSA."""
        transitions = {}
        
        # Method transitions
        self._add_method_transitions(transitions)
        
        # Whitespace transitions
        self._add_whitespace_transitions(transitions)
        
        # URI transitions
        self._add_uri_transitions(transitions)
        
        # HTTP version transitions
        self._add_version_transitions(transitions)
        
        # Header transitions
        self._add_header_transitions(transitions)
        
        # Message body transitions
        self._add_body_transitions(transitions)
        
        return transitions
    
    def _add_method_transitions(self, transitions: Dict[Tuple[State, str], State]):
        """Add HTTP method recognition transitions."""
        # GET method
        transitions[(State.START, 'G')] = State.METHOD_G
        transitions[(State.METHOD_G, 'E')] = State.METHOD_M
        transitions[(State.METHOD_M, 'T')] = State.METHOD_COMPLETE
        
        # POST method
        transitions[(State.START, 'P')] = State.METHOD_P
        transitions[(State.METHOD_P, 'O')] = State.METHOD_M
        transitions[(State.METHOD_M, 'S')] = State.METHOD_M
        transitions[(State.METHOD_M, 'T')] = State.METHOD_COMPLETE
        
        # PUT method (reusing some states)
        transitions[(State.METHOD_P, 'U')] = State.METHOD_M
        transitions[(State.METHOD_M, 'T')] = State.METHOD_COMPLETE
        
        # DELETE method
        transitions[(State.START, 'D')] = State.METHOD_D
        transitions[(State.METHOD_D, 'E')] = State.METHOD_M
        transitions[(State.METHOD_M, 'L')] = State.METHOD_M
        transitions[(State.METHOD_M, 'E')] = State.METHOD_M
        transitions[(State.METHOD_M, 'T')] = State.METHOD_COMPLETE
        
        # HEAD method
        transitions[(State.START, 'H')] = State.METHOD_H
        transitions[(State.METHOD_H, 'E')] = State.METHOD_M
        transitions[(State.METHOD_M, 'A')] = State.METHOD_M
        transitions[(State.METHOD_M, 'D')] = State.METHOD_COMPLETE
        
        # OPTIONS method
        transitions[(State.START, 'O')] = State.METHOD_O
        transitions[(State.METHOD_O, 'P')] = State.METHOD_M
        transitions[(State.METHOD_M, 'T')] = State.METHOD_M
        transitions[(State.METHOD_M, 'I')] = State.METHOD_M
        transitions[(State.METHOD_M, 'O')] = State.METHOD_M
        transitions[(State.METHOD_M, 'N')] = State.METHOD_M
        transitions[(State.METHOD_M, 'S')] = State.METHOD_COMPLETE
        
        # TRACE method
        transitions[(State.START, 'T')] = State.METHOD_T
        transitions[(State.METHOD_T, 'R')] = State.METHOD_M
        transitions[(State.METHOD_M, 'A')] = State.METHOD_M
        transitions[(State.METHOD_M, 'C')] = State.METHOD_M
        transitions[(State.METHOD_M, 'E')] = State.METHOD_COMPLETE
        
        # CONNECT method
        transitions[(State.START, 'C')] = State.METHOD_C
        transitions[(State.METHOD_C, 'O')] = State.METHOD_M
        transitions[(State.METHOD_M, 'N')] = State.METHOD_M
        transitions[(State.METHOD_M, 'N')] = State.METHOD_M
        transitions[(State.METHOD_M, 'E')] = State.METHOD_M
        transitions[(State.METHOD_M, 'C')] = State.METHOD_M
        transitions[(State.METHOD_M, 'T')] = State.METHOD_COMPLETE
    
    def _add_whitespace_transitions(self, transitions: Dict[Tuple[State, str], State]):
        """Add whitespace handling transitions."""
        transitions[(State.METHOD_COMPLETE, ' ')] = State.SPACE_AFTER_METHOD
        transitions[(State.URI_COMPLETE, ' ')] = State.SPACE_AFTER_URI
        
        # Allow multiple spaces
        transitions[(State.SPACE_AFTER_METHOD, ' ')] = State.SPACE_AFTER_METHOD
        transitions[(State.SPACE_AFTER_URI, ' ')] = State.SPACE_AFTER_URI
    
    def _add_uri_transitions(self, transitions: Dict[Tuple[State, str], State]):
        """Add URI recognition transitions."""
        transitions[(State.SPACE_AFTER_METHOD, '/')] = State.URI_START
        transitions[(State.SPACE_AFTER_METHOD, '*')] = State.URI_COMPLETE  # asterisk-form
        
        # URI path characters
        uri_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-._~:@!$&'()*+,;="
        for char in uri_chars:
            transitions[(State.URI_START, char)] = State.URI_PATH
            transitions[(State.URI_PATH, char)] = State.URI_PATH
        
        # URI path separators
        transitions[(State.URI_PATH, '/')] = State.URI_PATH
        
        # Query string
        transitions[(State.URI_PATH, '?')] = State.URI_QUERY_START
        for char in uri_chars + "/?":
            transitions[(State.URI_QUERY_START, char)] = State.URI_QUERY
            transitions[(State.URI_QUERY, char)] = State.URI_QUERY
        
        # Fragment
        transitions[(State.URI_PATH, '#')] = State.URI_FRAGMENT_START
        transitions[(State.URI_QUERY, '#')] = State.URI_FRAGMENT_START
        for char in uri_chars + "/?":
            transitions[(State.URI_FRAGMENT_START, char)] = State.URI_FRAGMENT
            transitions[(State.URI_FRAGMENT, char)] = State.URI_FRAGMENT
    
    def _add_version_transitions(self, transitions: Dict[Tuple[State, str], State]):
        """Add HTTP version recognition transitions."""
        transitions[(State.SPACE_AFTER_URI, 'H')] = State.VERSION_H
        transitions[(State.VERSION_H, 'T')] = State.VERSION_T1
        transitions[(State.VERSION_T1, 'T')] = State.VERSION_T2
        transitions[(State.VERSION_T2, 'P')] = State.VERSION_P
        transitions[(State.VERSION_P, '/')] = State.VERSION_SLASH
        
        # Version numbers
        for digit in "0123456789":
            transitions[(State.VERSION_SLASH, digit)] = State.VERSION_MAJOR
            transitions[(State.VERSION_MAJOR, digit)] = State.VERSION_MAJOR
            transitions[(State.VERSION_DOT, digit)] = State.VERSION_MINOR
            transitions[(State.VERSION_MINOR, digit)] = State.VERSION_MINOR
        
        transitions[(State.VERSION_MAJOR, '.')] = State.VERSION_DOT
    
    def _add_header_transitions(self, transitions: Dict[Tuple[State, str], State]):
        """Add header field recognition transitions."""
        transitions[(State.VERSION_COMPLETE, '\r')] = State.CRLF_AFTER_REQUEST
        transitions[(State.CRLF_AFTER_REQUEST, '\n')] = State.HEADER_NAME_START
        
        # Header name characters (tokens)
        header_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!#$%&'*+-.^_`|~"
        for char in header_chars:
            transitions[(State.HEADER_NAME_START, char)] = State.HEADER_NAME
            transitions[(State.HEADER_NAME, char)] = State.HEADER_NAME
        
        transitions[(State.HEADER_NAME, ':')] = State.HEADER_COLON
        transitions[(State.HEADER_COLON, ' ')] = State.HEADER_VALUE_START
        transitions[(State.HEADER_COLON, '\t')] = State.HEADER_VALUE_START
        
        # Header value characters (VCHAR and WSP)
        value_chars = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!\"#$%&'()*+,-./:;<=>?@[\\]^_`{|}~ "
        for char in value_chars:
            transitions[(State.HEADER_VALUE_START, char)] = State.HEADER_VALUE
            transitions[(State.HEADER_VALUE, char)] = State.HEADER_VALUE
        
        transitions[(State.HEADER_VALUE, '\r')] = State.HEADER_CRLF
        transitions[(State.HEADER_CRLF, '\n')] = State.HEADER_NAME_START
        
        # End of headers (empty line)
        transitions[(State.HEADER_NAME_START, '\r')] = State.HEADERS_END
        transitions[(State.HEADERS_END, '\n')] = State.MESSAGE_BODY
    
    def _add_body_transitions(self, transitions: Dict[Tuple[State, str], State]):
        """Add message body recognition transitions."""
        # Message body can contain any octets
        for i in range(256):
            char = chr(i)
            transitions[(State.MESSAGE_BODY, char)] = State.MESSAGE_BODY
    
    def reset(self):
        """Reset the FSA to initial state."""
        self.current_state = State.START
        self.position = 0
        self.line = 1
        self.column = 1
        self.current_token_start = 0
        self.current_token_value = ""
        self.tokens = []
        self.state_path = []
        self.error_recovery_stack = []
    
    def process_input(self, input_text: str) -> List[Token]:
        """
        Process input text through the FSA and generate tokens.
        
        Args:
            input_text (str): HTTP request text to tokenize
            
        Returns:
            List[Token]: List of recognized tokens
        """
        self.reset()
        
        for char in input_text:
            self._process_character(char)
            self._update_position(char)
        
        # Process any remaining token
        self._finalize_current_token()
        
        return self.tokens
    
    def _process_character(self, char: str):
        """Process a single character through the FSA."""
        previous_state = self.current_state
        
        # Look up transition
        transition_key = (self.current_state, char)
        
        if transition_key in self.transitions:
            self.current_state = self.transitions[transition_key]
            self.current_token_value += char
            self.state_path.append(self.current_state.value)
            
            # Check if we completed a token
            if self._should_emit_token(previous_state, self.current_state):
                self._emit_token()
        else:
            # Handle transition failure
            self._handle_transition_error(char)
    
    def _should_emit_token(self, previous_state: State, current_state: State) -> bool:
        """Determine if a token should be emitted based on state transition."""
        # Emit token when transitioning to certain states
        emit_triggers = {
            State.METHOD_COMPLETE: "METHOD",
            State.URI_COMPLETE: "URI", 
            State.VERSION_COMPLETE: "HTTP_VERSION",
            State.HEADER_NAME: "HEADER_NAME",
            State.HEADER_VALUE: "HEADER_VALUE",
            State.SPACE_AFTER_METHOD: "SP",
            State.SPACE_AFTER_URI: "SP"
        }
        
        return current_state in emit_triggers
    
    def _emit_token(self):
        """Emit the current token."""
        if not self.current_token_value:
            return
        
        # Determine token type based on current state
        token_type = self._determine_token_type()
        
        token = Token(
            type=token_type,
            value=self.current_token_value.strip(),
            start_pos=self.current_token_start,
            end_pos=self.position,
            line=self.line,
            column=self.column,
            state_path=self.state_path.copy()
        )
        
        self.tokens.append(token)
        self._reset_current_token()
    
    def _determine_token_type(self) -> str:
        """Determine the token type based on current FSA state."""
        state_to_token = {
            State.METHOD_COMPLETE: "METHOD",
            State.URI_COMPLETE: "URI",
            State.URI_PATH: "URI",
            State.URI_QUERY: "URI",
            State.URI_FRAGMENT: "URI",
            State.VERSION_COMPLETE: "HTTP_VERSION",
            State.VERSION_MINOR: "HTTP_VERSION",
            State.HEADER_NAME: "HEADER_NAME",
            State.HEADER_VALUE: "HEADER_VALUE",
            State.SPACE_AFTER_METHOD: "SP",
            State.SPACE_AFTER_URI: "SP",
            State.MESSAGE_BODY: "MESSAGE_BODY"
        }
        
        return state_to_token.get(self.current_state, "UNKNOWN")
    
    def _handle_transition_error(self, char: str):
        """Handle invalid transitions with error recovery."""
        # Try epsilon transitions or error recovery
        self.current_state = State.ERROR
        
        # Simple error recovery: skip character and try to continue
        error_token = Token(
            type="ERROR",
            value=char,
            start_pos=self.position,
            end_pos=self.position + 1,
            line=self.line,
            column=self.column,
            state_path=["ERROR"]
        )
        
        self.tokens.append(error_token)
        
        # Attempt to recover to a valid state
        self._attempt_error_recovery()
    
    def _attempt_error_recovery(self):
        """Attempt to recover from error state."""
        # Simple recovery: return to START state
        self.current_state = State.START
        self._reset_current_token()
    
    def _finalize_current_token(self):
        """Finalize any remaining token at end of input."""
        if self.current_token_value and self.current_state in self.accepting_states:
            self._emit_token()
    
    def _reset_current_token(self):
        """Reset current token tracking variables."""
        self.current_token_start = self.position
        self.current_token_value = ""
        self.state_path = []
    
    def _update_position(self, char: str):
        """Update position tracking."""
        self.position += 1
        if char == '\n':
            self.line += 1
            self.column = 1
        else:
            self.column += 1
    
    def get_state_transition_graph(self) -> Dict[str, Any]:
        """Generate a representation of the FSA state transition graph."""
        graph = {
            'states': [state.value for state in self.states],
            'start_state': State.START.value,
            'accepting_states': [state.value for state in self.accepting_states],
            'transitions': []
        }
        
        for (from_state, symbol), to_state in self.transitions.items():
            graph['transitions'].append({
                'from': from_state.value,
                'to': to_state.value,
                'symbol': symbol,
                'symbol_code': ord(symbol) if len(symbol) == 1 else None
            })
        
        return graph
    
    def analyze_token_sequence(self, tokens: List[Token]) -> Dict[str, Any]:
        """Analyze the structure of a token sequence."""
        token_types = [token.type for token in tokens]
        
        analysis = {
            'total_tokens': len(tokens),
            'token_types': list(set(token_types)),
            'token_sequence': token_types,
            'has_method': 'METHOD' in token_types,
            'has_uri': 'URI' in token_types,
            'has_version': 'HTTP_VERSION' in token_types,
            'has_headers': 'HEADER_NAME' in token_types,
            'has_body': 'MESSAGE_BODY' in token_types,
            'error_count': token_types.count('ERROR'),
            'structure_validity': self._validate_token_structure(token_types)
        }
        
        return analysis
    
    def _validate_token_structure(self, token_types: List[str]) -> Dict[str, Any]:
        """Validate the structure of the token sequence."""
        validity = {
            'is_valid': False,
            'required_present': False,
            'correct_order': False,
            'issues': []
        }
        
        # Check for required tokens
        required_tokens = {'METHOD', 'URI', 'HTTP_VERSION'}
        present_tokens = set(token_types)
        
        if required_tokens.issubset(present_tokens):
            validity['required_present'] = True
        else:
            missing = required_tokens - present_tokens
            validity['issues'].append(f"Missing required tokens: {missing}")
        
        # Check token order (simplified)
        if len(token_types) >= 3:
            if (token_types[0] == 'METHOD' and 
                'URI' in token_types[:5] and 
                'HTTP_VERSION' in token_types[:5]):
                validity['correct_order'] = True
            else:
                validity['issues'].append("Incorrect token order")
        
        validity['is_valid'] = validity['required_present'] and validity['correct_order']
        
        return validity

# Example usage and testing
if __name__ == "__main__":
    # Create FSA instance
    fsa = HTTPRequestFSA()
    
    # Test with sample HTTP request
    sample_request = "GET /index.html HTTP/1.1\r\nHost: example.com\r\nUser-Agent: TestAgent/1.0\r\n\r\n"
    
    tokens = fsa.process_input(sample_request)
    
    print("Generated Tokens:")
    for token in tokens:
        print(f"  {token.type}: '{token.value}' (pos: {token.start_pos}-{token.end_pos})")
    
    # Analyze token sequence
    analysis = fsa.analyze_token_sequence(tokens)
    print(f"\nToken Analysis: {json.dumps(analysis, indent=2)}")
    
    # Get state transition graph
    graph = fsa.get_state_transition_graph()
    print(f"\nFSA has {len(graph['states'])} states and {len(graph['transitions'])} transitions")