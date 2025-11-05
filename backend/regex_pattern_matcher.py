"""
Comprehensive Regex Pattern Matching Engine

This module provides a complete regex pattern matching system using both NFA and DFA
approaches, demonstrating the practical application of formal language automata theory
in HTTP protocol analysis and general pattern matching.
"""

import re
from typing import Dict, List, Set, Optional, Tuple, Any, Union, Pattern
from dataclasses import dataclass, field
from enum import Enum
from datetime import datetime
import time

from nfa_engine import NFAEngine, NFAState, NFAResult, ThompsonConstruction
from dfa_engine import DFAEngine, DFAState, DFAResult

class MatchMethod(Enum):
    NFA_SIMULATION = "nfa_simulation"
    DFA_SIMULATION = "dfa_simulation"
    PYTHON_REGEX = "python_regex"
    HYBRID = "hybrid"

class PatternType(Enum):
    HTTP_METHOD = "http_method"
    URI_PATH = "uri_path"
    HTTP_VERSION = "http_version"
    HEADER_NAME = "header_name"
    HEADER_VALUE = "header_value"
    EMAIL = "email"
    IP_ADDRESS = "ip_address"
    CUSTOM = "custom"

@dataclass
class MatchResult:
    """Result of pattern matching."""
    matched: bool
    pattern: str
    input_string: str
    method: MatchMethod
    match_start: int
    match_end: int
    matched_text: str
    execution_time: float
    steps: int
    groups: List[str] = field(default_factory=list)
    metadata: Dict[str, Any] = field(default_factory=dict)

@dataclass
class PatternPerformance:
    """Performance comparison between different matching methods."""
    pattern: str
    test_string: str
    nfa_time: float
    dfa_time: float
    python_regex_time: float
    nfa_steps: int
    dfa_steps: int
    all_match: bool
    speed_factor: Dict[str, float] = field(default_factory=dict)

class RegexPatternMatcher:
    """Comprehensive regex pattern matching engine."""
    
    def __init__(self):
        self.nfa_engine = NFAEngine()
        self.dfa_engine = DFAEngine()
        self.thompson = ThompsonConstruction()
        
        # Predefined patterns for HTTP analysis
        self.http_patterns = {
            PatternType.HTTP_METHOD: r"GET|POST|PUT|DELETE|HEAD|OPTIONS|PATCH|TRACE|CONNECT",
            PatternType.URI_PATH: r"/[a-zA-Z0-9/_.\-]*",
            PatternType.HTTP_VERSION: r"HTTP/[1-2]\.[0-9]",
            PatternType.HEADER_NAME: r"[a-zA-Z0-9\-]+",
            PatternType.HEADER_VALUE: r"[^\r\n]*",
            PatternType.EMAIL: r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}",
            PatternType.IP_ADDRESS: r"\b(?:[0-9]{1,3}\.){3}[0-9]{1,3}\b"
        }
        
        # Compiled Python regex patterns for comparison
        self.compiled_patterns = {
            pattern_type: re.compile(pattern)
            for pattern_type, pattern in self.http_patterns.items()
        }
    
    def match(self, pattern: str, text: str, method: MatchMethod = MatchMethod.HYBRID) -> MatchResult:
        """
        Match a pattern against text using the specified method.
        
        Args:
            pattern: Regular expression pattern
            text: Input text to match against
            method: Method to use for matching
            
        Returns:
            MatchResult with detailed information about the match
        """
        start_time = time.perf_counter()
        
        if method == MatchMethod.NFA_SIMULATION:
            return self._match_with_nfa(pattern, text)
        elif method == MatchMethod.DFA_SIMULATION:
            return self._match_with_dfa(pattern, text)
        elif method == MatchMethod.PYTHON_REGEX:
            return self._match_with_python_regex(pattern, text)
        elif method == MatchMethod.HYBRID:
            return self._match_hybrid(pattern, text)
        else:
            raise ValueError(f"Unknown matching method: {method}")
    
    def match_http_component(self, component_type: PatternType, text: str, 
                           method: MatchMethod = MatchMethod.HYBRID) -> MatchResult:
        """Match specific HTTP component using predefined patterns."""
        if component_type not in self.http_patterns:
            raise ValueError(f"Unknown HTTP component type: {component_type}")
        
        pattern = self.http_patterns[component_type]
        result = self.match(pattern, text, method)
        result.metadata['component_type'] = component_type.value
        
        return result
    
    def _match_with_nfa(self, pattern: str, text: str) -> MatchResult:
        """Match using NFA simulation."""
        start_time = time.perf_counter()
        
        try:
            # Convert regex to NFA using Thompson's Construction
            nfa = self.thompson.regex_to_nfa(pattern)
            
            # Try to match at each position in the text
            for start_pos in range(len(text)):
                for end_pos in range(start_pos + 1, len(text) + 1):
                    substring = text[start_pos:end_pos]
                    result = self.nfa_engine.simulate(nfa, substring)
                    
                    if result.accepted:
                        execution_time = time.perf_counter() - start_time
                        return MatchResult(
                            matched=True,
                            pattern=pattern,
                            input_string=text,
                            method=MatchMethod.NFA_SIMULATION,
                            match_start=start_pos,
                            match_end=end_pos,
                            matched_text=substring,
                            execution_time=execution_time,
                            steps=result.total_steps,
                            metadata={'nfa_configurations': len(result.configurations)}
                        )
            
            # No match found
            execution_time = time.perf_counter() - start_time
            return MatchResult(
                matched=False,
                pattern=pattern,
                input_string=text,
                method=MatchMethod.NFA_SIMULATION,
                match_start=-1,
                match_end=-1,
                matched_text="",
                execution_time=execution_time,
                steps=0
            )
            
        except Exception as e:
            execution_time = time.perf_counter() - start_time
            return MatchResult(
                matched=False,
                pattern=pattern,
                input_string=text,
                method=MatchMethod.NFA_SIMULATION,
                match_start=-1,
                match_end=-1,
                matched_text="",
                execution_time=execution_time,
                steps=0,
                metadata={'error': str(e)}
            )
    
    def _match_with_dfa(self, pattern: str, text: str) -> MatchResult:
        """Match using DFA simulation."""
        start_time = time.perf_counter()
        
        try:
            # Convert regex to NFA, then to DFA
            nfa = self.thompson.regex_to_nfa(pattern)
            dfa = self.dfa_engine.create_dfa_from_nfa(nfa)
            
            # Try to match at each position in the text
            for start_pos in range(len(text)):
                for end_pos in range(start_pos + 1, len(text) + 1):
                    substring = text[start_pos:end_pos]
                    result = self.dfa_engine.simulate(dfa, substring)
                    
                    if result.accepted:
                        execution_time = time.perf_counter() - start_time
                        return MatchResult(
                            matched=True,
                            pattern=pattern,
                            input_string=text,
                            method=MatchMethod.DFA_SIMULATION,
                            match_start=start_pos,
                            match_end=end_pos,
                            matched_text=substring,
                            execution_time=execution_time,
                            steps=result.total_steps,
                            metadata={'dfa_path': result.path}
                        )
            
            # No match found
            execution_time = time.perf_counter() - start_time
            return MatchResult(
                matched=False,
                pattern=pattern,
                input_string=text,
                method=MatchMethod.DFA_SIMULATION,
                match_start=-1,
                match_end=-1,
                matched_text="",
                execution_time=execution_time,
                steps=0
            )
            
        except Exception as e:
            execution_time = time.perf_counter() - start_time
            return MatchResult(
                matched=False,
                pattern=pattern,
                input_string=text,
                method=MatchMethod.DFA_SIMULATION,
                match_start=-1,
                match_end=-1,
                matched_text="",
                execution_time=execution_time,
                steps=0,
                metadata={'error': str(e)}
            )
    
    def _match_with_python_regex(self, pattern: str, text: str) -> MatchResult:
        """Match using Python's built-in regex engine."""
        start_time = time.perf_counter()
        
        try:
            compiled_pattern = re.compile(pattern)
            match = compiled_pattern.search(text)
            
            execution_time = time.perf_counter() - start_time
            
            if match:
                return MatchResult(
                    matched=True,
                    pattern=pattern,
                    input_string=text,
                    method=MatchMethod.PYTHON_REGEX,
                    match_start=match.start(),
                    match_end=match.end(),
                    matched_text=match.group(0),
                    execution_time=execution_time,
                    steps=1,  # Python regex is optimized, we can't count actual steps
                    groups=list(match.groups()),
                    metadata={'full_match': match.group(0)}
                )
            else:
                return MatchResult(
                    matched=False,
                    pattern=pattern,
                    input_string=text,
                    method=MatchMethod.PYTHON_REGEX,
                    match_start=-1,
                    match_end=-1,
                    matched_text="",
                    execution_time=execution_time,
                    steps=0
                )
                
        except Exception as e:
            execution_time = time.perf_counter() - start_time
            return MatchResult(
                matched=False,
                pattern=pattern,
                input_string=text,
                method=MatchMethod.PYTHON_REGEX,
                match_start=-1,
                match_end=-1,
                matched_text="",
                execution_time=execution_time,
                steps=0,
                metadata={'error': str(e)}
            )
    
    def _match_hybrid(self, pattern: str, text: str) -> MatchResult:
        """
        Hybrid matching: choose the best method based on pattern complexity.
        Simple patterns use DFA, complex patterns use Python regex.
        """
        # Heuristic: if pattern is simple (no complex features), use DFA
        # Otherwise, use Python regex
        
        complex_features = [r'\d', r'\w', r'\s', r'+', r'?', r'{', r'}', r'(', r')', r'[', r']']
        is_complex = any(feature in pattern for feature in complex_features)
        
        if is_complex or len(pattern) > 20:
            # Use Python regex for complex patterns
            result = self._match_with_python_regex(pattern, text)
            result.metadata['hybrid_choice'] = 'python_regex'
            result.metadata['reason'] = 'complex_pattern'
        else:
            # Try DFA for simple patterns
            try:
                result = self._match_with_dfa(pattern, text)
                result.metadata['hybrid_choice'] = 'dfa'
                result.metadata['reason'] = 'simple_pattern'
            except:
                # Fallback to Python regex if DFA fails
                result = self._match_with_python_regex(pattern, text)
                result.metadata['hybrid_choice'] = 'python_regex_fallback'
                result.metadata['reason'] = 'dfa_failed'
        
        result.method = MatchMethod.HYBRID
        return result
    
    def compare_methods(self, pattern: str, text: str) -> PatternPerformance:
        """Compare performance of different matching methods."""
        # Test NFA
        nfa_result = self._match_with_nfa(pattern, text)
        
        # Test DFA
        dfa_result = self._match_with_dfa(pattern, text)
        
        # Test Python regex
        python_result = self._match_with_python_regex(pattern, text)
        
        # Check if all methods agree
        all_match = (nfa_result.matched == dfa_result.matched == python_result.matched)
        
        # Calculate speed factors
        times = [nfa_result.execution_time, dfa_result.execution_time, python_result.execution_time]
        min_time = min(t for t in times if t > 0)
        
        speed_factor = {
            'nfa_vs_fastest': nfa_result.execution_time / min_time if min_time > 0 else 1.0,
            'dfa_vs_fastest': dfa_result.execution_time / min_time if min_time > 0 else 1.0,
            'python_vs_fastest': python_result.execution_time / min_time if min_time > 0 else 1.0
        }
        
        return PatternPerformance(
            pattern=pattern,
            test_string=text,
            nfa_time=nfa_result.execution_time,
            dfa_time=dfa_result.execution_time,
            python_regex_time=python_result.execution_time,
            nfa_steps=nfa_result.steps,
            dfa_steps=dfa_result.steps,
            all_match=all_match,
            speed_factor=speed_factor
        )
    
    def validate_http_request_line(self, request_line: str) -> Dict[str, MatchResult]:
        """Validate an HTTP request line using pattern matching."""
        parts = request_line.strip().split(' ')
        
        if len(parts) != 3:
            return {
                'valid': MatchResult(
                    matched=False,
                    pattern="complete_request_line",
                    input_string=request_line,
                    method=MatchMethod.HYBRID,
                    match_start=-1,
                    match_end=-1,
                    matched_text="",
                    execution_time=0.0,
                    steps=0,
                    metadata={'error': 'Invalid number of parts'}
                )
            }
        
        method, uri, version = parts
        
        # Validate each component
        results = {}
        results['method'] = self.match_http_component(PatternType.HTTP_METHOD, method)
        results['uri'] = self.match_http_component(PatternType.URI_PATH, uri)
        results['version'] = self.match_http_component(PatternType.HTTP_VERSION, version)
        
        # Overall validation
        all_valid = all(result.matched for result in results.values())
        results['valid'] = MatchResult(
            matched=all_valid,
            pattern="complete_request_line",
            input_string=request_line,
            method=MatchMethod.HYBRID,
            match_start=0 if all_valid else -1,
            match_end=len(request_line) if all_valid else -1,
            matched_text=request_line if all_valid else "",
            execution_time=sum(r.execution_time for r in results.values()),
            steps=sum(r.steps for r in results.values()),
            metadata={
                'components_valid': {k: v.matched for k, v in results.items() if k != 'valid'},
                'method_matched': results['method'].matched_text,
                'uri_matched': results['uri'].matched_text,
                'version_matched': results['version'].matched_text
            }
        )
        
        return results
    
    def benchmark_pattern_matching(self, test_cases: List[Tuple[str, str]]) -> Dict[str, Any]:
        """Benchmark pattern matching performance across different methods."""
        results = {
            'total_tests': len(test_cases),
            'method_performance': {
                'nfa': {'total_time': 0.0, 'total_steps': 0, 'matches': 0},
                'dfa': {'total_time': 0.0, 'total_steps': 0, 'matches': 0},
                'python_regex': {'total_time': 0.0, 'total_steps': 0, 'matches': 0}
            },
            'detailed_results': [],
            'recommendations': []
        }
        
        for pattern, text in test_cases:
            performance = self.compare_methods(pattern, text)
            results['detailed_results'].append(performance)
            
            # Update totals
            results['method_performance']['nfa']['total_time'] += performance.nfa_time
            results['method_performance']['nfa']['total_steps'] += performance.nfa_steps
            
            results['method_performance']['dfa']['total_time'] += performance.dfa_time
            results['method_performance']['dfa']['total_steps'] += performance.dfa_steps
            
            results['method_performance']['python_regex']['total_time'] += performance.python_regex_time
        
        # Generate recommendations
        avg_nfa_time = results['method_performance']['nfa']['total_time'] / len(test_cases)
        avg_dfa_time = results['method_performance']['dfa']['total_time'] / len(test_cases)
        avg_python_time = results['method_performance']['python_regex']['total_time'] / len(test_cases)
        
        fastest_method = min([
            ('nfa', avg_nfa_time),
            ('dfa', avg_dfa_time),
            ('python_regex', avg_python_time)
        ], key=lambda x: x[1])
        
        results['recommendations'] = [
            f"Fastest method overall: {fastest_method[0]} (avg {fastest_method[1]:.6f}s)",
            f"For simple patterns: Prefer DFA or NFA for educational value",
            f"For complex patterns: Use Python regex for reliability",
            f"For production: Use hybrid approach for optimal performance"
        ]
        
        # Calculate averages
        for method_data in results['method_performance'].values():
            method_data['avg_time'] = method_data['total_time'] / len(test_cases)
            method_data['avg_steps'] = method_data['total_steps'] / len(test_cases)
        
        return results
    
    def get_pattern_suggestions(self, pattern_type: PatternType) -> Dict[str, Any]:
        """Get pattern suggestions and examples for HTTP components."""
        suggestions = {
            PatternType.HTTP_METHOD: {
                'pattern': self.http_patterns[PatternType.HTTP_METHOD],
                'description': 'Matches standard HTTP methods',
                'examples': ['GET', 'POST', 'PUT', 'DELETE'],
                'anti_examples': ['get', 'PATCH', 'INVALID']
            },
            PatternType.URI_PATH: {
                'pattern': self.http_patterns[PatternType.URI_PATH],
                'description': 'Matches URI paths starting with /',
                'examples': ['/', '/index.html', '/api/users/123'],
                'anti_examples': ['index.html', 'api/users', '']
            },
            PatternType.HTTP_VERSION: {
                'pattern': self.http_patterns[PatternType.HTTP_VERSION],
                'description': 'Matches HTTP version identifiers',
                'examples': ['HTTP/1.0', 'HTTP/1.1', 'HTTP/2.0'],
                'anti_examples': ['HTTP/3.0', 'http/1.1', 'HTTP/1']
            }
        }
        
        return suggestions.get(pattern_type, {
            'pattern': 'No predefined pattern',
            'description': 'Custom pattern type',
            'examples': [],
            'anti_examples': []
        })

# Example usage and testing
if __name__ == "__main__":
    matcher = RegexPatternMatcher()
    
    # Test HTTP request line validation
    print("=== HTTP Request Line Validation ===")
    test_requests = [
        "GET /index.html HTTP/1.1",
        "POST /api/users HTTP/1.0",
        "INVALID /path HTTP/1.1",
        "GET invalid_uri HTTP/1.1",
        "GET /path INVALID_VERSION"
    ]
    
    for request in test_requests:
        results = matcher.validate_http_request_line(request)
        valid = results['valid']
        print(f"'{request}': {'VALID' if valid.matched else 'INVALID'}")
        if not valid.matched and 'error' in valid.metadata:
            print(f"  Error: {valid.metadata['error']}")
    
    # Test method comparison
    print("\n=== Method Performance Comparison ===")
    test_cases = [
        ("GET", "GET"),
        ("POST|PUT", "POST"),
        (r"/[a-z]+", "/index"),
        (r"HTTP/[12]\.[0-9]", "HTTP/1.1")
    ]
    
    for pattern, text in test_cases:
        performance = matcher.compare_methods(pattern, text)
        print(f"Pattern '{pattern}' on '{text}':")
        print(f"  NFA: {performance.nfa_time:.6f}s ({performance.nfa_steps} steps)")
        print(f"  DFA: {performance.dfa_time:.6f}s ({performance.dfa_steps} steps)")
        print(f"  Python: {performance.python_regex_time:.6f}s")
        print(f"  All match: {performance.all_match}")
    
    # Benchmark
    print("\n=== Benchmark Results ===")
    benchmark = matcher.benchmark_pattern_matching(test_cases)
    print(f"Total tests: {benchmark['total_tests']}")
    for method, data in benchmark['method_performance'].items():
        print(f"{method}: avg {data['avg_time']:.6f}s, {data['avg_steps']} steps")
    
    for recommendation in benchmark['recommendations']:
        print(f"• {recommendation}")