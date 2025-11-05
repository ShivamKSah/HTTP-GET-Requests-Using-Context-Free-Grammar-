"""
Deterministic Finite Automaton (DFA) Engine with NFA to DFA Conversion

This module implements a comprehensive DFA engine including the Subset Construction
algorithm for converting NFAs to DFAs, and provides efficient string matching
capabilities for HTTP protocol analysis.
"""

from typing import Dict, List, Set, Optional, Tuple, Any, Union, FrozenSet
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import json
from datetime import datetime
from nfa_engine import NFAState, NFAEngine, NFAResult

class DFAState:
    """Represents a state in the DFA."""
    
    def __init__(self, name: str, nfa_states: Optional[Set[NFAState]] = None, is_accepting: bool = False):
        self.name = name
        self.nfa_states = nfa_states or set()  # Set of NFA states this DFA state represents
        self.is_accepting = is_accepting
        self.transitions: Dict[str, 'DFAState'] = {}
    
    def add_transition(self, symbol: str, target_state: 'DFAState'):
        """Add a transition on a symbol to a target state."""
        self.transitions[symbol] = target_state
    
    def __str__(self):
        return f"DFAState({self.name}, accepting={self.is_accepting})"
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return isinstance(other, DFAState) and self.name == other.name

@dataclass
class DFAConfiguration:
    """Represents a configuration during DFA execution."""
    current_state: DFAState
    input_position: int
    input_consumed: str
    remaining_input: str
    step: int
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class DFAResult:
    """Result of DFA execution."""
    accepted: bool
    input_string: str
    configurations: List[DFAConfiguration]
    final_state: DFAState
    total_steps: int
    execution_time: float
    path: List[str]  # Sequence of states visited

class SubsetConstruction:
    """Implements the Subset Construction algorithm for NFA to DFA conversion."""
    
    def __init__(self, nfa_engine: NFAEngine):
        self.nfa_engine = nfa_engine
        self.state_counter = 0
    
    def convert_nfa_to_dfa(self, nfa: Tuple[NFAState, NFAState]) -> Tuple[DFAState, Set[DFAState]]:
        """
        Convert an NFA to a DFA using Subset Construction algorithm.
        
        Returns:
            Tuple of (start_state, all_states) for the resulting DFA
        """
        start_nfa, _ = nfa
        
        # Step 1: Compute epsilon closure of start state
        start_closure = self.nfa_engine.epsilon_closure({start_nfa})
        
        # Create DFA start state
        start_dfa = self._create_dfa_state(start_closure)
        
        # Initialize data structures
        dfa_states = {self._nfa_set_to_key(start_closure): start_dfa}
        unmarked_states = [start_closure]
        all_dfa_states = {start_dfa}
        
        # Get alphabet from NFA
        alphabet = self.nfa_engine.get_alphabet(nfa)
        
        # Step 2: Process unmarked states
        while unmarked_states:
            current_nfa_set = unmarked_states.pop(0)
            current_dfa_state = dfa_states[self._nfa_set_to_key(current_nfa_set)]
            
            # For each symbol in alphabet
            for symbol in alphabet:
                # Compute move(current_nfa_set, symbol)
                target_nfa_set = self._move(current_nfa_set, symbol)
                
                if not target_nfa_set:
                    continue
                
                # Compute epsilon closure of target set
                target_closure = self.nfa_engine.epsilon_closure(target_nfa_set)
                target_key = self._nfa_set_to_key(target_closure)
                
                # Check if this DFA state already exists
                if target_key not in dfa_states:
                    # Create new DFA state
                    target_dfa_state = self._create_dfa_state(target_closure)
                    dfa_states[target_key] = target_dfa_state
                    all_dfa_states.add(target_dfa_state)
                    unmarked_states.append(target_closure)
                else:
                    target_dfa_state = dfa_states[target_key]
                
                # Add transition
                current_dfa_state.add_transition(symbol, target_dfa_state)
        
        return start_dfa, all_dfa_states
    
    def _move(self, nfa_states: Set[NFAState], symbol: str) -> Set[NFAState]:
        """
        Compute the set of NFA states reachable from any state in nfa_states
        on input symbol.
        """
        result = set()
        
        for state in nfa_states:
            if symbol in state.transitions:
                result.update(state.transitions[symbol])
        
        return result
    
    def _create_dfa_state(self, nfa_states: Set[NFAState]) -> DFAState:
        """Create a DFA state representing a set of NFA states."""
        # Create state name
        state_names = sorted([state.name for state in nfa_states])
        name = "{" + ",".join(state_names) + "}"
        
        # Check if any NFA state is accepting
        is_accepting = any(state.is_accepting for state in nfa_states)
        
        return DFAState(name, nfa_states, is_accepting)
    
    def _nfa_set_to_key(self, nfa_states: Set[NFAState]) -> str:
        """Convert a set of NFA states to a unique string key."""
        return ",".join(sorted([state.name for state in nfa_states]))

class DFAEngine:
    """Comprehensive DFA engine with optimization and analysis capabilities."""
    
    def __init__(self):
        self.nfa_engine = NFAEngine()
        self.subset_construction = SubsetConstruction(self.nfa_engine)
    
    def create_dfa_from_nfa(self, nfa: Tuple[NFAState, NFAState]) -> Tuple[DFAState, Set[DFAState]]:
        """Create DFA from NFA using subset construction."""
        return self.subset_construction.convert_nfa_to_dfa(nfa)
    
    def create_http_method_dfa(self) -> Tuple[DFAState, Set[DFAState]]:
        """Create DFA for HTTP methods by converting from NFA."""
        method_nfa = self.nfa_engine.create_http_method_nfa()
        return self.create_dfa_from_nfa(method_nfa)
    
    def create_uri_pattern_dfa(self) -> Tuple[DFAState, Set[DFAState]]:
        """Create DFA for URI patterns by converting from NFA."""
        uri_nfa = self.nfa_engine.create_uri_pattern_nfa()
        return self.create_dfa_from_nfa(uri_nfa)
    
    def create_http_version_dfa(self) -> Tuple[DFAState, Set[DFAState]]:
        """Create DFA for HTTP version patterns by converting from NFA."""
        version_nfa = self.nfa_engine.create_http_version_nfa()
        return self.create_dfa_from_nfa(version_nfa)
    
    def simulate(self, dfa: Tuple[DFAState, Set[DFAState]], input_string: str) -> DFAResult:
        """Simulate DFA execution on input string."""
        start_time = datetime.now()
        start_state, all_states = dfa
        
        configurations = []
        path = []
        
        # Initial configuration
        current_state = start_state
        current_config = DFAConfiguration(
            current_state=current_state,
            input_position=0,
            input_consumed="",
            remaining_input=input_string,
            step=0
        )
        configurations.append(current_config)
        path.append(current_state.name)
        
        # Process each input character
        for i, char in enumerate(input_string):
            # Check if transition exists
            if char not in current_state.transitions:
                # No transition available - reject
                break
            
            # Follow transition
            current_state = current_state.transitions[char]
            path.append(current_state.name)
            
            # Create new configuration
            current_config = DFAConfiguration(
                current_state=current_state,
                input_position=i + 1,
                input_consumed=input_string[:i + 1],
                remaining_input=input_string[i + 1:],
                step=i + 1
            )
            configurations.append(current_config)
        
        # Check acceptance
        accepted = (current_config.input_position == len(input_string) and 
                   current_state.is_accepting)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return DFAResult(
            accepted=accepted,
            input_string=input_string,
            configurations=configurations,
            final_state=current_state,
            total_steps=len(configurations),
            execution_time=execution_time,
            path=path
        )
    
    def minimize_dfa(self, dfa: Tuple[DFAState, Set[DFAState]]) -> Tuple[DFAState, Set[DFAState]]:
        """
        Minimize DFA using Hopcroft's algorithm (simplified version).
        This is a basic implementation - a full version would be more complex.
        """
        start_state, all_states = dfa
        
        if not all_states:
            return start_state, all_states
        
        # Get alphabet
        alphabet = self._get_dfa_alphabet(all_states)
        
        # Step 1: Initial partition into accepting and non-accepting states
        accepting_states = {state for state in all_states if state.is_accepting}
        non_accepting_states = {state for state in all_states if not state.is_accepting}
        
        partitions = []
        if non_accepting_states:
            partitions.append(non_accepting_states)
        if accepting_states:
            partitions.append(accepting_states)
        
        # Step 2: Refine partitions
        changed = True
        while changed:
            changed = False
            new_partitions = []
            
            for partition in partitions:
                refined = self._refine_partition(partition, partitions, alphabet)
                if len(refined) > 1:
                    changed = True
                new_partitions.extend(refined)
            
            partitions = new_partitions
        
        # Step 3: Create minimized DFA
        return self._create_minimized_dfa(partitions, start_state, alphabet)
    
    def _refine_partition(self, partition: Set[DFAState], 
                         all_partitions: List[Set[DFAState]], 
                         alphabet: Set[str]) -> List[Set[DFAState]]:
        """Refine a partition based on transition behavior."""
        if len(partition) <= 1:
            return [partition]
        
        # Group states by their transition signatures
        signature_groups = defaultdict(set)
        
        for state in partition:
            signature = []
            for symbol in sorted(alphabet):
                if symbol in state.transitions:
                    target = state.transitions[symbol]
                    # Find which partition the target belongs to
                    target_partition_idx = None
                    for i, part in enumerate(all_partitions):
                        if target in part:
                            target_partition_idx = i
                            break
                    signature.append(target_partition_idx)
                else:
                    signature.append(None)  # No transition
            
            signature_key = tuple(signature)
            signature_groups[signature_key].add(state)
        
        return list(signature_groups.values())
    
    def _create_minimized_dfa(self, partitions: List[Set[DFAState]], 
                             original_start: DFAState, 
                             alphabet: Set[str]) -> Tuple[DFAState, Set[DFAState]]:
        """Create the minimized DFA from partitions."""
        # Create new states for each partition
        partition_to_state = {}
        new_states = set()
        
        for i, partition in enumerate(partitions):
            # Use representative state from partition
            representative = next(iter(partition))
            is_accepting = representative.is_accepting
            
            new_state = DFAState(f"q{i}", set(), is_accepting)
            partition_to_state[i] = new_state
            new_states.add(new_state)
        
        # Find start state partition
        start_partition_idx = None
        for i, partition in enumerate(partitions):
            if original_start in partition:
                start_partition_idx = i
                break
        
        new_start = partition_to_state[start_partition_idx]
        
        # Create transitions
        for i, partition in enumerate(partitions):
            representative = next(iter(partition))
            new_state = partition_to_state[i]
            
            for symbol in alphabet:
                if symbol in representative.transitions:
                    target = representative.transitions[symbol]
                    
                    # Find target's partition
                    target_partition_idx = None
                    for j, part in enumerate(partitions):
                        if target in part:
                            target_partition_idx = j
                            break
                    
                    if target_partition_idx is not None:
                        target_state = partition_to_state[target_partition_idx]
                        new_state.add_transition(symbol, target_state)
        
        return new_start, new_states
    
    def _get_dfa_alphabet(self, states: Set[DFAState]) -> Set[str]:
        """Get the alphabet used by the DFA."""
        alphabet = set()
        for state in states:
            alphabet.update(state.transitions.keys())
        return alphabet
    
    def analyze_dfa_properties(self, dfa: Tuple[DFAState, Set[DFAState]]) -> Dict[str, Any]:
        """Analyze properties of the DFA."""
        start_state, all_states = dfa
        alphabet = self._get_dfa_alphabet(all_states)
        
        # Count transitions
        total_transitions = sum(len(state.transitions) for state in all_states)
        
        # Check completeness
        is_complete = all(
            len(state.transitions) == len(alphabet) 
            for state in all_states
        )
        
        # Find accepting states
        accepting_states = {state for state in all_states if state.is_accepting}
        
        # Check for unreachable states
        reachable_states = self._find_reachable_states(start_state)
        unreachable_states = all_states - reachable_states
        
        # Check for dead states (non-accepting states with no path to accepting state)
        dead_states = self._find_dead_states(all_states, accepting_states)
        
        return {
            'total_states': len(all_states),
            'alphabet_size': len(alphabet),
            'total_transitions': total_transitions,
            'accepting_states_count': len(accepting_states),
            'unreachable_states_count': len(unreachable_states),
            'dead_states_count': len(dead_states),
            'is_complete': is_complete,
            'is_deterministic': True,  # By definition
            'start_state': start_state.name,
            'complexity': {
                'space': f"O({len(all_states)})",
                'time_per_char': "O(1)",
                'preprocessing': f"O({len(all_states)}² × {len(alphabet)})"
            },
            'properties': {
                'has_unreachable_states': len(unreachable_states) > 0,
                'has_dead_states': len(dead_states) > 0,
                'is_minimal': len(unreachable_states) == 0 and len(dead_states) == 0,
                'transition_density': total_transitions / (len(all_states) * len(alphabet)) if alphabet else 0
            }
        }
    
    def _find_reachable_states(self, start_state: DFAState) -> Set[DFAState]:
        """Find all states reachable from the start state."""
        visited = set()
        stack = [start_state]
        
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            
            visited.add(current)
            stack.extend(current.transitions.values())
        
        return visited
    
    def _find_dead_states(self, all_states: Set[DFAState], 
                         accepting_states: Set[DFAState]) -> Set[DFAState]:
        """Find dead states (non-accepting states with no path to accepting state)."""
        # Build reverse transition graph
        reverse_transitions = defaultdict(set)
        for state in all_states:
            for symbol, target in state.transitions.items():
                reverse_transitions[target].add(state)
        
        # BFS from accepting states backwards
        can_reach_accepting = set(accepting_states)
        queue = deque(accepting_states)
        
        while queue:
            current = queue.popleft()
            for predecessor in reverse_transitions[current]:
                if predecessor not in can_reach_accepting:
                    can_reach_accepting.add(predecessor)
                    queue.append(predecessor)
        
        # Dead states are non-accepting states that can't reach accepting states
        non_accepting = all_states - accepting_states
        dead_states = non_accepting - can_reach_accepting
        
        return dead_states
    
    def to_dict(self, dfa: Tuple[DFAState, Set[DFAState]]) -> Dict[str, Any]:
        """Convert DFA to dictionary representation for serialization."""
        start_state, all_states = dfa
        alphabet = self._get_dfa_alphabet(all_states)
        
        # Create state mapping
        state_to_id = {state: f"q{i}" for i, state in enumerate(all_states)}
        
        # Build transitions
        transitions = []
        for state in all_states:
            state_id = state_to_id[state]
            for symbol, target in state.transitions.items():
                transitions.append({
                    'from': state_id,
                    'to': state_to_id[target],
                    'symbol': symbol
                })
        
        return {
            'type': 'DFA',
            'states': [
                {
                    'id': state_to_id[state],
                    'name': state.name,
                    'is_start': state == start_state,
                    'is_accepting': state.is_accepting
                }
                for state in all_states
            ],
            'alphabet': list(alphabet),
            'transitions': transitions,
            'start_state': state_to_id[start_state],
            'accepting_states': [state_to_id[state] for state in all_states if state.is_accepting],
            'is_deterministic': True
        }
    
    def compare_with_nfa(self, nfa: Tuple[NFAState, NFAState], 
                        dfa: Tuple[DFAState, Set[DFAState]]) -> Dict[str, Any]:
        """Compare NFA and DFA properties."""
        nfa_analysis = self.nfa_engine.analyze_nfa_properties(nfa)
        dfa_analysis = self.analyze_dfa_properties(dfa)
        
        return {
            'comparison': {
                'states': {
                    'nfa': nfa_analysis['total_states'],
                    'dfa': dfa_analysis['total_states'],
                    'ratio': dfa_analysis['total_states'] / nfa_analysis['total_states']
                },
                'transitions': {
                    'nfa': nfa_analysis['total_transitions'],
                    'dfa': dfa_analysis['total_transitions'],
                    'ratio': dfa_analysis['total_transitions'] / nfa_analysis['total_transitions'] if nfa_analysis['total_transitions'] > 0 else 0
                },
                'determinism': {
                    'nfa': nfa_analysis['is_deterministic'],
                    'dfa': True
                },
                'epsilon_transitions': {
                    'nfa': nfa_analysis['epsilon_transitions'],
                    'dfa': 0
                }
            },
            'performance': {
                'nfa_time_complexity': nfa_analysis['complexity']['time_per_char'],
                'dfa_time_complexity': 'O(1)',
                'space_trade_off': 'DFA uses more space but provides constant time recognition'
            },
            'advantages': {
                'nfa': [
                    'More compact representation',
                    'Easier to construct from regex',
                    'Natural for parallel computation'
                ],
                'dfa': [
                    'Constant time per character',
                    'Deterministic execution',
                    'No backtracking needed'
                ]
            }
        }

# Example usage and testing
if __name__ == "__main__":
    # Create DFA engine
    dfa_engine = DFAEngine()
    
    # Test NFA to DFA conversion for HTTP methods
    print("=== NFA to DFA Conversion for HTTP Methods ===")
    method_nfa = dfa_engine.nfa_engine.create_http_method_nfa()
    method_dfa = dfa_engine.create_dfa_from_nfa(method_nfa)
    
    print(f"Original NFA: {dfa_engine.nfa_engine.analyze_nfa_properties(method_nfa)['total_states']} states")
    print(f"Converted DFA: {dfa_engine.analyze_dfa_properties(method_dfa)['total_states']} states")
    
    # Test DFA simulation
    test_methods = ["GET", "POST", "PUT", "DELETE", "INVALID"]
    for method in test_methods:
        result = dfa_engine.simulate(method_dfa, method)
        print(f"'{method}': {'ACCEPTED' if result.accepted else 'REJECTED'} "
              f"(Path: {' -> '.join(result.path)})")
    
    # Compare NFA vs DFA performance
    print("\n=== Performance Comparison ===")
    comparison = dfa_engine.compare_with_nfa(method_nfa, method_dfa)
    print(f"State ratio (DFA/NFA): {comparison['comparison']['states']['ratio']:.2f}")
    print(f"NFA time complexity: {comparison['performance']['nfa_time_complexity']}")
    print(f"DFA time complexity: {comparison['performance']['dfa_time_complexity']}")
    
    # Test minimization
    print("\n=== DFA Minimization ===")
    minimized_dfa = dfa_engine.minimize_dfa(method_dfa)
    original_analysis = dfa_engine.analyze_dfa_properties(method_dfa)
    minimized_analysis = dfa_engine.analyze_dfa_properties(minimized_dfa)
    
    print(f"Original DFA: {original_analysis['total_states']} states")
    print(f"Minimized DFA: {minimized_analysis['total_states']} states")
    print(f"Reduction: {original_analysis['total_states'] - minimized_analysis['total_states']} states")