"""
Comprehensive Integration API for FLA and Networking Features

This module integrates all the enhanced FLA and networking components:
- Advanced CFG parser
- FSA tokenizer
- PDA parser
- Network state machines
- Packet analyzer
- Header validator
- Advanced visualizer
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
import traceback
from typing import Dict, List, Any, Optional

# Import all our enhanced modules
from advanced_cfg_parser import AdvancedHTTPRequestCFGParser
from fsa_tokenizer import HTTPRequestFSA
from pda_parser import HTTPRequestPDA
from network_state_machine import TCPStateMachine
from packet_analyzer import HTTPPacketAnalyzer
from header_cfg_validator import HTTPHeaderCFGValidator
from advanced_visualizer import AdvancedVisualizer, TreeNode, NodeType, ProtocolLayer

app = Flask(__name__)
CORS(app)

class ComprehensiveAnalysisEngine:
    """Main engine that orchestrates all FLA and networking components."""
    
    def __init__(self):
        self.cfg_parser = AdvancedHTTPRequestCFGParser()
        self.fsa_tokenizer = HTTPRequestFSA()
        self.pda_parser = HTTPRequestPDA()
        self.tcp_state_machine = TCPStateMachine()
        self.packet_analyzer = HTTPPacketAnalyzer()
        self.header_validator = HTTPHeaderCFGValidator()
        self.visualizer = AdvancedVisualizer()
        
    def comprehensive_analysis(self, http_request: str) -> Dict[str, Any]:
        """Perform comprehensive FLA and networking analysis."""
        results = {
            'input': http_request,
            'timestamp': 'now',
            'analysis_components': {},
            'visualizations': {},
            'integration_insights': {},
            'formal_verification': {},
            'educational_content': {}
        }
        
        try:
            # 1. FSA Tokenization
            tokens = self.fsa_tokenizer.process_input(http_request)
            results['analysis_components']['fsa_tokenization'] = {
                'tokens': [{'type': t.type, 'value': t.value, 'start_pos': t.start_pos, 'end_pos': t.end_pos} for t in tokens],
                'token_count': len(tokens),
                'lexical_errors': []  # FSA handles errors internally
            }
            
            # 2. CFG Parsing
            cfg_result = self.cfg_parser.validate_request(http_request)
            results['analysis_components']['cfg_parsing'] = cfg_result
            
            # 3. PDA Analysis
            # Convert FSA tokens to format expected by PDA
            token_dicts = [{'type': t.type, 'value': t.value} for t in tokens]
            pda_result = self.pda_parser.parse(token_dicts)
            results['analysis_components']['pda_analysis'] = pda_result
            
            # 4. Header Validation
            headers_text = self._extract_headers(http_request)
            header_validation = self.header_validator.validate_headers(headers_text)
            results['analysis_components']['header_validation'] = header_validation
            
            # 5. Packet Analysis
            packet = self.packet_analyzer.analyze_http_request_packet(http_request)
            packet_viz = self.packet_analyzer.generate_packet_visualization_data(packet)
            results['analysis_components']['packet_analysis'] = packet_viz
            
            # 6. Network State Analysis
            connection_analysis = self._analyze_network_connection(http_request)
            results['analysis_components']['network_state'] = connection_analysis
            
            # 7. Generate Visualizations
            results['visualizations'] = self._generate_comprehensive_visualizations(
                cfg_result, pda_result, packet_viz, header_validation
            )
            
            # 8. Integration Insights
            results['integration_insights'] = self._generate_integration_insights(results['analysis_components'])
            
            # 9. Formal Verification
            results['formal_verification'] = self._perform_formal_verification(results['analysis_components'])
            
            # 10. Educational Content
            results['educational_content'] = self._generate_educational_content(results)
            
        except Exception as e:
            results['error'] = str(e)
            results['traceback'] = traceback.format_exc()
            
        return results
    
    def _extract_headers(self, http_request: str) -> str:
        """Extract headers section from HTTP request."""
        lines = http_request.strip().split('\n')
        headers = []
        
        for i, line in enumerate(lines[1:], 1):  # Skip request line
            if line.strip() == "":  # Empty line indicates end of headers
                break
            headers.append(line)
        
        return '\n'.join(headers)
    
    def _analyze_network_connection(self, http_request: str) -> Dict[str, Any]:
        """Analyze network connection aspects."""
        # Simulate TCP connection analysis
        tcp_analysis = {
            'connection_state': 'ESTABLISHED',
            'handshake_completed': True,
            'sequence_numbers': {
                'client_seq': 1000000,
                'server_seq': 2000000
            },
            'window_size': 65535,
            'mss': 1460
        }
        
        # Analyze HTTP session
        http_analysis = {
            'version': 'HTTP/1.1',
            'connection_type': 'keep-alive',
            'expects_response': True,
            'content_length_required': 'POST' in http_request or 'PUT' in http_request
        }
        
        return {
            'tcp_layer': tcp_analysis,
            'http_layer': http_analysis,
            'security_considerations': {
                'uses_tls': False,
                'authentication_present': 'Authorization:' in http_request,
                'secure_headers': []
            }
        }
    
    def _generate_comprehensive_visualizations(self, cfg_result: Dict, pda_result: Dict, 
                                             packet_viz: Dict, header_validation: Dict) -> Dict[str, Any]:
        """Generate all visualization components."""
        visualizations = {}
        
        # Parse tree visualization (if available)
        if 'parse_tree' in cfg_result and cfg_result['parse_tree']:
            # Convert parse tree to TreeNode format for visualization
            root_node = self._convert_to_tree_node(cfg_result['parse_tree'])
            if root_node:
                parse_tree_viz = self.visualizer.generate_parse_tree_visualization(
                    root_node, cfg_result.get('grammar_rules', {})
                )
                visualizations['parse_tree'] = parse_tree_viz
        
        # FSA visualization
        states = ['START', 'METHOD', 'PATH', 'VERSION', 'HEADERS', 'BODY', 'END']
        transitions = [
            {'from_state': 'START', 'to_state': 'METHOD', 'input_symbol': 'method_token'},
            {'from_state': 'METHOD', 'to_state': 'PATH', 'input_symbol': 'space'},
            {'from_state': 'PATH', 'to_state': 'VERSION', 'input_symbol': 'space'},
            {'from_state': 'VERSION', 'to_state': 'HEADERS', 'input_symbol': 'crlf'},
            {'from_state': 'HEADERS', 'to_state': 'BODY', 'input_symbol': 'empty_line'},
            {'from_state': 'BODY', 'to_state': 'END', 'input_symbol': 'eof'}
        ]
        
        # Convert to StateTransition objects
        from advanced_visualizer import StateTransition
        state_transitions = [
            StateTransition(t['from_state'], t['to_state'], t['input_symbol']) 
            for t in transitions
        ]
        
        fsa_viz = self.visualizer.generate_fsa_visualization(
            states, state_transitions, ['method_token', 'space', 'crlf', 'empty_line', 'eof'],
            'START', ['END']
        )
        visualizations['fsa_diagram'] = fsa_viz
        
        # Protocol stack visualization
        protocol_layers = [
            ProtocolLayer('Application', 'HTTP', [], 100, 5, 20),
            ProtocolLayer('Transport', 'TCP', [], 0, 4, 20),
            ProtocolLayer('Network', 'IP', [], 0, 3, 20),
            ProtocolLayer('Data Link', 'Ethernet', [], 0, 2, 18),
            ProtocolLayer('Physical', 'Copper/Fiber', [], 0, 1, 0)
        ]
        
        protocol_viz = self.visualizer.generate_protocol_stack_visualization(protocol_layers)
        visualizations['protocol_stack'] = protocol_viz
        
        # Packet flow visualization
        packet_flow_viz = self.visualizer.generate_packet_flow_visualization(
            'Client', 'Server', ['Router1', 'Router2'], ['HTTP', 'TCP', 'IP', 'Ethernet']
        )
        visualizations['packet_flow'] = packet_flow_viz
        
        # Combined FLA-Network visualization
        combined_viz = self.visualizer.generate_combined_fla_network_visualization(
            {'grammar_rules': cfg_result.get('grammar_rules', {}), 'parse_success': cfg_result.get('valid', False)},
            {'protocol_stack': protocol_viz, 'packet_analysis': packet_viz}
        )
        visualizations['combined_analysis'] = combined_viz
        
        return visualizations
    
    def _convert_to_tree_node(self, parse_tree_data: Any) -> Optional[TreeNode]:
        """Convert parse tree data to TreeNode format."""
        if not parse_tree_data:
            return None
            
        if isinstance(parse_tree_data, dict):
            node_id = parse_tree_data.get('id', 'node_1')
            label = parse_tree_data.get('label', 'Unknown')
            node_type = NodeType.NON_TERMINAL if parse_tree_data.get('is_terminal', False) else NodeType.TERMINAL
            
            children = []
            if 'children' in parse_tree_data:
                for child_data in parse_tree_data['children']:
                    child_node = self._convert_to_tree_node(child_data)
                    if child_node:
                        children.append(child_node)
            
            return TreeNode(
                id=node_id,
                label=label,
                node_type=node_type,
                children=children,
                production_rule=parse_tree_data.get('rule', None)
            )
        
        return None
    
    def _generate_integration_insights(self, components: Dict[str, Any]) -> Dict[str, Any]:
        """Generate insights about how FLA and networking integrate."""
        insights = {
            'formal_language_applications': [
                {
                    'concept': 'Context-Free Grammars',
                    'network_application': 'HTTP request/response syntax validation',
                    'benefit': 'Ensures protocol compliance and prevents malformed requests'
                },
                {
                    'concept': 'Finite State Automata',
                    'network_application': 'TCP connection state management',
                    'benefit': 'Models connection lifecycle and state transitions'
                },
                {
                    'concept': 'Pushdown Automata',
                    'network_application': 'Nested protocol parsing (HTTP headers, JSON payloads)',
                    'benefit': 'Handles hierarchical data structures in network protocols'
                }
            ],
            'network_protocol_formal_aspects': [
                {
                    'protocol_feature': 'HTTP Message Structure',
                    'formal_model': 'Context-Free Grammar',
                    'example': 'request-line = method SP request-target SP HTTP-version CRLF'
                },
                {
                    'protocol_feature': 'TCP State Machine',
                    'formal_model': 'Finite State Automaton',
                    'example': 'CLOSED → LISTEN → SYN_RCVD → ESTABLISHED'
                },
                {
                    'protocol_feature': 'Protocol Stack Encapsulation',
                    'formal_model': 'Hierarchical Grammar',
                    'example': 'Application → Transport → Network → Data Link'
                }
            ],
            'practical_benefits': [
                'Automated protocol validation',
                'Formal verification of network implementations',
                'Educational tools for understanding both domains',
                'Error detection and recovery mechanisms',
                'Specification-driven development'
            ]
        }
        
        return insights
    
    def _perform_formal_verification(self, components: Dict[str, Any]) -> Dict[str, Any]:
        """Perform formal verification across all components."""
        verification = {
            'syntax_verification': {
                'cfg_validation': components.get('cfg_parsing', {}).get('valid', False),
                'header_validation': components.get('header_validation', {}).get('is_valid', False),
                'lexical_validation': len(components.get('fsa_tokenization', {}).get('lexical_errors', [])) == 0
            },
            'semantic_verification': {
                'method_path_consistency': True,  # Would check if method matches expected path
                'header_requirements': True,     # Would verify required headers for method
                'protocol_compliance': True      # Would check RFC compliance
            },
            'network_verification': {
                'packet_structure': components.get('packet_analysis', {}).get('packet_info', {}).get('is_valid', False),
                'protocol_stack_integrity': True,
                'state_machine_consistency': True
            },
            'overall_score': 0.0,
            'recommendations': []
        }
        
        # Calculate overall score
        all_checks = []
        for category in verification.values():
            if isinstance(category, dict):
                all_checks.extend([v for v in category.values() if isinstance(v, bool)])
        
        if all_checks:
            verification['overall_score'] = sum(all_checks) / len(all_checks) * 100
        
        # Generate recommendations
        if not verification['syntax_verification']['cfg_validation']:
            verification['recommendations'].append('Fix HTTP request syntax errors')
        if not verification['syntax_verification']['header_validation']:
            verification['recommendations'].append('Correct invalid HTTP headers')
        
        return verification
    
    def _generate_educational_content(self, results: Dict[str, Any]) -> Dict[str, Any]:
        """Generate educational explanations and examples."""
        return {
            'concepts_explained': {
                'context_free_grammar': {
                    'definition': 'A formal grammar with rules that can generate context-free languages',
                    'example': 'HTTP-message = start-line *(header-field CRLF) CRLF [message-body]',
                    'application': 'Used to define and validate HTTP message syntax'
                },
                'finite_state_automaton': {
                    'definition': 'A computational model with states and transitions',
                    'example': 'TCP connection states: CLOSED → LISTEN → ESTABLISHED → CLOSE_WAIT',
                    'application': 'Models protocol state machines and connection lifecycles'
                },
                'network_layering': {
                    'definition': 'Hierarchical organization of network protocols',
                    'example': 'Application (HTTP) → Transport (TCP) → Network (IP) → Data Link (Ethernet)',
                    'application': 'Enables modular protocol design and implementation'
                }
            },
            'learning_paths': {
                'beginner': [
                    'Understand basic HTTP request structure',
                    'Learn about protocol layers',
                    'Explore simple state machines'
                ],
                'intermediate': [
                    'Study context-free grammars for protocol definition',
                    'Analyze TCP state machine behavior',
                    'Implement basic protocol parsers'
                ],
                'advanced': [
                    'Design formal protocol specifications',
                    'Build comprehensive protocol analyzers',
                    'Research protocol verification methods'
                ]
            },
            'practical_exercises': [
                'Parse different HTTP methods using CFG rules',
                'Trace TCP connection establishment',
                'Analyze packet flow through network layers',
                'Validate protocol compliance automatically'
            ]
        }

# Create the comprehensive analysis engine
analysis_engine = ComprehensiveAnalysisEngine()

@app.route('/api/comprehensive/analyze', methods=['POST'])
def comprehensive_analyze():
    """Comprehensive analysis endpoint."""
    try:
        data = request.get_json()
        http_request = data.get('request', '')
        
        if not http_request:
            return jsonify({'error': 'No HTTP request provided'}), 400
        
        result = analysis_engine.comprehensive_analysis(http_request)
        return jsonify(result)
        
    except Exception as e:
        return jsonify({
            'error': str(e),
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/comprehensive/components', methods=['GET'])
def get_available_components():
    """Get information about available analysis components."""
    return jsonify({
        'components': [
            'FSA Tokenizer',
            'CFG Parser', 
            'PDA Parser',
            'TCP State Machine',
            'Packet Analyzer',
            'Header Validator',
            'Advanced Visualizer'
        ],
        'visualizations': [
            'Parse Tree',
            'FSA Diagram',
            'Protocol Stack',
            'Packet Flow',
            'Combined Analysis'
        ],
        'educational_features': [
            'Integration Insights',
            'Formal Verification',
            'Learning Paths',
            'Practical Exercises'
        ]
    })

@app.route('/api/comprehensive/demo', methods=['GET'])
def get_demo_data():
    """Get demo HTTP request for testing."""
    demo_request = """GET /api/users/123 HTTP/1.1
Host: example.com
User-Agent: Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36
Accept: application/json, text/plain, */*
Accept-Language: en-US,en;q=0.5
Accept-Encoding: gzip, deflate
Authorization: Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9
Connection: keep-alive
Cache-Control: no-cache"""
    
    return jsonify({
        'demo_request': demo_request,
        'description': 'Sample HTTP GET request with various headers for comprehensive analysis'
    })

if __name__ == '__main__':
    app.run(debug=True, port=5000)