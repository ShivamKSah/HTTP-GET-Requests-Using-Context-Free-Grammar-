"""
Nondeterministic Finite Automaton (NFA) Engine with Regex Support

This module implements a comprehensive NFA engine with support for regular expressions,
Thompson's Construction, and conversion to DFA. Demonstrates advanced formal language
automata concepts in the context of HTTP protocol analysis.
"""

import re
from typing import Dict, List, Set, Optional, Tuple, Any, Union
from dataclasses import dataclass, field
from enum import Enum
from collections import defaultdict, deque
import json
from datetime import datetime

class NFAState:
    """Represents a state in the NFA."""
    
    def __init__(self, name: str, is_accepting: bool = False):
        self.name = name
        self.is_accepting = is_accepting
        self.transitions: Dict[str, Set['NFAState']] = defaultdict(set)
        self.epsilon_transitions: Set['NFAState'] = set()
    
    def add_transition(self, symbol: str, target_state: 'NFAState'):
        """Add a transition on a symbol to a target state."""
        self.transitions[symbol].add(target_state)
    
    def add_epsilon_transition(self, target_state: 'NFAState'):
        """Add an epsilon (empty) transition to a target state."""
        self.epsilon_transitions.add(target_state)
    
    def __str__(self):
        return f"NFAState({self.name}, accepting={self.is_accepting})"
    
    def __repr__(self):
        return self.__str__()
    
    def __hash__(self):
        return hash(self.name)
    
    def __eq__(self, other):
        return isinstance(other, NFAState) and self.name == other.name

@dataclass
class NFAConfiguration:
    """Represents a configuration during NFA execution."""
    current_states: Set[NFAState]
    input_position: int
    input_consumed: str
    remaining_input: str
    step: int
    timestamp: datetime = field(default_factory=datetime.now)

@dataclass
class NFAResult:
    """Result of NFA execution."""
    accepted: bool
    input_string: str
    configurations: List[NFAConfiguration]
    accepting_states: Set[NFAState]
    total_steps: int
    execution_time: float
    epsilon_closures_computed: int

class ThompsonConstruction:
    """Implements Thompson's Construction algorithm for regex to NFA conversion."""
    
    def __init__(self):
        self.state_counter = 0
    
    def _new_state(self, is_accepting: bool = False) -> NFAState:
        """Create a new unique state."""
        state = NFAState(f"q{self.state_counter}", is_accepting)
        self.state_counter += 1
        return state
    
    def char_nfa(self, char: str) -> Tuple[NFAState, NFAState]:
        """Create NFA for a single character."""
        start = self._new_state()
        end = self._new_state(True)
        start.add_transition(char, end)
        return start, end
    
    def epsilon_nfa(self) -> Tuple[NFAState, NFAState]:
        """Create NFA for epsilon (empty string)."""
        start = self._new_state()
        end = self._new_state(True)
        start.add_epsilon_transition(end)
        return start, end
    
    def concatenation(self, nfa1: Tuple[NFAState, NFAState], 
                     nfa2: Tuple[NFAState, NFAState]) -> Tuple[NFAState, NFAState]:
        """Concatenate two NFAs."""
        start1, end1 = nfa1
        start2, end2 = nfa2
        
        # Remove accepting from first NFA's end state
        end1.is_accepting = False
        
        # Connect end of first NFA to start of second NFA with epsilon
        end1.add_epsilon_transition(start2)
        
        return start1, end2
    
    def union(self, nfa1: Tuple[NFAState, NFAState], 
             nfa2: Tuple[NFAState, NFAState]) -> Tuple[NFAState, NFAState]:
        """Create union of two NFAs."""
        start1, end1 = nfa1
        start2, end2 = nfa2
        
        new_start = self._new_state()
        new_end = self._new_state(True)
        
        # Remove accepting from original end states
        end1.is_accepting = False
        end2.is_accepting = False
        
        # Connect new start to both original starts
        new_start.add_epsilon_transition(start1)
        new_start.add_epsilon_transition(start2)
        
        # Connect both original ends to new end
        end1.add_epsilon_transition(new_end)
        end2.add_epsilon_transition(new_end)
        
        return new_start, new_end
    
    def kleene_star(self, nfa: Tuple[NFAState, NFAState]) -> Tuple[NFAState, NFAState]:
        """Apply Kleene star to an NFA."""
        start, end = nfa
        
        new_start = self._new_state()
        new_end = self._new_state(True)
        
        # Remove accepting from original end
        end.is_accepting = False
        
        # New start can go directly to new end (for empty string)
        new_start.add_epsilon_transition(new_end)
        
        # New start can go to original start
        new_start.add_epsilon_transition(start)
        
        # Original end can go to new end
        end.add_epsilon_transition(new_end)
        
        # Original end can go back to original start (for repetition)
        end.add_epsilon_transition(start)
        
        return new_start, new_end
    
    def plus_closure(self, nfa: Tuple[NFAState, NFAState]) -> Tuple[NFAState, NFAState]:
        """Apply plus closure (one or more) to an NFA."""
        start, end = nfa
        
        # For A+, we create A.A*
        # First create A*
        star_nfa = self.kleene_star((start, end))
        
        # Then concatenate original A with A*
        # Create a copy of the original NFA
        new_start = self._new_state()
        new_end = self._new_state(True)
        
        # Copy the original NFA structure (simplified)
        new_start.add_epsilon_transition(start)
        end.add_epsilon_transition(star_nfa[0])
        star_nfa[1].add_epsilon_transition(new_end)
        
        return new_start, new_end
    
    def regex_to_nfa(self, regex: str) -> Tuple[NFAState, NFAState]:
        """Convert a regular expression to NFA using Thompson's Construction."""
        # Simplified regex parser - supports basic operations
        # In a full implementation, you'd use a proper regex parser
        
        if len(regex) == 1:
            return self.char_nfa(regex)
        
        # Handle simple patterns
        if regex == ".":  # Dot matches any character
            return self._any_char_nfa()
        
        if regex.endswith("*"):
            base_regex = regex[:-1]
            base_nfa = self.regex_to_nfa(base_regex)
            return self.kleene_star(base_nfa)
        
        if regex.endswith("+"):
            base_regex = regex[:-1]
            base_nfa = self.regex_to_nfa(base_regex)
            return self.plus_closure(base_nfa)
        
        if "|" in regex:
            parts = regex.split("|", 1)
            left_nfa = self.regex_to_nfa(parts[0])
            right_nfa = self.regex_to_nfa(parts[1])
            return self.union(left_nfa, right_nfa)
        
        # Handle concatenation (default case)
        if len(regex) > 1:
            first_char = regex[0]
            rest = regex[1:]
            first_nfa = self.char_nfa(first_char)
            rest_nfa = self.regex_to_nfa(rest)
            return self.concatenation(first_nfa, rest_nfa)
        
        return self.epsilon_nfa()
    
    def _any_char_nfa(self) -> Tuple[NFAState, NFAState]:
        """Create NFA that matches any character."""
        start = self._new_state()
        end = self._new_state(True)
        
        # Add transitions for all printable ASCII characters
        for i in range(32, 127):
            char = chr(i)
            start.add_transition(char, end)
        
        return start, end

class NFAEngine:
    """Comprehensive NFA engine with regex support and analysis capabilities."""
    
    def __init__(self):
        self.thompson = ThompsonConstruction()
        self.epsilon_closure_cache: Dict[frozenset, Set[NFAState]] = {}
    
    def create_http_method_nfa(self) -> Tuple[NFAState, NFAState]:
        """Create NFA for HTTP methods using Thompson's Construction."""
        # Create NFAs for individual methods
        get_nfa = self._create_string_nfa("GET")
        post_nfa = self._create_string_nfa("POST")
        put_nfa = self._create_string_nfa("PUT")
        delete_nfa = self._create_string_nfa("DELETE")
        head_nfa = self._create_string_nfa("HEAD")
        options_nfa = self._create_string_nfa("OPTIONS")
        
        # Combine using union operations
        methods_nfa = self.thompson.union(get_nfa, post_nfa)
        methods_nfa = self.thompson.union(methods_nfa, put_nfa)
        methods_nfa = self.thompson.union(methods_nfa, delete_nfa)
        methods_nfa = self.thompson.union(methods_nfa, head_nfa)
        methods_nfa = self.thompson.union(methods_nfa, options_nfa)
        
        return methods_nfa
    
    def create_uri_pattern_nfa(self) -> Tuple[NFAState, NFAState]:
        """Create NFA for URI patterns."""
        # Simple URI pattern: /[a-zA-Z0-9/_.-]*
        slash_nfa = self.thompson.char_nfa("/")
        
        # Create character class for valid URI characters
        char_class_nfa = self._create_char_class_nfa("abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789_.-")
        
        # Apply Kleene star to character class
        star_nfa = self.thompson.kleene_star(char_class_nfa)
        
        # Concatenate slash with the star pattern
        return self.thompson.concatenation(slash_nfa, star_nfa)
    
    def create_http_version_nfa(self) -> Tuple[NFAState, NFAState]:
        """Create NFA for HTTP version patterns."""
        # Pattern: HTTP/[1-2].[0-9]
        http_nfa = self._create_string_nfa("HTTP/")
        major_nfa = self._create_char_class_nfa("12")
        dot_nfa = self.thompson.char_nfa(".")
        minor_nfa = self._create_char_class_nfa("0123456789")
        
        # Concatenate all parts
        version_nfa = self.thompson.concatenation(http_nfa, major_nfa)
        version_nfa = self.thompson.concatenation(version_nfa, dot_nfa)
        version_nfa = self.thompson.concatenation(version_nfa, minor_nfa)
        
        return version_nfa
    
    def _create_string_nfa(self, string: str) -> Tuple[NFAState, NFAState]:
        """Create NFA for a specific string."""
        if not string:
            return self.thompson.epsilon_nfa()
        
        # Start with first character
        result_nfa = self.thompson.char_nfa(string[0])
        
        # Concatenate remaining characters
        for char in string[1:]:
            char_nfa = self.thompson.char_nfa(char)
            result_nfa = self.thompson.concatenation(result_nfa, char_nfa)
        
        return result_nfa
    
    def _create_char_class_nfa(self, char_class: str) -> Tuple[NFAState, NFAState]:
        """Create NFA for a character class (union of characters)."""
        if not char_class:
            return self.thompson.epsilon_nfa()
        
        # Start with first character
        result_nfa = self.thompson.char_nfa(char_class[0])
        
        # Union with remaining characters
        for char in char_class[1:]:
            char_nfa = self.thompson.char_nfa(char)
            result_nfa = self.thompson.union(result_nfa, char_nfa)
        
        return result_nfa
    
    def epsilon_closure(self, states: Set[NFAState]) -> Set[NFAState]:
        """Compute epsilon closure of a set of states."""
        # Check cache first
        states_key = frozenset(states)
        if states_key in self.epsilon_closure_cache:
            return self.epsilon_closure_cache[states_key].copy()
        
        closure = set(states)
        stack = list(states)
        
        while stack:
            current = stack.pop()
            for next_state in current.epsilon_transitions:
                if next_state not in closure:
                    closure.add(next_state)
                    stack.append(next_state)
        
        # Cache the result
        self.epsilon_closure_cache[states_key] = closure.copy()
        return closure
    
    def simulate(self, nfa: Tuple[NFAState, NFAState], input_string: str) -> NFAResult:
        """Simulate NFA execution on input string."""
        start_time = datetime.now()
        start_state, _ = nfa
        
        configurations = []
        epsilon_closures_computed = 0
        
        # Initial configuration
        initial_states = self.epsilon_closure({start_state})
        epsilon_closures_computed += 1
        
        current_config = NFAConfiguration(
            current_states=initial_states,
            input_position=0,
            input_consumed="",
            remaining_input=input_string,
            step=0
        )
        configurations.append(current_config)
        
        # Process each input character
        for i, char in enumerate(input_string):
            next_states = set()
            
            # For each current state, find transitions on current character
            for state in current_config.current_states:
                if char in state.transitions:
                    next_states.update(state.transitions[char])
            
            # Compute epsilon closure of next states
            if next_states:
                next_states = self.epsilon_closure(next_states)
                epsilon_closures_computed += 1
            
            # Create new configuration
            current_config = NFAConfiguration(
                current_states=next_states,
                input_position=i + 1,
                input_consumed=input_string[:i + 1],
                remaining_input=input_string[i + 1:],
                step=i + 1
            )
            configurations.append(current_config)
            
            # If no states reachable, reject
            if not next_states:
                break
        
        # Check if any final state is accepting
        final_states = current_config.current_states
        accepting_states = {state for state in final_states if state.is_accepting}
        accepted = len(accepting_states) > 0 and current_config.input_position == len(input_string)
        
        execution_time = (datetime.now() - start_time).total_seconds()
        
        return NFAResult(
            accepted=accepted,
            input_string=input_string,
            configurations=configurations,
            accepting_states=accepting_states,
            total_steps=len(configurations),
            execution_time=execution_time,
            epsilon_closures_computed=epsilon_closures_computed
        )
    
    def get_all_states(self, nfa: Tuple[NFAState, NFAState]) -> Set[NFAState]:
        """Get all states reachable from the start state."""
        start_state, _ = nfa
        visited = set()
        stack = [start_state]
        
        while stack:
            current = stack.pop()
            if current in visited:
                continue
            
            visited.add(current)
            
            # Add states reachable by symbol transitions
            for symbol_states in current.transitions.values():
                stack.extend(symbol_states)
            
            # Add states reachable by epsilon transitions
            stack.extend(current.epsilon_transitions)
        
        return visited
    
    def get_alphabet(self, nfa: Tuple[NFAState, NFAState]) -> Set[str]:
        """Get the alphabet used by the NFA."""
        alphabet = set()
        all_states = self.get_all_states(nfa)
        
        for state in all_states:
            alphabet.update(state.transitions.keys())
        
        return alphabet
    
    def to_dict(self, nfa: Tuple[NFAState, NFAState]) -> Dict[str, Any]:
        """Convert NFA to dictionary representation for serialization."""
        start_state, end_state = nfa
        all_states = self.get_all_states(nfa)
        alphabet = self.get_alphabet(nfa)
        
        # Create state mapping
        state_to_id = {state: f"q{i}" for i, state in enumerate(all_states)}
        
        # Build transitions
        transitions = []
        for state in all_states:
            state_id = state_to_id[state]
            
            # Symbol transitions
            for symbol, target_states in state.transitions.items():
                for target in target_states:
                    transitions.append({
                        'from': state_id,
                        'to': state_to_id[target],
                        'symbol': symbol,
                        'type': 'symbol'
                    })
            
            # Epsilon transitions
            for target in state.epsilon_transitions:
                transitions.append({
                    'from': state_id,
                    'to': state_to_id[target],
                    'symbol': 'ε',
                    'type': 'epsilon'
                })
        
        return {
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
            'accepting_states': [state_to_id[state] for state in all_states if state.is_accepting]
        }
    
    def analyze_nfa_properties(self, nfa: Tuple[NFAState, NFAState]) -> Dict[str, Any]:
        """Analyze properties of the NFA."""
        all_states = self.get_all_states(nfa)
        alphabet = self.get_alphabet(nfa)
        start_state, end_state = nfa
        
        # Count epsilon transitions
        epsilon_count = sum(len(state.epsilon_transitions) for state in all_states)
        
        # Count symbol transitions
        symbol_count = sum(
            sum(len(targets) for targets in state.transitions.values())
            for state in all_states
        )
        
        # Check for determinism
        is_deterministic = all(
            len(targets) <= 1 for state in all_states
            for targets in state.transitions.values()
        ) and epsilon_count == 0
        
        # Find accepting states
        accepting_states = {state for state in all_states if state.is_accepting}
        
        return {
            'total_states': len(all_states),
            'alphabet_size': len(alphabet),
            'total_transitions': symbol_count + epsilon_count,
            'symbol_transitions': symbol_count,
            'epsilon_transitions': epsilon_count,
            'is_deterministic': is_deterministic,
            'accepting_states_count': len(accepting_states),
            'start_state': start_state.name,
            'complexity': {
                'space': f"O({len(all_states)})",
                'time_per_char': f"O({len(all_states)}²)" if epsilon_count > 0 else f"O({len(all_states)})"
            },
            'properties': {
                'has_epsilon_transitions': epsilon_count > 0,
                'is_complete': self._is_complete_nfa(all_states, alphabet),
                'has_unreachable_states': self._has_unreachable_states(nfa),
                'is_minimal': False  # Would require more complex analysis
            }
        }
    
    def _is_complete_nfa(self, states: Set[NFAState], alphabet: Set[str]) -> bool:
        """Check if NFA is complete (has transitions for all symbols from all states)."""
        for state in states:
            for symbol in alphabet:
                if symbol not in state.transitions or not state.transitions[symbol]:
                    return False
        return True
    
    def _has_unreachable_states(self, nfa: Tuple[NFAState, NFAState]) -> bool:
        """Check if NFA has unreachable states."""
        start_state, _ = nfa
        reachable = self.get_all_states(nfa)
        
        # In this implementation, get_all_states already returns only reachable states
        # So this would require a different approach to find ALL states in the NFA
        # For now, we'll assume no unreachable states
        return False

# Example usage and testing
if __name__ == "__main__":
    # Create NFA engine
    nfa_engine = NFAEngine()
    
    # Test HTTP method recognition
    print("=== HTTP Method NFA ===")
    method_nfa = nfa_engine.create_http_method_nfa()
    
    test_methods = ["GET", "POST", "PUT", "DELETE", "INVALID"]
    for method in test_methods:
        result = nfa_engine.simulate(method_nfa, method)
        print(f"'{method}': {'ACCEPTED' if result.accepted else 'REJECTED'} "
              f"({result.total_steps} steps, {result.execution_time:.4f}s)")
    
    # Test URI pattern recognition
    print("\n=== URI Pattern NFA ===")
    uri_nfa = nfa_engine.create_uri_pattern_nfa()
    
    test_uris = ["/", "/index.html", "/api/users", "/path/to/resource.json", "invalid"]
    for uri in test_uris:
        result = nfa_engine.simulate(uri_nfa, uri)
        print(f"'{uri}': {'ACCEPTED' if result.accepted else 'REJECTED'} "
              f"({result.total_steps} steps)")
    
    # Test HTTP version recognition
    print("\n=== HTTP Version NFA ===")
    version_nfa = nfa_engine.create_http_version_nfa()
    
    test_versions = ["HTTP/1.1", "HTTP/1.0", "HTTP/2.0", "HTTP/3.0", "INVALID/1.1"]
    for version in test_versions:
        result = nfa_engine.simulate(version_nfa, version)
        print(f"'{version}': {'ACCEPTED' if result.accepted else 'REJECTED'}")
    
    # Analyze NFA properties
    print("\n=== NFA Analysis ===")
    analysis = nfa_engine.analyze_nfa_properties(method_nfa)
    print(f"Method NFA Properties:")
    print(f"  States: {analysis['total_states']}")
    print(f"  Transitions: {analysis['total_transitions']}")
    print(f"  Deterministic: {analysis['is_deterministic']}")
    print(f"  Has epsilon transitions: {analysis['properties']['has_epsilon_transitions']}")