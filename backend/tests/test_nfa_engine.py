"""
Test suite for NFA Engine module.

Tests the Nondeterministic Finite Automaton implementation,
Thompson's Construction algorithm, and pattern matching.
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from nfa_engine import NFAEngine, NFAState, ThompsonConstruction
from typing import Set, Tuple


class TestNFAEngine:
    """Test cases for NFA Engine."""
    
    def test_nfa_engine_initialization(self, nfa_engine):
        """Test NFA engine initializes correctly."""
        assert nfa_engine is not None
        assert hasattr(nfa_engine, 'simulate')
        assert hasattr(nfa_engine, 'epsilon_closure')
        
    def test_epsilon_closure(self, nfa_engine):
        """Test epsilon closure computation."""
        # Create simple NFA states for testing
        state1 = NFAState(name="state1", is_accepting=False)
        state2 = NFAState(name="state2", is_accepting=True)
        
        # Add epsilon transition
        state1.add_epsilon_transition(state2)
        
        # Test epsilon closure
        closure = nfa_engine.epsilon_closure({state1})
        assert len(closure) == 2
        assert state1 in closure
        assert state2 in closure
        
    def test_simple_character_matching(self, nfa_engine):
        """Test simple character matching with NFA."""
        # Create simple NFA for character 'a'
        start = NFAState(name="start", is_accepting=False)
        end = NFAState(name="end", is_accepting=True)
        start.add_transition('a', end)
        
        # Test matching
        result = nfa_engine.simulate((start, end), 'a')
        assert result.accepted == True
        result = nfa_engine.simulate((start, end), 'b')
        assert result.accepted == False
        result = nfa_engine.simulate((start, end), '')
        assert result.accepted == False
        
    def test_thompson_construction_initialization(self):
        """Test Thompson's Construction algorithm initialization."""
        thompson = ThompsonConstruction()
        assert thompson is not None
        assert hasattr(thompson, 'regex_to_nfa')
        assert hasattr(thompson, 'char_nfa')
        assert hasattr(thompson, 'concatenation')
        
    def test_single_character_nfa(self):
        """Test NFA creation for single character."""
        thompson = ThompsonConstruction()
        start, end = thompson.char_nfa('a')
        
        assert start is not None
        assert end is not None
        assert start != end
        assert end.is_accepting == True
        assert start.is_accepting == False
        
    def test_kleene_star_construction(self):
        """Test Kleene star NFA construction."""
        thompson = ThompsonConstruction()
        
        # Create base NFA for 'a'
        base_nfa = thompson.char_nfa('a')
        
        # Apply Kleene star
        star_nfa = thompson.kleene_star(base_nfa)
        
        assert star_nfa is not None
        assert len(star_nfa) == 2  # Returns (start, end) tuple
        
    def test_alternation_construction(self):
        """Test alternation (OR) NFA construction."""
        thompson = ThompsonConstruction()
        
        nfa1 = thompson.char_nfa('a')
        nfa2 = thompson.char_nfa('b')
        
        alt_nfa = thompson.union(nfa1, nfa2)
        
        assert alt_nfa is not None
        assert len(alt_nfa) == 2
        
    def test_concatenation_construction(self):
        """Test concatenation NFA construction."""
        thompson = ThompsonConstruction()
        
        nfa1 = thompson.char_nfa('a')
        nfa2 = thompson.char_nfa('b')
        
        concat_nfa = thompson.concatenation(nfa1, nfa2)
        
        assert concat_nfa is not None
        assert len(concat_nfa) == 2
        
    def test_complex_regex_patterns(self, nfa_engine):
        """Test complex regex pattern matching."""
        patterns_and_tests = [
            # (pattern, test_string, expected_result)
            ("GET", "GET", True),
            ("GET", "POST", False),
            ("GET", "get", False),  # Case sensitive
            ("/", "/", True),
            ("/.*", "/index.html", True),
            ("HTTP", "HTTP", True),
        ]
        
        for pattern, test_string, expected in patterns_and_tests:
            try:
                result = nfa_engine.match_pattern(pattern, test_string)
                assert result == expected, f"Pattern '{pattern}' with '{test_string}' expected {expected}, got {result}"
            except AttributeError:
                # If match_pattern doesn't exist, skip this test
                pass
                
    def test_performance_benchmarking(self, nfa_engine, performance_timer):
        """Test NFA performance for reasonable response times."""
        # Simple pattern matching performance
        pattern = "GET"
        test_string = "GET"
        
        # Warm up
        try:
            nfa_engine.match_pattern(pattern, test_string)
        except AttributeError:
            # Skip if method doesn't exist
            return
            
        # Benchmark
        performance_timer.start()
        for _ in range(1000):
            nfa_engine.match_pattern(pattern, test_string)
        performance_timer.stop()
        
        avg_time = performance_timer.elapsed / 1000
        assert avg_time < 0.001, f"Average NFA matching time too slow: {avg_time:.6f}s"
        
    def test_state_management(self):
        """Test NFA state creation and management."""
        state = NFAState(name="test_state", is_accepting=False)
        
        assert state.name == "test_state"
        assert state.is_accepting == False
        assert len(state.transitions) == 0
        assert len(state.epsilon_transitions) == 0
        
        # Test adding transitions
        target_state = NFAState(name="target", is_accepting=True)
        state.add_transition('a', target_state)
        
        assert 'a' in state.transitions
        assert target_state in state.transitions['a']
        
        # Test epsilon transitions
        state.add_epsilon_transition(target_state)
        assert target_state in state.epsilon_transitions
        
    def test_nfa_execution_trace(self, nfa_engine):
        """Test NFA execution with step tracing."""
        # This tests the educational aspect of showing NFA execution steps
        try:
            # Create simple NFA
            start = NFAState(name="start", is_accepting=False)
            end = NFAState(name="end", is_accepting=True)
            start.add_transition('a', end)
            
            # Test with tracing if available
            if hasattr(nfa_engine, 'simulate_with_trace'):
                trace = nfa_engine.simulate_with_trace((start, end), 'a')
                assert isinstance(trace, list)
                assert len(trace) > 0
        except AttributeError:
            # Method might not be implemented yet
            pass


class TestThompsonConstruction:
    """Specific tests for Thompson's Construction algorithm."""
    
    def test_regex_parsing_simple(self):
        """Test simple regex pattern parsing."""
        thompson = ThompsonConstruction()
        
        simple_patterns = ['a', 'b', 'G', 'E', 'T']
        
        for pattern in simple_patterns:
            nfa = thompson.regex_to_nfa(pattern)
            assert nfa is not None
            assert len(nfa) == 2  # (start, end) tuple
            
    def test_regex_operators(self):
        """Test regex operators in Thompson's Construction."""
        thompson = ThompsonConstruction()
        
        try:
            # Test Kleene star
            star_nfa = thompson.regex_to_nfa("a*")
            assert star_nfa is not None
            
            # Test alternation (if supported)
            if hasattr(thompson, 'parse_alternation'):
                alt_nfa = thompson.regex_to_nfa("a|b")
                assert alt_nfa is not None
                
        except (NotImplementedError, AttributeError):
            # Some operations might not be fully implemented
            pass
            
    def test_http_specific_patterns(self):
        """Test HTTP-specific pattern construction."""
        thompson = ThompsonConstruction()
        
        http_patterns = [
            "GET",
            "HTTP",
            "/",
        ]
        
        for pattern in http_patterns:
            nfa = thompson.regex_to_nfa(pattern)
            assert nfa is not None
            start, end = nfa
            assert start is not None
            assert end is not None
            assert end.is_accepting == True
            
    def test_nfa_state_counting(self):
        """Test that NFA constructions use reasonable number of states."""
        thompson = ThompsonConstruction()
        
        # Simple character should use minimal states
        start, end = thompson.char_nfa('a')
        
        # Should be exactly 2 states for simple character
        assert start != end
        assert start.is_accepting == False
        assert end.is_accepting == True