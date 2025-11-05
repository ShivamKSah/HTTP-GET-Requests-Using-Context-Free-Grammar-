"""
Comprehensive Security and Input Validation System for CFG QODER

This module provides security measures including input sanitization,
rate limiting, request validation, and protection against common attacks.
"""

import re
import html
import hashlib
import time
import ipaddress
from typing import Dict, List, Optional, Any, Union, Tuple
from functools import wraps
from datetime import datetime, timedelta
from flask import request, jsonify, g
from werkzeug.exceptions import BadRequest, RequestEntityTooLarge
import json
from collections import defaultdict, deque
import threading


class SecurityConfig:
    """Security configuration settings."""
    
    # Rate limiting settings
    DEFAULT_RATE_LIMIT = 100  # requests per hour
    RATE_LIMIT_WINDOW = 3600  # 1 hour in seconds
    BURST_LIMIT = 10  # requests per minute for burst protection
    BURST_WINDOW = 60  # 1 minute in seconds
    
    # Input validation settings
    MAX_REQUEST_SIZE = 16 * 1024 * 1024  # 16MB
    MAX_TEXT_LENGTH = 50000  # Maximum text length for NLP processing
    MAX_BATCH_SIZE = 100  # Maximum batch processing size
    MAX_PATTERN_LENGTH = 1000  # Maximum regex pattern length
    
    # Security headers
    SECURITY_HEADERS = {
        'X-Content-Type-Options': 'nosniff',
        'X-Frame-Options': 'DENY',
        'X-XSS-Protection': '1; mode=block',
        'Strict-Transport-Security': 'max-age=31536000; includeSubDomains',
        'Content-Security-Policy': "default-src 'self'; script-src 'self' 'unsafe-inline'",
        'Referrer-Policy': 'strict-origin-when-cross-origin'
    }
    
    # Allowed origins for CORS
    ALLOWED_ORIGINS = [
        'http://localhost:3000',
        'http://localhost:5174',
        'http://127.0.0.1:3000',
        'http://127.0.0.1:5174'
    ]
    
    # Blocked patterns for malicious input detection
    MALICIOUS_PATTERNS = [
        r'<script[^>]*>.*?</script>',  # XSS attempts
        r'javascript:',  # JavaScript protocol
        r'on\w+\s*=',  # Event handlers
        r'eval\s*\(',  # Code evaluation
        r'exec\s*\(',  # Code execution
        r'import\s+',  # Import statements
        r'__import__',  # Python imports
        r'subprocess',  # Subprocess calls
        r'os\.',  # OS module access
        r'file://',  # File protocol
        r'\.\./',  # Directory traversal
        r'union\s+select',  # SQL injection
        r'drop\s+table',  # SQL injection
        r'delete\s+from',  # SQL injection
    ]


class RateLimiter:
    """Advanced rate limiting with multiple strategies."""
    
    def __init__(self):
        self.requests = defaultdict(deque)
        self.blocked_ips = {}
        self.lock = threading.Lock()
    
    def is_allowed(self, identifier: str, limit: int = None, window: int = None) -> Tuple[bool, Dict[str, Any]]:
        """
        Check if request is allowed based on rate limiting rules.
        
        Args:
            identifier: Unique identifier (IP address, user ID, etc.)
            limit: Requests per window (defaults to SecurityConfig.DEFAULT_RATE_LIMIT)
            window: Time window in seconds (defaults to SecurityConfig.RATE_LIMIT_WINDOW)
            
        Returns:
            Tuple of (is_allowed, rate_limit_info)
        """
        if limit is None:
            limit = SecurityConfig.DEFAULT_RATE_LIMIT
        if window is None:
            window = SecurityConfig.RATE_LIMIT_WINDOW
            
        current_time = time.time()
        
        with self.lock:
            # Check if IP is temporarily blocked
            if identifier in self.blocked_ips:
                if current_time < self.blocked_ips[identifier]:
                    return False, {
                        'blocked': True,
                        'blocked_until': self.blocked_ips[identifier],
                        'reason': 'Temporarily blocked due to suspicious activity'
                    }
                else:
                    del self.blocked_ips[identifier]
            
            # Clean old requests outside the window
            request_times = self.requests[identifier]
            while request_times and request_times[0] <= current_time - window:
                request_times.popleft()
            
            # Check rate limit
            if len(request_times) >= limit:
                # Block IP for additional time if consistently hitting limits
                if len(request_times) >= limit * 1.5:
                    self.blocked_ips[identifier] = current_time + 300  # 5 minute block
                
                return False, {
                    'rate_limited': True,
                    'limit': limit,
                    'window': window,
                    'requests_made': len(request_times),
                    'reset_time': request_times[0] + window,
                    'retry_after': int(request_times[0] + window - current_time)
                }
            
            # Add current request
            request_times.append(current_time)
            
            return True, {
                'rate_limited': False,
                'limit': limit,
                'window': window,
                'requests_made': len(request_times),
                'requests_remaining': limit - len(request_times),
                'reset_time': current_time + window
            }
    
    def get_stats(self) -> Dict[str, Any]:
        """Get rate limiting statistics."""
        with self.lock:
            return {
                'active_clients': len(self.requests),
                'blocked_ips': len(self.blocked_ips),
                'total_requests': sum(len(reqs) for reqs in self.requests.values())
            }


class InputValidator:
    """Comprehensive input validation and sanitization."""
    
    @staticmethod
    def sanitize_text(text: str, max_length: int = None) -> str:
        """
        Sanitize text input to prevent XSS and other attacks.
        
        Args:
            text: Input text to sanitize
            max_length: Maximum allowed length
            
        Returns:
            Sanitized text
            
        Raises:
            ValueError: If text fails validation
        """
        if not isinstance(text, str):
            raise ValueError("Input must be a string")
        
        if max_length and len(text) > max_length:
            raise ValueError(f"Text length exceeds maximum of {max_length} characters")
        
        # HTML escape to prevent XSS
        sanitized = html.escape(text)
        
        # Check for malicious patterns
        for pattern in SecurityConfig.MALICIOUS_PATTERNS:
            if re.search(pattern, sanitized, re.IGNORECASE):
                raise ValueError(f"Potentially malicious content detected")
        
        # Remove null bytes and control characters
        sanitized = re.sub(r'[\x00-\x08\x0B\x0C\x0E-\x1F\x7F]', '', sanitized)
        
        return sanitized.strip()
    
    @staticmethod
    def validate_http_request(request_line: str) -> str:
        """
        Validate and sanitize HTTP request line.
        
        Args:
            request_line: HTTP request line to validate
            
        Returns:
            Validated request line
            
        Raises:
            ValueError: If request line is invalid
        """
        if not request_line or not isinstance(request_line, str):
            raise ValueError("Request line must be a non-empty string")
        
        # Basic length check
        if len(request_line) > 8192:  # Maximum HTTP request line length
            raise ValueError("Request line too long")
        
        # Check for null bytes and control characters
        if re.search(r'[\x00-\x08\x0B\x0C\x0E-\x1F]', request_line):
            raise ValueError("Request line contains invalid characters")
        
        # Validate basic HTTP structure
        parts = request_line.strip().split()
        if len(parts) != 3:
            raise ValueError("Invalid HTTP request format")
        
        method, uri, version = parts
        
        # Validate HTTP method
        valid_methods = ['GET', 'POST', 'PUT', 'DELETE', 'HEAD', 'OPTIONS', 'PATCH']
        if method not in valid_methods:
            raise ValueError(f"Invalid HTTP method: {method}")
        
        # Validate URI
        if not uri.startswith('/'):
            raise ValueError("URI must start with '/'")
        
        # Check for directory traversal
        if '../' in uri or '..\\' in uri:
            raise ValueError("Directory traversal detected in URI")
        
        # Validate HTTP version
        if not re.match(r'^HTTP/[12]\.[01]$', version):
            raise ValueError(f"Invalid HTTP version: {version}")
        
        return request_line.strip()
    
    @staticmethod
    def validate_regex_pattern(pattern: str) -> str:
        """
        Validate regex pattern for security and complexity.
        
        Args:
            pattern: Regex pattern to validate
            
        Returns:
            Validated pattern
            
        Raises:
            ValueError: If pattern is invalid or potentially dangerous
        """
        if not pattern or not isinstance(pattern, str):
            raise ValueError("Pattern must be a non-empty string")
        
        if len(pattern) > SecurityConfig.MAX_PATTERN_LENGTH:
            raise ValueError(f"Pattern too long (max {SecurityConfig.MAX_PATTERN_LENGTH} chars)")
        
        # Check for catastrophic backtracking patterns
        dangerous_patterns = [
            r'\(\?\:.*\)\*\+',  # Nested quantifiers
            r'\(\.\*\)\+',      # Exponential backtracking
            r'\(\w\+\)\+',      # Repeated groups
        ]
        
        for dangerous in dangerous_patterns:
            if re.search(dangerous, pattern):
                raise ValueError("Pattern may cause catastrophic backtracking")
        
        # Try to compile the pattern
        try:
            re.compile(pattern)
        except re.error as e:
            raise ValueError(f"Invalid regex pattern: {e}")
        
        return pattern
    
    @staticmethod
    def validate_json_payload(data: Any, max_size: int = None) -> Dict[str, Any]:
        """
        Validate JSON payload.
        
        Args:
            data: JSON data to validate
            max_size: Maximum payload size in bytes
            
        Returns:
            Validated JSON data
            
        Raises:
            ValueError: If payload is invalid
        """
        if max_size and len(str(data)) > max_size:
            raise ValueError(f"Payload too large (max {max_size} bytes)")
        
        if not isinstance(data, dict):
            raise ValueError("Payload must be a JSON object")
        
        # Recursively sanitize string values
        def sanitize_recursive(obj):
            if isinstance(obj, dict):
                return {k: sanitize_recursive(v) for k, v in obj.items()}
            elif isinstance(obj, list):
                return [sanitize_recursive(item) for item in obj]
            elif isinstance(obj, str):
                return InputValidator.sanitize_text(obj)
            else:
                return obj
        
        return sanitize_recursive(data)


class SecurityMiddleware:
    """Security middleware for Flask applications."""
    
    def __init__(self, app=None):
        self.rate_limiter = RateLimiter()
        if app:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize security middleware with Flask app."""
        app.before_request(self.before_request)
        app.after_request(self.after_request)
    
    def before_request(self):
        """Execute before each request."""
        # Check content length
        if request.content_length and request.content_length > SecurityConfig.MAX_REQUEST_SIZE:
            raise RequestEntityTooLarge("Request entity too large")
        
        # Get client identifier
        client_ip = self.get_client_ip()
        
        # Rate limiting
        allowed, rate_info = self.rate_limiter.is_allowed(client_ip)
        if not allowed:
            response = jsonify({
                'error': 'Rate limit exceeded',
                'rate_limit_info': rate_info
            })
            response.status_code = 429
            return response
        
        # Store rate limit info for headers
        g.rate_limit_info = rate_info
        g.client_ip = client_ip
    
    def after_request(self, response):
        """Execute after each request."""
        # Add security headers
        for header, value in SecurityConfig.SECURITY_HEADERS.items():
            response.headers[header] = value
        
        # Add rate limit headers
        if hasattr(g, 'rate_limit_info'):
            info = g.rate_limit_info
            response.headers['X-RateLimit-Limit'] = str(info.get('limit', 0))
            response.headers['X-RateLimit-Remaining'] = str(info.get('requests_remaining', 0))
            response.headers['X-RateLimit-Reset'] = str(int(info.get('reset_time', 0)))
        
        return response
    
    def get_client_ip(self) -> str:
        """Get client IP address, handling proxies."""
        # Check for forwarded headers (be careful with these in production)
        forwarded_ips = request.headers.get('X-Forwarded-For', '').split(',')
        if forwarded_ips and forwarded_ips[0].strip():
            return forwarded_ips[0].strip()
        
        return request.remote_addr or 'unknown'


def rate_limit(limit: int = None, per: int = None, key_func=None):
    """
    Decorator for applying rate limits to specific endpoints.
    
    Args:
        limit: Number of requests allowed
        per: Time period in seconds
        key_func: Function to generate rate limit key
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            # Get rate limiter instance
            from flask import current_app
            security_middleware = getattr(current_app, '_security_middleware', None)
            if not security_middleware:
                return f(*args, **kwargs)
            
            # Get rate limit key
            if key_func:
                key = key_func()
            else:
                key = getattr(g, 'client_ip', request.remote_addr or 'unknown')
            
            # Check rate limit
            rate_limit_limit = limit or SecurityConfig.DEFAULT_RATE_LIMIT
            rate_limit_window = per or SecurityConfig.RATE_LIMIT_WINDOW
            
            allowed, rate_info = security_middleware.rate_limiter.is_allowed(
                key, rate_limit_limit, rate_limit_window
            )
            
            if not allowed:
                response = jsonify({
                    'error': 'Rate limit exceeded for this endpoint',
                    'rate_limit_info': rate_info
                })
                response.status_code = 429
                return response
            
            return f(*args, **kwargs)
        return wrapper
    return decorator


def validate_input(**validators):
    """
    Decorator for input validation.
    
    Usage:
        @validate_input(
            request_line=InputValidator.validate_http_request,
            pattern=InputValidator.validate_regex_pattern
        )
        def my_endpoint():
            pass
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            if request.is_json:
                data = request.get_json()
                
                for field, validator in validators.items():
                    if field in data:
                        try:
                            data[field] = validator(data[field])
                        except ValueError as e:
                            return jsonify({
                                'error': f'Invalid {field}: {str(e)}',
                                'field': field
                            }), 400
                
                # Replace request data with validated data
                request._cached_json = data
            
            return f(*args, **kwargs)
        return wrapper
    return decorator


def security_headers(additional_headers: Dict[str, str] = None):
    """
    Decorator to add custom security headers.
    
    Args:
        additional_headers: Additional headers to add
    """
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            response = f(*args, **kwargs)
            
            if additional_headers:
                for header, value in additional_headers.items():
                    response.headers[header] = value
            
            return response
        return wrapper
    return decorator


class SecurityAuditLogger:
    """Security audit logging for suspicious activities."""
    
    def __init__(self):
        self.suspicious_activities = deque(maxlen=1000)
        self.lock = threading.Lock()
    
    def log_suspicious_activity(self, 
                              activity_type: str,
                              client_ip: str, 
                              details: Dict[str, Any],
                              severity: str = 'medium'):
        """Log suspicious security activity."""
        with self.lock:
            activity = {
                'timestamp': datetime.utcnow().isoformat(),
                'type': activity_type,
                'client_ip': client_ip,
                'details': details,
                'severity': severity,
                'user_agent': request.headers.get('User-Agent', 'Unknown')
            }
            self.suspicious_activities.append(activity)
    
    def get_recent_activities(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Get recent suspicious activities."""
        with self.lock:
            return list(self.suspicious_activities)[-limit:]
    
    def get_activity_summary(self) -> Dict[str, Any]:
        """Get summary of security activities."""
        with self.lock:
            activities = list(self.suspicious_activities)
            
            summary = {
                'total_activities': len(activities),
                'by_type': defaultdict(int),
                'by_severity': defaultdict(int),
                'by_ip': defaultdict(int),
                'recent_24h': 0
            }
            
            cutoff_time = datetime.utcnow() - timedelta(hours=24)
            
            for activity in activities:
                summary['by_type'][activity['type']] += 1
                summary['by_severity'][activity['severity']] += 1
                summary['by_ip'][activity['client_ip']] += 1
                
                activity_time = datetime.fromisoformat(activity['timestamp'])
                if activity_time > cutoff_time:
                    summary['recent_24h'] += 1
            
            return dict(summary)


# Global instances
security_middleware = SecurityMiddleware()
audit_logger = SecurityAuditLogger()


def init_security(app):
    """Initialize security components with Flask app."""
    security_middleware.init_app(app)
    app._security_middleware = security_middleware
    app._audit_logger = audit_logger
    
    return security_middleware, audit_logger


# Example usage in Flask routes
def create_secure_endpoints(app):
    """Create security-related endpoints."""
    
    @app.route('/api/security/stats')
    @rate_limit(limit=10, per=60)  # 10 requests per minute
    def security_stats():
        """Get security statistics."""
        rate_stats = security_middleware.rate_limiter.get_stats()
        audit_stats = audit_logger.get_activity_summary()
        
        return jsonify({
            'rate_limiting': rate_stats,
            'security_audit': audit_stats,
            'timestamp': datetime.utcnow().isoformat()
        })
    
    @app.route('/api/security/audit')
    @rate_limit(limit=5, per=60)  # 5 requests per minute
    def security_audit():
        """Get recent security audit logs."""
        activities = audit_logger.get_recent_activities(50)
        return jsonify({
            'activities': activities,
            'total_count': len(activities)
        })


if __name__ == "__main__":
    # Test security functions
    validator = InputValidator()
    
    # Test input sanitization
    test_inputs = [
        "GET /index.html HTTP/1.1",
        "<script>alert('xss')</script>",
        "GET /../etc/passwd HTTP/1.1",
        "Normal text input"
    ]
    
    for test_input in test_inputs:
        try:
            result = validator.sanitize_text(test_input)
            print(f"✅ Sanitized: '{test_input}' → '{result}'")
        except ValueError as e:
            print(f"❌ Rejected: '{test_input}' → {e}")
    
    print("\n🔒 Security validation system ready!")