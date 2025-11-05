"""
HTTP Headers Validation using Context-Free Grammar Rules

This module implements HTTP header validation using CFG principles.
"""

import re
from typing import Dict, List, Any
from datetime import datetime
from enum import Enum

class HeaderFieldType(Enum):
    GENERAL = "general"
    REQUEST = "request" 
    RESPONSE = "response"
    ENTITY = "entity"

class HTTPHeaderCFGValidator:
    """CFG validator for HTTP headers according to RFC 7230."""
    
    def __init__(self):
        self.header_rules = self._init_rules()
        
    def _init_rules(self) -> Dict[str, Dict[str, Any]]:
        """Initialize header validation rules."""
        return {
            'Host': {
                'type': HeaderFieldType.REQUEST,
                'required': True,
                'pattern': r'^[a-zA-Z0-9\-\.]+(:\d+)?$'
            },
            'User-Agent': {
                'type': HeaderFieldType.REQUEST,
                'pattern': r'^[^\r\n]*$'
            },
            'Accept': {
                'type': HeaderFieldType.REQUEST,
                'pattern': r'^[a-zA-Z0-9\-\+]+/[a-zA-Z0-9\-\+\*]+(;[^,]*)?(\s*,\s*[a-zA-Z0-9\-\+]+/[a-zA-Z0-9\-\+\*]+(;[^,]*)?)*$'
            },
            'Content-Type': {
                'type': HeaderFieldType.ENTITY,
                'pattern': r'^[a-zA-Z0-9\-\+]+/[a-zA-Z0-9\-\+\*]+(;[^,]*)?$'
            },
            'Content-Length': {
                'type': HeaderFieldType.ENTITY,
                'pattern': r'^\d+$'
            },
            'Authorization': {
                'type': HeaderFieldType.REQUEST,
                'pattern': r'^[A-Za-z0-9\-\._~\+/]+=*(\s+[A-Za-z0-9\-\._~\+/!=]+)?$'
            },
            'Cache-Control': {
                'type': HeaderFieldType.GENERAL,
                'pattern': r'^(no-cache|no-store|max-age=\d+|must-revalidate|public|private)(\s*,\s*(no-cache|no-store|max-age=\d+|must-revalidate|public|private))*$'
            },
            'Connection': {
                'type': HeaderFieldType.GENERAL,
                'pattern': r'^(close|keep-alive|upgrade)(\s*,\s*(close|keep-alive|upgrade))*$'
            }
        }
    
    def validate_headers(self, headers_text: str) -> Dict[str, Any]:
        """Validate HTTP headers using CFG rules."""
        result = {
            'is_valid': True,
            'headers_text': headers_text,
            'parsed_headers': {},
            'validation_results': {},
            'errors': [],
            'warnings': [],
            'statistics': {},
            'timestamp': datetime.now().isoformat()
        }
        
        try:
            # Parse headers
            parsed_headers = self._parse_headers(headers_text)
            result['parsed_headers'] = parsed_headers
            
            # Validate each header
            for header_name, header_values in parsed_headers.items():
                validation_result = self._validate_header(header_name, header_values)
                result['validation_results'][header_name] = validation_result
                
                if not validation_result['is_valid']:
                    result['is_valid'] = False
                    result['errors'].extend(validation_result['errors'])
                
                result['warnings'].extend(validation_result.get('warnings', []))
            
            # Check required headers
            missing_required = self._check_required_headers(parsed_headers)
            if missing_required:
                result['is_valid'] = False
                result['errors'].extend(missing_required)
            
            # Calculate statistics
            result['statistics'] = {
                'total_headers': len(parsed_headers),
                'valid_headers': len([h for h in result['validation_results'].values() if h['is_valid']]),
                'invalid_headers': len([h for h in result['validation_results'].values() if not h['is_valid']]),
                'unknown_headers': len([h for h in result['validation_results'].values() if h.get('type') == 'unknown'])
            }
            
        except Exception as e:
            result['is_valid'] = False
            result['errors'].append(f"Header parsing error: {str(e)}")
        
        return result
    
    def _parse_headers(self, headers_text: str) -> Dict[str, List[str]]:
        """Parse headers text into structured format."""
        headers = {}
        lines = headers_text.strip().split('\n')
        
        for line in lines:
            line = line.strip()
            if not line or ':' not in line:
                continue
            
            header_name, header_value = line.split(':', 1)
            header_name = header_name.strip()
            header_value = header_value.strip()
            
            # Normalize header name
            header_name = '-'.join(word.capitalize() for word in header_name.split('-'))
            
            if header_name not in headers:
                headers[header_name] = []
            headers[header_name].append(header_value)
        
        return headers
    
    def _validate_header(self, header_name: str, header_values: List[str]) -> Dict[str, Any]:
        """Validate a single header field."""
        result = {
            'header_name': header_name,
            'header_values': header_values,
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'type': 'unknown'
        }
        
        if header_name in self.header_rules:
            rule = self.header_rules[header_name]
            result['type'] = rule['type'].value
            
            # Validate each value
            for i, value in enumerate(header_values):
                if 'pattern' in rule and not re.match(rule['pattern'], value):
                    result['is_valid'] = False
                    result['errors'].append(f"Value {i+1} '{value}' does not match expected pattern")
                
                if not self._is_valid_field_value(value):
                    result['is_valid'] = False
                    result['errors'].append(f"Value {i+1} contains invalid characters")
        else:
            result['warnings'].append(f"Unknown header '{header_name}' - treating as extension header")
            
            # Basic validation for unknown headers
            if not self._is_valid_token(header_name):
                result['is_valid'] = False
                result['errors'].append(f"Invalid header name '{header_name}'")
        
        return result
    
    def _is_valid_token(self, token: str) -> bool:
        """Check if string is a valid HTTP token."""
        return bool(re.match(r'^[!#$%&\'*+\-.0-9A-Z^_`a-z|~]+$', token))
    
    def _is_valid_field_value(self, value: str) -> bool:
        """Check if string is a valid field value."""
        for char in value:
            if ord(char) < 32 and char not in ['\t', ' ']:
                return False
        return True
    
    def _check_required_headers(self, headers: Dict[str, List[str]]) -> List[str]:
        """Check for required headers."""
        missing = []
        for header_name, rule in self.header_rules.items():
            if rule.get('required', False) and header_name not in headers:
                missing.append(f"Required header '{header_name}' is missing")
        return missing
    
    def get_grammar_info(self) -> Dict[str, Any]:
        """Get grammar information for headers."""
        return {
            'header_field_grammar': 'field-name ":" OWS field-value OWS',
            'field_name_grammar': 'token',
            'field_value_grammar': '*(field-content / obs-fold)',
            'token_grammar': '1*tchar',
            'supported_headers': list(self.header_rules.keys()),
            'header_types': [t.value for t in HeaderFieldType]
        }

# Example usage
if __name__ == "__main__":
    validator = HTTPHeaderCFGValidator()
    
    sample_headers = """Host: example.com
User-Agent: Mozilla/5.0
Accept: text/html,application/xhtml+xml
Content-Type: application/json
Content-Length: 123"""
    
    result = validator.validate_headers(sample_headers)
    print(f"Headers valid: {result['is_valid']}")
    print(f"Total headers: {result['statistics']['total_headers']}")
    if result['errors']:
        print(f"Errors: {result['errors']}")
    if result['warnings']:
        print(f"Warnings: {result['warnings']}")