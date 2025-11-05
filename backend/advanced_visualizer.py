"""
Advanced Visualization for CFG Derivations and Network Protocol Layers

This module provides comprehensive visualization capabilities for:
1. Context-Free Grammar derivations and parse trees
2. Network protocol layer analysis
3. Formal language automaton state transitions
4. Educational diagrams for FLA and networking concepts
"""

import json
import re
from typing import Dict, List, Any, Optional, Tuple, Union
from datetime import datetime
from enum import Enum
from dataclasses import dataclass, asdict

class VisualizationType(Enum):
    PARSE_TREE = "parse_tree"
    DERIVATION_STEPS = "derivation_steps"
    FSA_DIAGRAM = "fsa_diagram"
    PDA_DIAGRAM = "pda_diagram"
    PROTOCOL_STACK = "protocol_stack"
    PACKET_FLOW = "packet_flow"
    NETWORK_TOPOLOGY = "network_topology"
    GRAMMAR_RULES = "grammar_rules"

class NodeType(Enum):
    TERMINAL = "terminal"
    NON_TERMINAL = "non_terminal"
    ROOT = "root"
    PRODUCTION = "production"

@dataclass
class TreeNode:
    """Represents a node in a parse tree."""
    id: str
    label: str
    node_type: NodeType
    children: List['TreeNode']
    parent_id: Optional[str] = None
    production_rule: Optional[str] = None
    position: Optional[Tuple[int, int]] = None
    metadata: Optional[Dict[str, Any]] = None

    def __post_init__(self):
        if self.metadata is None:
            self.metadata = {}

@dataclass
class DerivationStep:
    """Represents a step in CFG derivation."""
    step_number: int
    current_string: str
    applied_rule: str
    replaced_symbol: str
    replacement: str
    position: int
    explanation: str

@dataclass
class StateTransition:
    """Represents a state transition in automaton."""
    from_state: str
    to_state: str
    input_symbol: str
    stack_operation: Optional[str] = None
    output: Optional[str] = None

@dataclass
class ProtocolLayer:
    """Represents a network protocol layer."""
    name: str
    protocol: str
    headers: List[Dict[str, str]]
    payload_size: int
    layer_number: int
    encapsulation_overhead: int

class AdvancedVisualizer:
    """Advanced visualization generator for FLA and networking concepts."""
    
    def __init__(self):
        self.color_scheme = {
            'terminal': '#4CAF50',
            'non_terminal': '#2196F3',
            'root': '#FF9800',
            'production': '#9C27B0',
            'physical': '#795548',
            'data_link': '#607D8B',
            'network': '#3F51B5',
            'transport': '#009688',
            'application': '#F44336'
        }
        self.layout_settings = {
            'node_spacing': 80,
            'level_spacing': 100,
            'font_size': 12,
            'arrow_size': 8
        }
    
    def generate_parse_tree_visualization(self, parse_tree: TreeNode, 
                                        grammar_rules: Dict[str, List[str]]) -> Dict[str, Any]:
        """Generate visualization data for parse tree."""
        nodes = []
        edges = []
        positions = {}
        
        # Calculate positions using a tree layout algorithm
        self._calculate_tree_positions(parse_tree, positions, 0, 0)
        
        # Generate nodes and edges
        self._traverse_tree_for_visualization(parse_tree, nodes, edges, positions)
        
        # Generate derivation steps
        derivation_steps = self._generate_derivation_steps(parse_tree, grammar_rules)
        
        return {
            'type': VisualizationType.PARSE_TREE.value,
            'title': 'Context-Free Grammar Parse Tree',
            'nodes': nodes,
            'edges': edges,
            'derivation_steps': [asdict(step) for step in derivation_steps],
            'grammar_info': {
                'rules': grammar_rules,
                'terminals': self._extract_terminals(parse_tree),
                'non_terminals': self._extract_non_terminals(parse_tree)
            },
            'layout': {
                'width': max(pos[0] for pos in positions.values()) + 200,
                'height': max(pos[1] for pos in positions.values()) + 200,
                'root_position': positions.get(parse_tree.id, (0, 0))
            },
            'interaction': {
                'expandable_nodes': True,
                'step_by_step_derivation': True,
                'rule_highlighting': True
            }
        }
    
    def generate_fsa_visualization(self, states: List[str], 
                                 transitions: List[StateTransition],
                                 alphabet: List[str],
                                 start_state: str,
                                 accept_states: List[str]) -> Dict[str, Any]:
        """Generate FSA diagram visualization."""
        nodes = []
        edges = []
        
        # Generate state nodes
        for i, state in enumerate(states):
            node_type = 'start' if state == start_state else 'accept' if state in accept_states else 'normal'
            nodes.append({
                'id': state,
                'label': state,
                'type': node_type,
                'position': self._calculate_circular_position(i, len(states), 200),
                'color': self._get_state_color(node_type),
                'size': 30,
                'border_width': 3 if node_type in ['start', 'accept'] else 1
            })
        
        # Generate transition edges
        for transition in transitions:
            edges.append({
                'id': f"{transition.from_state}_{transition.to_state}_{transition.input_symbol}",
                'source': transition.from_state,
                'target': transition.to_state,
                'label': transition.input_symbol,
                'curved': True if transition.from_state == transition.to_state else False,
                'arrow_type': 'triangle',
                'color': '#666'
            })
        
        return {
            'type': VisualizationType.FSA_DIAGRAM.value,
            'title': 'Finite State Automaton',
            'nodes': nodes,
            'edges': edges,
            'alphabet': alphabet,
            'metadata': {
                'state_count': len(states),
                'transition_count': len(transitions),
                'alphabet_size': len(alphabet),
                'start_state': start_state,
                'accept_states': accept_states
            },
            'simulation': {
                'input_string': '',
                'current_state': start_state,
                'step_history': [],
                'accepted': False
            }
        }
    
    def generate_protocol_stack_visualization(self, layers: List[ProtocolLayer]) -> Dict[str, Any]:
        """Generate network protocol stack visualization."""
        layer_boxes = []
        total_height = 0
        
        for i, layer in enumerate(sorted(layers, key=lambda x: x.layer_number, reverse=True)):
            box_height = 60 + (len(layer.headers) * 20)
            layer_boxes.append({
                'id': f"layer_{layer.layer_number}",
                'name': layer.name,
                'protocol': layer.protocol,
                'headers': layer.headers,
                'position': {
                    'x': 50,
                    'y': total_height + 20,
                    'width': 400,
                    'height': box_height
                },
                'color': self.color_scheme.get(layer.name.lower(), '#999'),
                'payload_size': layer.payload_size,
                'overhead': layer.encapsulation_overhead
            })
            total_height += box_height + 10
        
        # Generate encapsulation flow
        encapsulation_steps = []
        for i, layer in enumerate(layers):
            encapsulation_steps.append({
                'step': i + 1,
                'layer': layer.name,
                'action': f"Add {layer.protocol} header",
                'size_added': layer.encapsulation_overhead,
                'total_size': sum(l.payload_size + l.encapsulation_overhead for l in layers[:i+1])
            })
        
        return {
            'type': VisualizationType.PROTOCOL_STACK.value,
            'title': 'Network Protocol Stack',
            'layers': layer_boxes,
            'encapsulation_flow': encapsulation_steps,
            'total_size': sum(l.payload_size + l.encapsulation_overhead for l in layers),
            'layout': {
                'width': 500,
                'height': total_height + 40
            },
            'animations': {
                'encapsulation_sequence': True,
                'data_flow_direction': 'top_down',
                'timing': 'sequential'
            }
        }
    
    def generate_packet_flow_visualization(self, source: str, destination: str,
                                         path_nodes: List[str],
                                         protocols: List[str]) -> Dict[str, Any]:
        """Generate packet flow through network visualization."""
        nodes = []
        edges = []
        
        # Add source and destination
        all_nodes = [source] + path_nodes + [destination]
        
        for i, node in enumerate(all_nodes):
            node_type = 'source' if node == source else 'destination' if node == destination else 'router'
            nodes.append({
                'id': node,
                'label': node,
                'type': node_type,
                'position': (i * 150, 100),
                'color': self._get_node_color(node_type),
                'size': 40 if node_type in ['source', 'destination'] else 30
            })
        
        # Add path edges
        for i in range(len(all_nodes) - 1):
            edges.append({
                'id': f"path_{i}",
                'source': all_nodes[i],
                'target': all_nodes[i + 1],
                'label': f"Step {i + 1}",
                'color': '#4CAF50',
                'animated': True
            })
        
        # Generate protocol timeline
        timeline = []
        for i, protocol in enumerate(protocols):
            timeline.append({
                'time': i * 100,
                'event': f"{protocol} processing",
                'node': all_nodes[min(i, len(all_nodes) - 1)],
                'description': f"Packet processed using {protocol}"
            })
        
        return {
            'type': VisualizationType.PACKET_FLOW.value,
            'title': 'Packet Flow Through Network',
            'nodes': nodes,
            'edges': edges,
            'timeline': timeline,
            'path_info': {
                'source': source,
                'destination': destination,
                'hop_count': len(path_nodes),
                'protocols_used': protocols
            },
            'animation': {
                'packet_speed': 1000,  # ms per hop
                'show_protocol_stack': True,
                'highlight_current_node': True
            }
        }
    
    def generate_combined_fla_network_visualization(self, 
                                                  cfg_data: Dict[str, Any],
                                                  network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate combined FLA and network visualization."""
        return {
            'type': 'combined_analysis',
            'title': 'Formal Language Automata meets Computer Networks',
            'sections': [
                {
                    'title': 'Grammar-Based Protocol Parsing',
                    'content': cfg_data,
                    'position': {'x': 0, 'y': 0, 'width': 50, 'height': 50}
                },
                {
                    'title': 'Network Protocol Stack',
                    'content': network_data,
                    'position': {'x': 50, 'y': 0, 'width': 50, 'height': 50}
                },
                {
                    'title': 'Integration Points',
                    'content': self._generate_integration_points(cfg_data, network_data),
                    'position': {'x': 0, 'y': 50, 'width': 100, 'height': 50}
                }
            ],
            'connections': [
                {
                    'from': 'grammar_rules',
                    'to': 'protocol_validation',
                    'label': 'Formal Verification',
                    'type': 'conceptual'
                },
                {
                    'from': 'parse_tree',
                    'to': 'packet_structure',
                    'label': 'Structural Analysis',
                    'type': 'mapping'
                }
            ],
            'educational_notes': [
                "CFG rules define valid HTTP request syntax",
                "FSA tokenizes network protocol fields",
                "PDA validates nested protocol structures",
                "State machines model network connection states"
            ]
        }
    
    def _calculate_tree_positions(self, node: TreeNode, positions: Dict[str, Tuple[int, int]], 
                                x: int, y: int, level: int = 0) -> int:
        """Calculate positions for tree layout."""
        if not node.children:
            positions[node.id] = (x, y)
            return x + self.layout_settings['node_spacing']
        
        # Calculate positions for children first
        child_x = x
        for child in node.children:
            child_x = self._calculate_tree_positions(child, positions, child_x, 
                                                   y + self.layout_settings['level_spacing'], level + 1)
        
        # Position parent in the middle of children
        if node.children:
            first_child_x = positions[node.children[0].id][0]
            last_child_x = positions[node.children[-1].id][0]
            parent_x = (first_child_x + last_child_x) // 2
        else:
            parent_x = x
        
        positions[node.id] = (parent_x, y)
        return child_x
    
    def _traverse_tree_for_visualization(self, node: TreeNode, nodes: List[Dict], 
                                       edges: List[Dict], positions: Dict[str, Tuple[int, int]]):
        """Traverse tree and generate visualization nodes and edges."""
        position = positions.get(node.id, (0, 0))
        
        nodes.append({
            'id': node.id,
            'label': node.label,
            'type': node.node_type.value,
            'position': position,
            'color': self.color_scheme.get(node.node_type.value, '#999'),
            'production_rule': node.production_rule,
            'metadata': node.metadata
        })
        
        for child in node.children:
            edges.append({
                'id': f"{node.id}_{child.id}",
                'source': node.id,
                'target': child.id,
                'type': 'tree_edge'
            })
            self._traverse_tree_for_visualization(child, nodes, edges, positions)
    
    def _generate_derivation_steps(self, parse_tree: TreeNode, 
                                 grammar_rules: Dict[str, List[str]]) -> List[DerivationStep]:
        """Generate step-by-step derivation from parse tree."""
        steps = []
        current_string = parse_tree.label
        step_count = 0
        
        def traverse_for_derivation(node: TreeNode, current: str, steps_list: List[DerivationStep]):
            nonlocal step_count
            
            if node.children and node.production_rule:
                step_count += 1
                replacement = ' '.join(child.label for child in node.children)
                position = current.find(node.label)
                
                new_string = current[:position] + replacement + current[position + len(node.label):]
                
                steps_list.append(DerivationStep(
                    step_number=step_count,
                    current_string=current,
                    applied_rule=node.production_rule,
                    replaced_symbol=node.label,
                    replacement=replacement,
                    position=position,
                    explanation=f"Apply rule: {node.production_rule}"
                ))
                
                for child in node.children:
                    traverse_for_derivation(child, new_string, steps_list)
        
        traverse_for_derivation(parse_tree, current_string, steps)
        return steps
    
    def _extract_terminals(self, node: TreeNode) -> List[str]:
        """Extract terminal symbols from parse tree."""
        terminals = []
        if node.node_type == NodeType.TERMINAL:
            terminals.append(node.label)
        for child in node.children:
            terminals.extend(self._extract_terminals(child))
        return list(set(terminals))
    
    def _extract_non_terminals(self, node: TreeNode) -> List[str]:
        """Extract non-terminal symbols from parse tree."""
        non_terminals = []
        if node.node_type == NodeType.NON_TERMINAL:
            non_terminals.append(node.label)
        for child in node.children:
            non_terminals.extend(self._extract_non_terminals(child))
        return list(set(non_terminals))
    
    def _calculate_circular_position(self, index: int, total: int, radius: int) -> Tuple[int, int]:
        """Calculate position for circular layout."""
        import math
        angle = 2 * math.pi * index / total
        x = int(radius * math.cos(angle)) + radius + 50
        y = int(radius * math.sin(angle)) + radius + 50
        return (x, y)
    
    def _get_state_color(self, state_type: str) -> str:
        """Get color for FSA state type."""
        colors = {
            'start': '#4CAF50',
            'accept': '#F44336',
            'normal': '#2196F3'
        }
        return colors.get(state_type, '#999')
    
    def _get_node_color(self, node_type: str) -> str:
        """Get color for network node type."""
        colors = {
            'source': '#4CAF50',
            'destination': '#F44336',
            'router': '#FF9800'
        }
        return colors.get(node_type, '#999')
    
    def _generate_integration_points(self, cfg_data: Dict[str, Any], 
                                   network_data: Dict[str, Any]) -> Dict[str, Any]:
        """Generate integration points between FLA and networking."""
        return {
            'formal_validation': {
                'description': 'Using CFG rules to validate protocol syntax',
                'examples': ['HTTP request validation', 'Header field parsing']
            },
            'state_modeling': {
                'description': 'FSA/PDA for protocol state management',
                'examples': ['TCP connection states', 'HTTP session tracking']
            },
            'parsing_hierarchy': {
                'description': 'Multi-level parsing similar to protocol layers',
                'examples': ['Lexical → Syntactic → Semantic', 'Physical → Network → Application']
            },
            'error_handling': {
                'description': 'Formal error detection and recovery',
                'examples': ['Syntax error recovery', 'Packet corruption detection']
            }
        }

# Example usage and testing
if __name__ == "__main__":
    visualizer = AdvancedVisualizer()
    
    # Example parse tree
    root = TreeNode("S", "S", NodeType.ROOT, [])
    
    # Example FSA
    states = ["q0", "q1", "q2"]
    transitions = [
        StateTransition("q0", "q1", "a"),
        StateTransition("q1", "q2", "b"),
        StateTransition("q2", "q2", "b")
    ]
    
    fsa_viz = visualizer.generate_fsa_visualization(
        states, transitions, ["a", "b"], "q0", ["q2"]
    )
    
    print("FSA Visualization generated with", len(fsa_viz['nodes']), "nodes")