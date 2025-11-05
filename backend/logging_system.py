"""
Comprehensive Logging System for CFG QODER Project

This module provides structured logging with different levels, formatters,
and handlers for development, testing, and production environments.
"""

import logging
import logging.handlers
import os
import json
import sys
import traceback
from datetime import datetime
from typing import Dict, Any, Optional
from pathlib import Path
from functools import wraps
import uuid


class JSONFormatter(logging.Formatter):
    """JSON formatter for structured logging."""
    
    def format(self, record: logging.LogRecord) -> str:
        """Format log record as JSON."""
        log_entry = {
            'timestamp': datetime.utcfromtimestamp(record.created).isoformat() + 'Z',
            'level': record.levelname,
            'logger': record.name,
            'message': record.getMessage(),
            'module': record.module,
            'function': record.funcName,
            'line': record.lineno,
        }
        
        # Add extra fields if present
        if hasattr(record, 'user_id'):
            log_entry['user_id'] = getattr(record, 'user_id')
        if hasattr(record, 'session_id'):
            log_entry['session_id'] = getattr(record, 'session_id')
        if hasattr(record, 'request_id'):
            log_entry['request_id'] = getattr(record, 'request_id')
        if hasattr(record, 'component'):
            log_entry['component'] = getattr(record, 'component')
        if hasattr(record, 'performance_metrics'):
            log_entry['performance_metrics'] = getattr(record, 'performance_metrics')
        if hasattr(record, 'error_details'):
            log_entry['error_details'] = getattr(record, 'error_details')
            
        # Add exception info if present
        if record.exc_info and record.exc_info[0] is not None:
            log_entry['exception'] = {
                'type': record.exc_info[0].__name__,
                'message': str(record.exc_info[1]),
                'traceback': traceback.format_exception(*record.exc_info)
            }
            
        return json.dumps(log_entry, ensure_ascii=False)


class CFGQoderLogger:
    """Main logger class for CFG QODER project."""
    
    def __init__(self, name: str = 'cfg_qoder'):
        self.name = name
        self.logger = logging.getLogger(name)
        self.setup_logger()
        
    def setup_logger(self):
        """Setup logger with appropriate handlers and formatters."""
        # Prevent duplicate handlers
        if self.logger.handlers:
            return
            
        self.logger.setLevel(logging.DEBUG)
        
        # Create logs directory
        log_dir = Path('logs')
        log_dir.mkdir(exist_ok=True)
        
        # Console handler for development
        console_handler = logging.StreamHandler(sys.stdout)
        console_handler.setLevel(logging.INFO)
        console_formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)
        
        # File handler for general logs
        file_handler = logging.handlers.RotatingFileHandler(
            log_dir / 'cfg_qoder.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        file_handler.setLevel(logging.DEBUG)
        file_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(file_handler)
        
        # Error file handler
        error_handler = logging.handlers.RotatingFileHandler(
            log_dir / 'cfg_qoder_errors.log',
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        error_handler.setLevel(logging.ERROR)
        error_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(error_handler)
        
        # Performance metrics handler
        performance_handler = logging.handlers.RotatingFileHandler(
            log_dir / 'cfg_qoder_performance.log',
            maxBytes=5*1024*1024,  # 5MB
            backupCount=3
        )
        performance_handler.setLevel(logging.INFO)
        performance_handler.addFilter(PerformanceFilter())
        performance_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(performance_handler)
        
        # API access handler
        api_handler = logging.handlers.RotatingFileHandler(
            log_dir / 'cfg_qoder_api.log',
            maxBytes=10*1024*1024,  # 10MB
            backupCount=5
        )
        api_handler.setLevel(logging.INFO)
        api_handler.addFilter(APIFilter())
        api_handler.setFormatter(JSONFormatter())
        self.logger.addHandler(api_handler)
        
    def debug(self, message: str, **kwargs):
        """Log debug message."""
        self._log(logging.DEBUG, message, kwargs)
        
    def info(self, message: str, **kwargs):
        """Log info message."""
        self._log(logging.INFO, message, kwargs)
        
    def warning(self, message: str, **kwargs):
        """Log warning message."""
        self._log(logging.WARNING, message, kwargs)
        
    def error(self, message: str, **kwargs):
        """Log error message."""
        self._log(logging.ERROR, message, kwargs)
        
    def critical(self, message: str, **kwargs):
        """Log critical message."""
        self._log(logging.CRITICAL, message, kwargs)
        
    def _log(self, level: int, message: str, extra: Dict[str, Any]):
        """Internal logging method with extra fields."""
        self.logger.log(level, message, extra=extra)


class PerformanceFilter(logging.Filter):
    """Filter for performance-related log records."""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter performance logs."""
        return hasattr(record, 'performance_metrics')


class APIFilter(logging.Filter):
    """Filter for API-related log records."""
    
    def filter(self, record: logging.LogRecord) -> bool:
        """Filter API logs."""
        return (hasattr(record, 'request_id') or 
                'api' in record.getMessage().lower() or
                'endpoint' in record.getMessage().lower())


class ComponentLogger:
    """Logger for specific components."""
    
    def __init__(self, component_name: str):
        self.component_name = component_name
        self.base_logger = CFGQoderLogger(f'cfg_qoder.{component_name}')
        
    def log_operation(self, operation: str, status: str, **kwargs):
        """Log component operation."""
        message = f"Component {self.component_name}: {operation} - {status}"
        self.base_logger.info(message, 
                            component=self.component_name,
                            operation=operation,
                            status=status,
                            **kwargs)
                            
    def log_performance(self, operation: str, duration: float, **metrics):
        """Log performance metrics."""
        message = f"Performance: {operation} completed in {duration:.4f}s"
        performance_data = {
            'operation': operation,
            'duration_seconds': duration,
            **metrics
        }
        self.base_logger.info(message,
                            component=self.component_name,
                            performance_metrics=performance_data)
                            
    def log_error(self, operation: str, error: Exception, **kwargs):
        """Log component error."""
        message = f"Component {self.component_name}: {operation} failed"
        error_details = {
            'operation': operation,
            'error_type': type(error).__name__,
            'error_message': str(error),
            **kwargs
        }
        self.base_logger.error(message,
                             component=self.component_name,
                             error_details=error_details,
                             exc_info=True)


def performance_monitor(operation_name: Optional[str] = None):
    """Decorator to monitor function performance."""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = datetime.now()
            operation = operation_name or f"{func.__module__}.{func.__name__}"
            logger = ComponentLogger('performance')
            
            try:
                result = func(*args, **kwargs)
                duration = (datetime.now() - start_time).total_seconds()
                
                logger.log_performance(
                    operation=operation,
                    duration=duration,
                    success=True
                )
                
                return result
                
            except Exception as e:
                duration = (datetime.now() - start_time).total_seconds()
                logger.log_error(operation, e, duration=duration)
                raise
                
        return wrapper
    return decorator


def api_request_logger(func):
    """Decorator to log API requests."""
    @wraps(func)
    def wrapper(*args, **kwargs):
        from flask import request, g
        
        # Generate request ID
        request_id = str(uuid.uuid4())
        g.request_id = request_id
        
        logger = ComponentLogger('api')
        
        # Log request
        logger.log_operation(
            operation='api_request',
            status='started',
            request_id=request_id,
            endpoint=request.endpoint,
            method=request.method,
            remote_addr=request.remote_addr,
            user_agent=request.headers.get('User-Agent', 'Unknown')
        )
        
        start_time = datetime.now()
        
        try:
            result = func(*args, **kwargs)
            duration = (datetime.now() - start_time).total_seconds()
            
            # Log successful response
            logger.log_performance(
                operation='api_request',
                duration=duration,
                request_id=request_id,
                endpoint=request.endpoint,
                status_code=getattr(result, 'status_code', 200)
            )
            
            return result
            
        except Exception as e:
            duration = (datetime.now() - start_time).total_seconds()
            logger.log_error(
                operation='api_request',
                error=e,
                request_id=request_id,
                endpoint=request.endpoint,
                duration=duration
            )
            raise
            
    return wrapper


# Global logger instances
main_logger = CFGQoderLogger('cfg_qoder')
cfg_logger = ComponentLogger('cfg_parser')
nfa_logger = ComponentLogger('nfa_engine')
dfa_logger = ComponentLogger('dfa_engine')
nlp_logger = ComponentLogger('nlp')
api_logger = ComponentLogger('api')


def get_logger(component: str = 'main'):
    """Get logger for specific component."""
    if component == 'main':
        return ComponentLogger('main')
    else:
        return ComponentLogger(component)


# Example usage and configuration
def configure_logging(log_level: str = 'INFO', 
                     enable_console: bool = True,
                     enable_file: bool = True):
    """Configure logging system."""
    level = getattr(logging, log_level.upper(), logging.INFO)
    
    # Update all loggers
    for logger_name in ['cfg_qoder', 'cfg_qoder.cfg_parser', 'cfg_qoder.nfa_engine', 
                       'cfg_qoder.dfa_engine', 'cfg_qoder.nlp', 'cfg_qoder.api']:
        logger = logging.getLogger(logger_name)
        logger.setLevel(level)
        
        # Enable/disable handlers based on configuration
        for handler in logger.handlers:
            if isinstance(handler, logging.StreamHandler) and not enable_console:
                logger.removeHandler(handler)
            elif isinstance(handler, logging.FileHandler) and not enable_file:
                logger.removeHandler(handler)


if __name__ == "__main__":
    # Test the logging system
    test_logger = get_logger('test')
    
    test_logger.log_operation('test_operation', 'started')
    
    @performance_monitor('test_function')
    def test_function():
        import time
        time.sleep(0.1)
        return "test_result"
    
    result = test_function()
    test_logger.log_operation('test_operation', 'completed', result=result)
    
    # Test error logging
    try:
        raise ValueError("Test error for logging")
    except Exception as e:
        test_logger.log_error('test_error_operation', e)
    
    print("Logging system test completed. Check logs/ directory for output.")