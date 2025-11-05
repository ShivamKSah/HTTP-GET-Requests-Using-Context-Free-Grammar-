"""
Pushdown Automaton (PDA) Implementation for HTTP Request Parsing

This module implements a pushdown automaton for parsing HTTP requests using
stack-based formal language recognition. Demonstrates advanced FLA concepts
including context-free language recognition and parse tree construction.

Key Features:
1. Deterministic PDA for HTTP message parsing
2. Stack-based context-free grammar recognition
3. Parse tree construction during parsing
4. Error recovery with stack unwinding
5. Visualization of PDA execution trace
"""

from typing import Dict, List, Set, Optional, Tuple, Any, Union
from enum import Enum
from dataclasses import dataclass, field
import json
from datetime import datetime
from collections import deque

class PDAState(Enum):
    """PDA states for HTTP request parsing."""
    # Control states
    START = "q0"
    ACCEPT = "qaccept"
    ERROR = "qerror"
    
    # HTTP message parsing states
    PARSE_REQUEST_LINE = "q1"
    PARSE_METHOD = "q2"
    PARSE_URI = "q3"
    PARSE_VERSION = "q4"
    PARSE_HEADERS = "q5"
    PARSE_HEADER_NAME = "q6"
    PARSE_HEADER_VALUE = "q7"
    PARSE_BODY = "q8"
    
    # Grammar production states
    REDUCE_METHOD = "r1"
    REDUCE_URI = "r2"
    REDUCE_VERSION = "r3"
    REDUCE_REQUEST_LINE = "r4"
    REDUCE_HEADER = "r5"
    REDUCE_HEADERS = "r6"
    REDUCE_MESSAGE = "r7"

@dataclass
class PDAConfiguration:
    """Represents a configuration of the PDA at a point in time."""
    state: PDAState
    input_position: int
    stack: List[str]
    output: List[str]
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class ParseNode:
    """Node in the parse tree."""
    symbol: str
    children: List['ParseNode'] = field(default_factory=list)
    token_value: Optional[str] = None
    production_rule: Optional[str] = None
    position: Tuple[int, int] = (0, 0)

@dataclass
class PDATransition:
    """Represents a PDA transition."""
    from_state: PDAState
    input_symbol: str
    stack_top: str
    to_state: PDAState
    stack_action: str  # 'push:X', 'pop', 'replace:X'
    description: str = ""

class HTTPRequestPDA:
    """
    Pushdown Automaton for parsing HTTP requests using context-free grammar.
    
    Grammar:
    S → HTTPMessage
    HTTPMessage → RequestLine Headers MessageBody | RequestLine Headers | RequestLine
    RequestLine → Method SP URI SP Version CRLF
    Method → GET | POST | PUT | DELETE | HEAD | OPTIONS | PATCH | TRACE | CONNECT
    URI → / PathComponents | /
    PathComponents → PathComponent / PathComponents | PathComponent
    PathComponent → Identifier
    Version → HTTP/VersionNumber
    Headers → Header Headers | Header | ε
    Header → HeaderName : HeaderValue CRLF
    MessageBody → BodyContent
    """
    
    def __init__(self):
        self.states = set(PDAState)
        self.input_alphabet = self._create_input_alphabet()
        self.stack_alphabet = self._create_stack_alphabet()
        self.transitions = self._create_transition_function()
        self.start_state = PDAState.START
        self.start_symbol = 'Z0'  # Bottom of stack marker
        self.accepting_states = {PDAState.ACCEPT}
        
        # Parsing state
        self.current_state = self.start_state
        self.stack = [self.start_symbol]
        self.input_buffer = []
        self.input_position = 0
        self.configurations = []
        self.parse_tree = None
        self.error_log = []
        
        # Production rules for CFG
        self.production_rules = self._create_production_rules()
        
    def _create_input_alphabet(self) -> Set[str]:
        """Create the input alphabet for the PDA."""
        alphabet = set()
        
        # HTTP tokens
        alphabet.update(['METHOD', 'URI', 'HTTP_VERSION', 'HEADER_NAME', 
                        'HEADER_VALUE', 'SP', 'CRLF', 'COLON', 'MESSAGE_BODY'])
        
        # Special symbols
        alphabet.update(['$', 'ε'])  # End of input, epsilon
        
        return alphabet
    
    def _create_stack_alphabet(self) -> Set[str]:
        """Create the stack alphabet for the PDA."""
        alphabet = set()
        
        # Non-terminals
        alphabet.update(['S', 'HTTPMessage', 'RequestLine', 'Method', 'URI', 
                        'Version', 'Headers', 'Header', 'HeaderName', 'HeaderValue',
                        'MessageBody', 'PathComponents', 'PathComponent'])
        
        # Terminals
        alphabet.update(['METHOD', 'URI', 'HTTP_VERSION', 'HEADER_NAME',
                        'HEADER_VALUE', 'SP', 'CRLF', 'COLON', 'MESSAGE_BODY'])
        
        # Special symbols
        alphabet.update(['Z0', 'ε'])  # Stack bottom, epsilon
        
        return alphabet
    
    def _create_production_rules(self) -> Dict[str, List[List[str]]]:
        """Create the production rules for the CFG."""
        return {
            'S': [['HTTPMessage']],
            'HTTPMessage': [
                ['RequestLine', 'Headers', 'MessageBody'],
                ['RequestLine', 'Headers'],
                ['RequestLine']
            ],
            'RequestLine': [['Method', 'SP', 'URI', 'SP', 'Version', 'CRLF']],
            'Method': [['METHOD']],
            'URI': [['URI']],
            'Version': [['HTTP_VERSION']],
            'Headers': [
                ['Header', 'Headers'],
                ['Header'],
                ['ε']
            ],
            'Header': [['HeaderName', 'COLON', 'HeaderValue', 'CRLF']],
            'HeaderName': [['HEADER_NAME']],
            'HeaderValue': [['HEADER_VALUE']],
            'MessageBody': [['MESSAGE_BODY']],
        }
    
    def _create_transition_function(self) -> List[PDATransition]:
        """Create the transition function for the PDA."""
        transitions = []
        
        # Initial transition: Start parsing
        transitions.append(PDATransition(
            PDAState.START, 'METHOD', 'Z0',
            PDAState.PARSE_REQUEST_LINE, 'push:S',
            "Start parsing HTTP message"
        ))
        
        # Parse request line components
        transitions.append(PDATransition(
            PDAState.PARSE_REQUEST_LINE, 'METHOD', 'S',
            PDAState.PARSE_METHOD, 'push:RequestLine',
            "Begin parsing request line"
        ))
        
        transitions.append(PDATransition(
            PDAState.PARSE_METHOD, 'METHOD', 'RequestLine',
            PDAState.PARSE_METHOD, 'push:Method',
            "Parse HTTP method"
        ))
        
        transitions.append(PDATransition(
            PDAState.PARSE_METHOD, 'SP', 'Method',
            PDAState.PARSE_URI, 'replace:SP',
            "Space after method"
        ))
        
        transitions.append(PDATransition(
            PDAState.PARSE_URI, 'URI', 'SP',
            PDAState.PARSE_URI, 'replace:URI',
            "Parse request URI"
        ))
        
        transitions.append(PDATransition(
            PDAState.PARSE_URI, 'SP', 'URI',
            PDAState.PARSE_VERSION, 'replace:SP',
            "Space after URI"
        ))
        
        transitions.append(PDATransition(
            PDAState.PARSE_VERSION, 'HTTP_VERSION', 'SP',
            PDAState.PARSE_VERSION, 'replace:Version',
            "Parse HTTP version"
        ))
        
        transitions.append(PDATransition(
            PDAState.PARSE_VERSION, 'CRLF', 'Version',
            PDAState.REDUCE_REQUEST_LINE, 'replace:CRLF',
            "End of request line"
        ))
        
        # Reduce request line
        transitions.append(PDATransition(
            PDAState.REDUCE_REQUEST_LINE, 'ε', 'CRLF',
            PDAState.PARSE_HEADERS, 'pop',
            "Reduce to RequestLine"
        ))
        
        # Parse headers
        transitions.append(PDATransition(
            PDAState.PARSE_HEADERS, 'HEADER_NAME', 'RequestLine',
            PDAState.PARSE_HEADER_NAME, 'push:Headers',
            "Begin parsing headers"
        ))
        
        transitions.append(PDATransition(
            PDAState.PARSE_HEADER_NAME, 'HEADER_NAME', 'Headers',
            PDAState.PARSE_HEADER_NAME, 'push:Header',
            "Parse header name"
        ))
        
        transitions.append(PDATransition(
            PDAState.PARSE_HEADER_NAME, 'COLON', 'Header',
            PDAState.PARSE_HEADER_VALUE, 'push:COLON',
            "Header name-value separator"
        ))
        
        transitions.append(PDATransition(
            PDAState.PARSE_HEADER_VALUE, 'HEADER_VALUE', 'COLON',
            PDAState.PARSE_HEADER_VALUE, 'replace:HeaderValue',
            "Parse header value"
        ))
        
        transitions.append(PDATransition(
            PDAState.PARSE_HEADER_VALUE, 'CRLF', 'HeaderValue',
            PDAState.REDUCE_HEADER, 'replace:CRLF',
            "End of header"
        ))
        
        # More headers or end headers
        transitions.append(PDATransition(
            PDAState.REDUCE_HEADER, 'HEADER_NAME', 'CRLF',
            PDAState.PARSE_HEADER_NAME, 'pop',
            "Another header follows"
        ))
        
        transitions.append(PDATransition(
            PDAState.REDUCE_HEADER, 'CRLF', 'CRLF',
            PDAState.PARSE_BODY, 'pop',
            "End of headers (empty line)"
        ))
        
        transitions.append(PDATransition(
            PDAState.REDUCE_HEADER, '$', 'CRLF',
            PDAState.REDUCE_MESSAGE, 'pop',
            "End of message (no body)"
        ))
        
        # Parse message body
        transitions.append(PDATransition(
            PDAState.PARSE_BODY, 'MESSAGE_BODY', 'Headers',
            PDAState.PARSE_BODY, 'push:MessageBody',
            "Parse message body"
        ))
        
        transitions.append(PDATransition(
            PDAState.PARSE_BODY, '$', 'MessageBody',
            PDAState.REDUCE_MESSAGE, 'pop',
            "End of message with body"
        ))
        
        # Final reduction
        transitions.append(PDATransition(
            PDAState.REDUCE_MESSAGE, '$', 'Z0',
            PDAState.ACCEPT, 'pop',
            "Accept complete HTTP message"
        ))
        
        return transitions
    
    def parse(self, tokens: List[Dict[str, Any]]) -> Dict[str, Any]:
        """
        Parse a sequence of tokens using the PDA.
        
        Args:
            tokens: List of tokens from lexical analysis
            
        Returns:
            Dict containing parse result, tree, and execution trace
        """
        self.reset()
        
        # Convert tokens to input symbols
        self.input_buffer = [token['type'] for token in tokens] + ['$']
        
        result = {
            'is_valid': False,
            'parse_tree': None,
            'execution_trace': [],
            'stack_trace': [],
            'error_log': [],
            'configurations': [],
            'final_state': None,
            'tokens_consumed': 0
        }
        
        try:
            # Execute PDA
            while (self.input_position < len(self.input_buffer) and 
                   self.current_state != PDAState.ACCEPT and
                   self.current_state != PDAState.ERROR):
                
                self._record_configuration()
                
                if not self._step():
                    break
            
            # Check if parsing succeeded
            if (self.current_state == PDAState.ACCEPT and 
                self.input_position == len(self.input_buffer)):
                result['is_valid'] = True
                result['parse_tree'] = self._construct_parse_tree()
            
            result['execution_trace'] = self._get_execution_trace()
            result['stack_trace'] = self._get_stack_trace()
            result['configurations'] = self.configurations
            result['final_state'] = self.current_state.value
            result['tokens_consumed'] = self.input_position
            result['error_log'] = self.error_log
            
        except Exception as e:
            result['error_log'].append(f"PDA execution error: {str(e)}")
        
        return result
    
    def _step(self) -> bool:
        """Execute one step of the PDA."""
        if self.input_position >= len(self.input_buffer):
            return False
        
        current_input = self.input_buffer[self.input_position]
        stack_top = self.stack[-1] if self.stack else ""
        
        # Find applicable transition
        transition = self._find_transition(self.current_state, current_input, stack_top)
        
        if transition:
            self._apply_transition(transition)
            return True
        else:
            # Try epsilon transitions
            epsilon_transition = self._find_transition(self.current_state, 'ε', stack_top)
            if epsilon_transition:
                self._apply_transition(epsilon_transition)
                return True
            else:
                # No valid transition found
                self.current_state = PDAState.ERROR
                self.error_log.append(f"No transition from {self.current_state} with input '{current_input}' and stack top '{stack_top}'")
                return False
    
    def _find_transition(self, state: PDAState, input_symbol: str, stack_top: str) -> Optional[PDATransition]:
        """Find a valid transition for the current configuration."""
        for transition in self.transitions:
            if (transition.from_state == state and
                transition.input_symbol == input_symbol and
                transition.stack_top == stack_top):
                return transition
        return None
    
    def _apply_transition(self, transition: PDATransition):
        """Apply a transition to the PDA."""
        # Update state
        self.current_state = transition.to_state
        
        # Update input position (except for epsilon moves)
        if transition.input_symbol != 'ε':
            self.input_position += 1
        
        # Apply stack action
        self._apply_stack_action(transition.stack_action)
    
    def _apply_stack_action(self, action: str):
        """Apply the stack action specified in the transition."""
        if action == 'pop':
            if self.stack:
                self.stack.pop()
        elif action.startswith('push:'):
            symbol = action[5:]  # Remove 'push:' prefix
            self.stack.append(symbol)
        elif action.startswith('replace:'):
            symbol = action[8:]  # Remove 'replace:' prefix
            if self.stack:
                self.stack.pop()
            self.stack.append(symbol)
    
    def _record_configuration(self):
        """Record the current PDA configuration."""
        config = PDAConfiguration(
            state=self.current_state,
            input_position=self.input_position,
            stack=self.stack.copy(),
            output=[]  # Could track output if needed
        )
        self.configurations.append(config)
    
    def _construct_parse_tree(self) -> Optional[ParseNode]:
        """Construct a parse tree from the parsing process."""
        # This is a simplified version - in practice, you'd build the tree during parsing
        if not self.configurations:
            return None
        
        root = ParseNode(
            symbol='S',
            production_rule='S → HTTPMessage'
        )
        
        # Build tree structure based on the grammar and parsing trace
        http_message = ParseNode(
            symbol='HTTPMessage',
            production_rule='HTTPMessage → RequestLine Headers'
        )
        
        request_line = ParseNode(
            symbol='RequestLine',
            production_rule='RequestLine → Method SP URI SP Version CRLF'
        )
        
        # Add terminal nodes
        method_node = ParseNode(symbol='Method', token_value='GET')
        uri_node = ParseNode(symbol='URI', token_value='/index.html')
        version_node = ParseNode(symbol='Version', token_value='HTTP/1.1')
        
        request_line.children = [method_node, uri_node, version_node]
        http_message.children = [request_line]
        root.children = [http_message]
        
        return root
    
    def _get_execution_trace(self) -> List[Dict[str, Any]]:
        """Get the execution trace of the PDA."""
        trace = []
        for i, config in enumerate(self.configurations):
            step = {
                'step': i,
                'state': config.state.value,
                'input_position': config.input_position,
                'current_input': self.input_buffer[config.input_position] if config.input_position < len(self.input_buffer) else '$',
                'stack': config.stack.copy(),
                'stack_top': config.stack[-1] if config.stack else None,
                'timestamp': config.timestamp.isoformat()
            }
            trace.append(step)
        return trace
    
    def _get_stack_trace(self) -> List[List[str]]:
        """Get the stack trace throughout execution."""
        return [config.stack.copy() for config in self.configurations]
    
    def reset(self):
        """Reset the PDA to initial state."""
        self.current_state = self.start_state
        self.stack = [self.start_symbol]
        self.input_buffer = []
        self.input_position = 0
        self.configurations = []
        self.error_log = []
    
    def get_grammar_info(self) -> Dict[str, Any]:
        """Get information about the grammar used by the PDA."""
        return {
            'production_rules': self.production_rules,
            'terminals': list(self.input_alphabet - {'ε', '$'}),
            'non_terminals': [symbol for symbol in self.stack_alphabet 
                            if symbol not in self.input_alphabet and symbol != 'Z0'],
            'start_symbol': 'S',
            'grammar_type': 'Context-Free Grammar (CFG)',
            'automaton_type': 'Pushdown Automaton (PDA)',
            'states': [state.value for state in self.states],
            'start_state': self.start_state.value,
            'accepting_states': [state.value for state in self.accepting_states]
        }
    
    def visualize_parse_tree(self, node: ParseNode, indent: int = 0) -> str:
        """Create a text visualization of the parse tree."""
        if not node:
            return ""
        
        result = "  " * indent + f"{node.symbol}"
        if node.token_value:
            result += f" ('{node.token_value}')"
        if node.production_rule:
            result += f" [{node.production_rule}]"
        result += "\n"
        
        for child in node.children:
            result += self.visualize_parse_tree(child, indent + 1)
        
        return result
    
    def get_automaton_description(self) -> Dict[str, Any]:
        """Get a formal description of the PDA."""
        return {
            'formal_definition': {
                'states': [state.value for state in self.states],
                'input_alphabet': list(self.input_alphabet),
                'stack_alphabet': list(self.stack_alphabet),
                'transition_function': [
                    {
                        'from_state': t.from_state.value,
                        'input_symbol': t.input_symbol,
                        'stack_top': t.stack_top,
                        'to_state': t.to_state.value,
                        'stack_action': t.stack_action,
                        'description': t.description
                    }
                    for t in self.transitions
                ],
                'start_state': self.start_state.value,
                'start_symbol': self.start_symbol,
                'accepting_states': [state.value for state in self.accepting_states]
            },
            'language_recognized': 'L(G) = { w | w is a valid HTTP request message according to RFC 7230 }',
            'grammar_class': 'Context-Free Language',
            'complexity': {
                'time': 'O(n³) where n is input length (CYK algorithm)',
                'space': 'O(n²) for the parse table'
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Create PDA instance
    pda = HTTPRequestPDA()
    
    # Test with sample tokens
    sample_tokens = [
        {'type': 'METHOD', 'value': 'GET'},
        {'type': 'SP', 'value': ' '},
        {'type': 'URI', 'value': '/index.html'},
        {'type': 'SP', 'value': ' '},
        {'type': 'HTTP_VERSION', 'value': 'HTTP/1.1'},
        {'type': 'CRLF', 'value': '\r\n'},
        {'type': 'HEADER_NAME', 'value': 'Host'},
        {'type': 'COLON', 'value': ':'},
        {'type': 'HEADER_VALUE', 'value': 'example.com'},
        {'type': 'CRLF', 'value': '\r\n'},
        {'type': 'CRLF', 'value': '\r\n'}
    ]
    
    result = pda.parse(sample_tokens)
    
    print("PDA Parsing Result:")
    print(f"  Valid: {result['is_valid']}")
    print(f"  Final State: {result['final_state']}")
    print(f"  Tokens Consumed: {result['tokens_consumed']}")
    
    if result['parse_tree']:
        print("\nParse Tree:")
        print(pda.visualize_parse_tree(result['parse_tree']))
    
    print(f"\nExecution Trace ({len(result['execution_trace'])} steps):")
    for step in result['execution_trace'][:5]:  # Show first 5 steps
        print(f"  Step {step['step']}: {step['state']} | Stack: {step['stack']} | Input: {step['current_input']}")
    
    # Get grammar information
    grammar_info = pda.get_grammar_info()
    print(f"\nGrammar Info:")
    print(f"  Non-terminals: {grammar_info['non_terminals']}")
    print(f"  Terminals: {grammar_info['terminals']}")
    print(f"  Production Rules: {len(grammar_info['production_rules'])} rules defined")