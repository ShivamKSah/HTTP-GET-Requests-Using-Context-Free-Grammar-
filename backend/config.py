"""
Comprehensive Configuration Management for CFG QODER Project

This module provides centralized configuration management with support for
environment variables, configuration files, and different deployment environments.
"""

import os
import json
import yaml
from pathlib import Path
from typing import Dict, Any, Optional, Union
from dataclasses import dataclass, field
from enum import Enum


class Environment(Enum):
    """Deployment environments."""
    DEVELOPMENT = "development"
    TESTING = "testing"
    STAGING = "staging"
    PRODUCTION = "production"


@dataclass
class DatabaseConfig:
    """Database configuration."""
    url: str = "sqlite:///cfg_validator.db"
    echo: bool = False
    pool_size: int = 5
    max_overflow: int = 10
    pool_timeout: int = 30
    pool_recycle: int = 3600


@dataclass
class APIConfig:
    """API configuration."""
    host: str = "localhost"
    port: int = 5000
    debug: bool = False
    testing: bool = False
    secret_key: str = "dev-secret-key"
    max_content_length: int = 16 * 1024 * 1024  # 16MB
    cors_origins: list = field(default_factory=lambda: ["http://localhost:3000"])
    rate_limit_enabled: bool = True
    rate_limit_default: str = "100/hour"


@dataclass
class LoggingConfig:
    """Logging configuration."""
    level: str = "INFO"
    enable_console: bool = True
    enable_file: bool = True
    enable_json: bool = True
    log_dir: str = "logs"
    max_file_size: int = 10 * 1024 * 1024  # 10MB
    backup_count: int = 5
    enable_performance_logging: bool = True
    enable_api_logging: bool = True


@dataclass
class NLPConfig:
    """NLP module configuration."""
    enable_summarization: bool = True
    enable_classification: bool = True
    enable_query_processing: bool = True
    max_text_length: int = 50000
    cache_enabled: bool = True
    cache_ttl: int = 3600  # 1 hour
    batch_size_limit: int = 10


@dataclass
class AutomataConfig:
    """Automata engines configuration."""
    enable_nfa: bool = True
    enable_dfa: bool = True
    enable_regex_matching: bool = True
    max_pattern_length: int = 1000
    timeout_seconds: int = 30
    cache_enabled: bool = True
    performance_monitoring: bool = True


@dataclass
class SecurityConfig:
    """Security configuration."""
    enable_input_validation: bool = True
    enable_sanitization: bool = True
    enable_rate_limiting: bool = True
    max_request_size: int = 16 * 1024 * 1024  # 16MB
    allowed_origins: list = field(default_factory=lambda: ["http://localhost:3000"])
    enable_cors: bool = True
    enable_csrf_protection: bool = True


@dataclass
class PerformanceConfig:
    """Performance monitoring configuration."""
    enable_metrics: bool = True
    enable_profiling: bool = False
    slow_query_threshold: float = 1.0  # seconds
    enable_caching: bool = True
    cache_timeout: int = 300  # 5 minutes
    max_cache_size: int = 1000


@dataclass
class CFGQoderConfig:
    """Main configuration class."""
    environment: Environment = Environment.DEVELOPMENT
    database: DatabaseConfig = field(default_factory=DatabaseConfig)
    api: APIConfig = field(default_factory=APIConfig)
    logging: LoggingConfig = field(default_factory=LoggingConfig)
    nlp: NLPConfig = field(default_factory=NLPConfig)
    automata: AutomataConfig = field(default_factory=AutomataConfig)
    security: SecurityConfig = field(default_factory=SecurityConfig)
    performance: PerformanceConfig = field(default_factory=PerformanceConfig)


class ConfigurationManager:
    """Configuration manager with multiple sources support."""
    
    def __init__(self, config_file: Optional[str] = None):
        self.config_file = config_file
        self.config = CFGQoderConfig()
        self.load_configuration()
    
    def load_configuration(self):
        """Load configuration from multiple sources in priority order."""
        # 1. Load default configuration (already done in dataclass)
        
        # 2. Load from configuration file
        if self.config_file:
            self.load_from_file(self.config_file)
        else:
            # Try to find configuration file
            for config_path in self._get_config_file_paths():
                if config_path.exists():
                    self.load_from_file(str(config_path))
                    break
        
        # 3. Override with environment variables
        self.load_from_environment()
        
        # 4. Apply environment-specific configurations
        self.apply_environment_config()
    
    def _get_config_file_paths(self) -> list[Path]:
        """Get possible configuration file paths."""
        return [
            Path("config.yaml"),
            Path("config.yml"),
            Path("config.json"),
            Path("cfg_qoder.yaml"),
            Path("cfg_qoder.yml"),
            Path("cfg_qoder.json"),
            Path.home() / ".cfg_qoder" / "config.yaml",
            Path("/etc/cfg_qoder/config.yaml"),
        ]
    
    def load_from_file(self, file_path: str):
        """Load configuration from file."""
        path = Path(file_path)
        if not path.exists():
            raise FileNotFoundError(f"Configuration file not found: {file_path}")
        
        try:
            with open(path, 'r', encoding='utf-8') as f:
                if path.suffix.lower() in ['.yaml', '.yml']:
                    data = yaml.safe_load(f)
                elif path.suffix.lower() == '.json':
                    data = json.load(f)
                else:
                    raise ValueError(f"Unsupported configuration file format: {path.suffix}")
            
            self._update_config_from_dict(data)
            
        except Exception as e:
            raise RuntimeError(f"Error loading configuration from {file_path}: {e}")
    
    def load_from_environment(self):
        """Load configuration from environment variables."""
        env_mappings = {
            # General
            'CFG_QODER_ENV': ('environment', self._parse_environment),
            
            # Database
            'DATABASE_URL': ('database.url', str),
            'DATABASE_ECHO': ('database.echo', self._parse_bool),
            'DATABASE_POOL_SIZE': ('database.pool_size', int),
            
            # API
            'API_HOST': ('api.host', str),
            'API_PORT': ('api.port', int),
            'API_DEBUG': ('api.debug', self._parse_bool),
            'SECRET_KEY': ('api.secret_key', str),
            'CORS_ORIGINS': ('api.cors_origins', self._parse_list),
            
            # Logging
            'LOG_LEVEL': ('logging.level', str),
            'ENABLE_CONSOLE_LOGGING': ('logging.enable_console', self._parse_bool),
            'ENABLE_FILE_LOGGING': ('logging.enable_file', self._parse_bool),
            'LOG_DIR': ('logging.log_dir', str),
            
            # NLP
            'ENABLE_NLP_SUMMARIZATION': ('nlp.enable_summarization', self._parse_bool),
            'ENABLE_NLP_CLASSIFICATION': ('nlp.enable_classification', self._parse_bool),
            'MAX_TEXT_LENGTH': ('nlp.max_text_length', int),
            
            # Security
            'ENABLE_RATE_LIMITING': ('security.enable_rate_limiting', self._parse_bool),
            'MAX_REQUEST_SIZE': ('security.max_request_size', int),
            
            # Performance
            'ENABLE_METRICS': ('performance.enable_metrics', self._parse_bool),
            'ENABLE_CACHING': ('performance.enable_caching', self._parse_bool),
        }
        
        for env_var, (config_path, parser) in env_mappings.items():
            value = os.getenv(env_var)
            if value is not None:
                try:
                    parsed_value = parser(value)
                    self._set_nested_config(config_path, parsed_value)
                except (ValueError, TypeError) as e:
                    print(f"Warning: Invalid value for {env_var}: {value} ({e})")
    
    def apply_environment_config(self):
        """Apply environment-specific configuration overrides."""
        env = self.config.environment
        
        if env == Environment.DEVELOPMENT:
            self.config.api.debug = True
            self.config.logging.level = "DEBUG"
            self.config.logging.enable_console = True
            self.config.database.echo = True
            
        elif env == Environment.TESTING:
            self.config.api.testing = True
            self.config.database.url = "sqlite:///:memory:"
            self.config.logging.level = "WARNING"
            self.config.logging.enable_file = False
            
        elif env == Environment.STAGING:
            self.config.api.debug = False
            self.config.logging.level = "INFO"
            self.config.performance.enable_profiling = True
            
        elif env == Environment.PRODUCTION:
            self.config.api.debug = False
            self.config.logging.level = "WARNING"
            self.config.logging.enable_console = False
            self.config.security.enable_csrf_protection = True
            self.config.performance.enable_metrics = True
    
    def _update_config_from_dict(self, data: Dict[str, Any]):
        """Update configuration from dictionary."""
        for key, value in data.items():
            if hasattr(self.config, key):
                if isinstance(value, dict):
                    # Handle nested configuration
                    config_section = getattr(self.config, key)
                    for nested_key, nested_value in value.items():
                        if hasattr(config_section, nested_key):
                            setattr(config_section, nested_key, nested_value)
                else:
                    setattr(self.config, key, value)
    
    def _set_nested_config(self, path: str, value: Any):
        """Set nested configuration value using dot notation."""
        parts = path.split('.')
        obj = self.config
        
        for part in parts[:-1]:
            obj = getattr(obj, part)
        
        setattr(obj, parts[-1], value)
    
    def _parse_bool(self, value: str) -> bool:
        """Parse boolean from string."""
        return value.lower() in ('true', '1', 'yes', 'on', 'enabled')
    
    def _parse_list(self, value: str) -> list:
        """Parse list from comma-separated string."""
        return [item.strip() for item in value.split(',') if item.strip()]
    
    def _parse_environment(self, value: str) -> Environment:
        """Parse environment from string."""
        try:
            return Environment(value.lower())
        except ValueError:
            return Environment.DEVELOPMENT
    
    def get(self, path: str, default: Any = None) -> Any:
        """Get configuration value using dot notation."""
        try:
            parts = path.split('.')
            obj = self.config
            
            for part in parts:
                obj = getattr(obj, part)
            
            return obj
        except AttributeError:
            return default
    
    def set(self, path: str, value: Any):
        """Set configuration value using dot notation."""
        self._set_nested_config(path, value)
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert configuration to dictionary."""
        def dataclass_to_dict(obj):
            if hasattr(obj, '__dataclass_fields__'):
                return {
                    field: dataclass_to_dict(getattr(obj, field))
                    for field in obj.__dataclass_fields__
                }
            elif isinstance(obj, Enum):
                return obj.value
            elif isinstance(obj, list):
                return [dataclass_to_dict(item) for item in obj]
            else:
                return obj
        
        return dataclass_to_dict(self.config)
    
    def save_to_file(self, file_path: str, format: str = 'yaml'):
        """Save configuration to file."""
        data = self.to_dict()
        path = Path(file_path)
        
        # Create directory if it doesn't exist
        path.parent.mkdir(parents=True, exist_ok=True)
        
        with open(path, 'w', encoding='utf-8') as f:
            if format.lower() in ['yaml', 'yml']:
                yaml.dump(data, f, default_flow_style=False, sort_keys=False)
            elif format.lower() == 'json':
                json.dump(data, f, indent=2, ensure_ascii=False)
            else:
                raise ValueError(f"Unsupported format: {format}")
    
    def validate(self) -> list[str]:
        """Validate configuration and return list of issues."""
        issues = []
        
        # Validate database URL
        if not self.config.database.url:
            issues.append("Database URL is required")
        
        # Validate API configuration
        if not (1 <= self.config.api.port <= 65535):
            issues.append("API port must be between 1 and 65535")
        
        if not self.config.api.secret_key or self.config.api.secret_key == "dev-secret-key":
            if self.config.environment == Environment.PRODUCTION:
                issues.append("Secret key must be set for production")
        
        # Validate logging configuration
        valid_log_levels = ['DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL']
        if self.config.logging.level.upper() not in valid_log_levels:
            issues.append(f"Invalid log level: {self.config.logging.level}")
        
        # Validate NLP configuration
        if self.config.nlp.max_text_length <= 0:
            issues.append("Maximum text length must be positive")
        
        # Validate performance configuration
        if self.config.performance.slow_query_threshold <= 0:
            issues.append("Slow query threshold must be positive")
        
        return issues


# Global configuration instance
_config_manager: Optional[ConfigurationManager] = None


def get_config(config_file: Optional[str] = None) -> CFGQoderConfig:
    """Get global configuration instance."""
    global _config_manager
    
    if _config_manager is None:
        _config_manager = ConfigurationManager(config_file)
    
    return _config_manager.config


def reload_config(config_file: Optional[str] = None):
    """Reload configuration."""
    global _config_manager
    _config_manager = ConfigurationManager(config_file)


def get_config_manager() -> ConfigurationManager:
    """Get configuration manager instance."""
    global _config_manager
    
    if _config_manager is None:
        _config_manager = ConfigurationManager()
    
    return _config_manager


# Example usage
if __name__ == "__main__":
    # Create example configuration file
    config_manager = ConfigurationManager()
    
    # Validate configuration
    issues = config_manager.validate()
    if issues:
        print("Configuration issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("Configuration is valid!")
    
    # Save example configuration
    config_manager.save_to_file("example_config.yaml")
    print("Example configuration saved to example_config.yaml")
    
    # Print current configuration
    print(f"Current environment: {config_manager.config.environment.value}")
    print(f"API host: {config_manager.config.api.host}")
    print(f"API port: {config_manager.config.api.port}")
    print(f"Database URL: {config_manager.config.database.url}")
    print(f"Log level: {config_manager.config.logging.level}")