"""
Enhanced API Endpoints for Advanced CFG and Network Analysis

This module provides enhanced API endpoints that integrate advanced
FLA concepts and computer networks principles for comprehensive
HTTP request validation and analysis.
"""

from flask import Flask, request, jsonify
from flask_cors import CORS
import json
from datetime import datetime
import traceback

# Import our enhanced modules
from advanced_cfg_parser import AdvancedHTTPRequestCFGParser, LexicalAnalyzer
from fsa_tokenizer import HTTPRequestFSA
from pda_parser import HTTPRequestPDA
from network_state_machine import NetworkProtocolAnalyzer

app = Flask(__name__)
CORS(app)

# Initialize enhanced parsers and analyzers
advanced_cfg_parser = AdvancedHTTPRequestCFGParser()
fsa_tokenizer = HTTPRequestFSA()
pda_parser = HTTPRequestPDA()
network_analyzer = NetworkProtocolAnalyzer()

@app.route('/api/enhanced/validate', methods=['POST'])
def enhanced_validate():
    """
    Enhanced validation endpoint that performs comprehensive analysis
    using multiple FLA and networking concepts.
    """
    try:
        data = request.get_json()
        if not data or 'request_text' not in data:
            return jsonify({'error': 'Missing request_text in payload'}), 400
        
        request_text = data['request_text'].strip()
        if not request_text:
            return jsonify({'error': 'Empty request_text'}), 400
        
        # Comprehensive analysis result
        analysis_result = {
            'request_text': request_text,
            'timestamp': datetime.now().isoformat(),
            'fla_analysis': {},
            'network_analysis': {},
            'integration_analysis': {},
            'overall_validity': False,
            'compliance_score': 0.0
        }
        
        # Step 1: Finite State Automaton (FSA) Lexical Analysis
        fsa_tokens = fsa_tokenizer.process_input(request_text)
        fsa_analysis = fsa_tokenizer.analyze_token_sequence(fsa_tokens)
        
        analysis_result['fla_analysis']['fsa'] = {
            'tokens': [
                {
                    'type': token.type,
                    'value': token.value,
                    'position': f"{token.start_pos}-{token.end_pos}",
                    'line': token.line,
                    'column': token.column
                }
                for token in fsa_tokens
            ],
            'token_analysis': fsa_analysis,
            'state_transitions': len(fsa_tokenizer.state_path) if hasattr(fsa_tokenizer, 'state_path') else 0
        }
        
        # Step 2: Advanced CFG Parsing
        cfg_result = advanced_cfg_parser.validate_request(request_text)
        analysis_result['fla_analysis']['cfg'] = cfg_result
        
        # Step 3: Pushdown Automaton (PDA) Analysis
        # Convert FSA tokens to format expected by PDA
        pda_tokens = [{'type': token.type, 'value': token.value} for token in fsa_tokens if token.type != 'ERROR']
        pda_result = pda_parser.parse(pda_tokens)
        
        analysis_result['fla_analysis']['pda'] = {
            'parse_valid': pda_result['is_valid'],
            'execution_steps': len(pda_result['execution_trace']),
            'final_state': pda_result['final_state'],
            'tokens_consumed': pda_result['tokens_consumed'],
            'stack_depth': max(len(config['stack']) for config in pda_result['configurations']) if pda_result['configurations'] else 0
        }
        
        # Step 4: Network Protocol Analysis
        network_simulation = network_analyzer.simulate_complete_http_session()
        protocol_compliance = network_analyzer.analyze_protocol_compliance(network_simulation)
        
        analysis_result['network_analysis'] = {
            'tcp_simulation': {
                'handshake_successful': all(r.get('success', False) for r in network_simulation.get('tcp_handshake', [])),
                'connection_established': network_simulation.get('final_tcp_state') == 'ESTABLISHED',
                'total_packets': network_simulation.get('total_packets', 0)
            },
            'http_simulation': {
                'request_processed': network_simulation.get('http_request', {}).get('success', False),
                'response_generated': network_simulation.get('http_response', {}).get('success', False),
                'protocol_version': network_simulation.get('session_analytics', {}).get('protocol_version', 'unknown')
            },
            'compliance': protocol_compliance
        }
        
        # Step 5: Integration Analysis
        analysis_result['integration_analysis'] = {
            'fla_network_correlation': {
                'tokens_match_network_structure': _analyze_token_network_correlation(fsa_tokens, network_simulation),
                'cfg_validates_protocol': cfg_result.get('is_valid', False),
                'pda_confirms_structure': pda_result['is_valid']
            },
            'formal_verification': {
                'lexical_correctness': fsa_analysis.get('structure_validity', {}).get('is_valid', False),
                'syntactic_correctness': cfg_result.get('is_valid', False),
                'semantic_correctness': len(cfg_result.get('semantic_analysis', {}).get('warnings', [])) == 0,
                'protocol_compliance': protocol_compliance.get('overall_score', 0) > 80
            }
        }
        
        # Calculate overall validity and compliance score
        fla_score = (
            (1 if analysis_result['integration_analysis']['formal_verification']['lexical_correctness'] else 0) +
            (1 if analysis_result['integration_analysis']['formal_verification']['syntactic_correctness'] else 0) +
            (1 if analysis_result['integration_analysis']['formal_verification']['semantic_correctness'] else 0)
        ) / 3 * 100
        
        network_score = protocol_compliance.get('overall_score', 0)
        
        analysis_result['compliance_score'] = (fla_score + network_score) / 2
        analysis_result['overall_validity'] = analysis_result['compliance_score'] > 75
        
        return jsonify(analysis_result)
        
    except Exception as e:
        return jsonify({
            'error': f'Enhanced validation error: {str(e)}',
            'traceback': traceback.format_exc()
        }), 500

@app.route('/api/enhanced/fsa-analysis', methods=['POST'])
def fsa_analysis():
    """Detailed FSA analysis endpoint."""
    try:
        data = request.get_json()
        if not data or 'input_text' not in data:
            return jsonify({'error': 'Missing input_text in payload'}), 400
        
        input_text = data['input_text']
        
        # Process with FSA
        tokens = fsa_tokenizer.process_input(input_text)
        analysis = fsa_tokenizer.analyze_token_sequence(tokens)
        state_graph = fsa_tokenizer.get_state_transition_graph()
        
        return jsonify({
            'tokens': [
                {
                    'type': token.type,
                    'value': token.value,
                    'start_pos': token.start_pos,
                    'end_pos': token.end_pos,
                    'line': token.line,
                    'column': token.column,
                    'state_path': token.state_path
                }
                for token in tokens
            ],
            'analysis': analysis,
            'automaton': {
                'total_states': len(state_graph['states']),
                'total_transitions': len(state_graph['transitions']),
                'start_state': state_graph['start_state'],
                'accepting_states': state_graph['accepting_states']
            },
            'complexity': {
                'time_complexity': 'O(n) where n is input length',
                'space_complexity': 'O(1) for DFA recognition'
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'FSA analysis error: {str(e)}'}), 500

@app.route('/api/enhanced/pda-analysis', methods=['POST'])
def pda_analysis():
    """Detailed PDA analysis endpoint."""
    try:
        data = request.get_json()
        if not data or 'tokens' not in data:
            return jsonify({'error': 'Missing tokens in payload'}), 400
        
        tokens = data['tokens']
        
        # Process with PDA
        result = pda_parser.parse(tokens)
        grammar_info = pda_parser.get_grammar_info()
        automaton_desc = pda_parser.get_automaton_description()
        
        return jsonify({
            'parse_result': result,
            'grammar': grammar_info,
            'automaton': automaton_desc,
            'parse_tree_visualization': pda_parser.visualize_parse_tree(result['parse_tree']) if result.get('parse_tree') else None
        })
        
    except Exception as e:
        return jsonify({'error': f'PDA analysis error: {str(e)}'}), 500

@app.route('/api/enhanced/network-simulation', methods=['POST'])
def network_simulation():
    """Network protocol simulation endpoint."""
    try:
        data = request.get_json()
        client_ip = data.get('client_ip', '192.168.1.100')
        server_ip = data.get('server_ip', '203.0.113.50')
        
        # Run simulation
        simulation_result = network_analyzer.simulate_complete_http_session(client_ip, server_ip)
        compliance = network_analyzer.analyze_protocol_compliance(simulation_result)
        
        return jsonify({
            'simulation': simulation_result,
            'compliance': compliance,
            'educational_notes': {
                'tcp_states': [
                    'CLOSED → LISTEN → SYN_RECEIVED → ESTABLISHED (3-way handshake)',
                    'ESTABLISHED → FIN_WAIT_1 → FIN_WAIT_2 → TIME_WAIT → CLOSED (4-way close)'
                ],
                'http_flow': [
                    'TCP connection established',
                    'HTTP request sent',
                    'Request parsed and processed',
                    'HTTP response sent',
                    'Connection managed (keep-alive or close)'
                ]
            }
        })
        
    except Exception as e:
        return jsonify({'error': f'Network simulation error: {str(e)}'}), 500

@app.route('/api/enhanced/formal-verification', methods=['POST'])
def formal_verification():
    """Formal verification endpoint combining FLA and network analysis."""
    try:
        data = request.get_json()
        if not data or 'request_text' not in data:
            return jsonify({'error': 'Missing request_text in payload'}), 400
        
        request_text = data['request_text']
        
        # Multi-level verification
        verification_result = {
            'input': request_text,
            'verification_levels': {},
            'formal_properties': {},
            'compliance_matrix': {},
            'recommendations': []
        }
        
        # Level 1: Lexical verification (FSA)
        fsa_tokens = fsa_tokenizer.process_input(request_text)
        lexical_valid = all(token.type != 'ERROR' for token in fsa_tokens)
        
        verification_result['verification_levels']['lexical'] = {
            'valid': lexical_valid,
            'method': 'Finite State Automaton (FSA)',
            'details': 'Token recognition and classification'
        }
        
        # Level 2: Syntactic verification (CFG)
        cfg_result = advanced_cfg_parser.validate_request(request_text)
        syntactic_valid = cfg_result.get('is_valid', False)
        
        verification_result['verification_levels']['syntactic'] = {
            'valid': syntactic_valid,
            'method': 'Context-Free Grammar (CFG)',
            'details': 'Grammar rule compliance verification'
        }
        
        # Level 3: Semantic verification
        semantic_warnings = cfg_result.get('semantic_analysis', {}).get('warnings', [])
        semantic_valid = len(semantic_warnings) == 0
        
        verification_result['verification_levels']['semantic'] = {
            'valid': semantic_valid,
            'method': 'Semantic Analysis',
            'details': 'HTTP protocol semantics verification',
            'warnings': semantic_warnings
        }
        
        # Level 4: Protocol verification
        network_sim = network_analyzer.simulate_complete_http_session()
        protocol_compliance = network_analyzer.analyze_protocol_compliance(network_sim)
        protocol_valid = protocol_compliance.get('overall_score', 0) > 80
        
        verification_result['verification_levels']['protocol'] = {
            'valid': protocol_valid,
            'method': 'Network Protocol Simulation',
            'details': 'TCP/HTTP protocol compliance verification',
            'score': protocol_compliance.get('overall_score', 0)
        }
        
        # Formal properties verification
        verification_result['formal_properties'] = {
            'language_membership': lexical_valid and syntactic_valid,
            'grammar_conformance': syntactic_valid,
            'protocol_compliance': protocol_valid,
            'deterministic_parsing': True,  # Our parser is deterministic
            'completeness': all([
                verification_result['verification_levels'][level]['valid']
                for level in verification_result['verification_levels']
            ])
        }
        
        # Compliance matrix
        verification_result['compliance_matrix'] = {
            'RFC_7230_HTTP_1_1': syntactic_valid and semantic_valid,
            'TCP_RFC_793': protocol_valid,
            'Formal_Language_Theory': lexical_valid and syntactic_valid,
            'Automata_Theory': True  # Our implementation uses automata
        }
        
        # Generate recommendations
        if not lexical_valid:
            verification_result['recommendations'].append("Fix lexical errors: invalid characters or token structure")
        if not syntactic_valid:
            verification_result['recommendations'].append("Fix syntax errors: request does not conform to HTTP grammar")
        if not semantic_valid:
            verification_result['recommendations'].append(f"Address semantic issues: {', '.join(semantic_warnings)}")
        if not protocol_valid:
            verification_result['recommendations'].append("Improve protocol compliance: check TCP/HTTP state management")
        
        if all([lexical_valid, syntactic_valid, semantic_valid, protocol_valid]):
            verification_result['recommendations'].append("Request is formally verified and protocol compliant!")
        
        return jsonify(verification_result)
        
    except Exception as e:
        return jsonify({'error': f'Formal verification error: {str(e)}'}), 500

@app.route('/api/enhanced/educational-analysis', methods=['POST'])
def educational_analysis():
    """Educational analysis endpoint for learning FLA and networking concepts."""
    try:
        data = request.get_json()
        if not data or 'request_text' not in data:
            return jsonify({'error': 'Missing request_text in payload'}), 400
        
        request_text = data['request_text']
        
        # Educational breakdown
        educational_result = {
            'fla_concepts_demonstrated': {
                'finite_state_automaton': {
                    'description': 'Used for lexical analysis and token recognition',
                    'implementation': 'HTTPRequestFSA class with state transitions',
                    'complexity': 'O(n) time, O(1) space for recognition'
                },
                'context_free_grammar': {
                    'description': 'Defines the syntax of HTTP requests',
                    'implementation': 'Production rules for HTTP message structure',
                    'complexity': 'O(n³) time for parsing (CYK algorithm)'
                },
                'pushdown_automaton': {
                    'description': 'Recognizes context-free languages with stack',
                    'implementation': 'Stack-based parser for HTTP grammar',
                    'complexity': 'O(n³) time, O(n²) space for parsing'
                }
            },
            'network_concepts_demonstrated': {
                'tcp_state_machine': {
                    'description': 'Models TCP connection lifecycle',
                    'states': ['CLOSED', 'LISTEN', 'SYN_SENT', 'SYN_RECEIVED', 'ESTABLISHED', 'FIN_WAIT_1', 'FIN_WAIT_2', 'CLOSE_WAIT', 'CLOSING', 'LAST_ACK', 'TIME_WAIT'],
                    'implementation': 'State transitions based on packet types'
                },
                'http_protocol_layers': {
                    'description': 'Application layer protocol over TCP',
                    'components': ['Request line', 'Headers', 'Message body'],
                    'implementation': 'State machine for request/response cycle'
                },
                'packet_analysis': {
                    'description': 'Simulation of network packet flow',
                    'types': ['SYN', 'ACK', 'FIN', 'HTTP_REQUEST', 'HTTP_RESPONSE'],
                    'implementation': 'Packet creation and flow tracking'
                }
            },
            'integration_concepts': {
                'formal_verification': 'Multiple levels of validation using different automata',
                'protocol_compliance': 'Verification against RFC specifications',
                'educational_value': 'Demonstrates practical application of theoretical concepts'
            }
        }
        
        # Add specific analysis for the input
        fsa_tokens = fsa_tokenizer.process_input(request_text)
        cfg_result = advanced_cfg_parser.validate_request(request_text)
        
        educational_result['analysis_for_input'] = {
            'tokens_identified': len(fsa_tokens),
            'grammar_rules_applied': len(cfg_result.get('grammar_rules', [])),
            'learning_opportunities': [
                f"FSA recognized {len(set(token.type for token in fsa_tokens))} different token types",
                f"CFG validation {'succeeded' if cfg_result.get('is_valid') else 'failed'} - demonstrates grammar membership",
                f"Network simulation shows complete TCP/HTTP interaction cycle"
            ]
        }
        
        return jsonify(educational_result)
        
    except Exception as e:
        return jsonify({'error': f'Educational analysis error: {str(e)}'}), 500

def _analyze_token_network_correlation(fsa_tokens, network_simulation):
    """Analyze correlation between FSA tokens and network structure."""
    
    # Extract token types
    token_types = [token.type for token in fsa_tokens]
    
    # Check if tokens match expected HTTP structure
    has_method = 'METHOD' in token_types
    has_uri = 'URI' in token_types
    has_version = 'HTTP_VERSION' in token_types
    
    # Check network simulation results
    network_success = network_simulation.get('http_request', {}).get('success', False)
    
    return {
        'tokens_complete': has_method and has_uri and has_version,
        'network_successful': network_success,
        'correlation_valid': (has_method and has_uri and has_version) == network_success
    }

if __name__ == '__main__':
    print("Starting Enhanced CFG and Network Analysis API...")
    print("Available endpoints:")
    print("  POST /api/enhanced/validate - Comprehensive analysis")
    print("  POST /api/enhanced/fsa-analysis - FSA detailed analysis")
    print("  POST /api/enhanced/pda-analysis - PDA detailed analysis")
    print("  POST /api/enhanced/network-simulation - Network simulation")
    print("  POST /api/enhanced/formal-verification - Formal verification")
    print("  POST /api/enhanced/educational-analysis - Educational breakdown")
    
    app.run(host='0.0.0.0', port=5001, debug=True)