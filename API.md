# CFG-Based HTTP GET Request Validator - API Documentation

## Overview

The CFG Validator API provides endpoints for validating HTTP GET requests using Context-Free Grammar rules, managing analytics, and accessing learning resources.

**Base URL**: `http://localhost:5000/api`

## Authentication

Currently, the API does not require authentication. Sessions are tracked automatically using cookies.

## Endpoints

### Health Check

#### `GET /health`
Check if the API is running.

**Response:**
```json
{
  "status": "healthy",
  "timestamp": "2024-01-20T15:30:00Z",
  "version": "1.0.0"
}
```

### Request Validation

#### `POST /validate`
Validate a single HTTP GET request line.

**Request Body:**
```json
{
  "request_line": "GET /index.html HTTP/1.1"
}
```

**Response:**
```json
{
  "is_valid": true,
  "request_line": "GET /index.html HTTP/1.1",
  "tokens": ["GET", " ", "/index.html", " ", "HTTP/1.1"],
  "parse_trees": [
    {
      "label": "RequestLine",
      "children": [
        {"label": "GET", "children": []},
        {"label": "SP", "children": []},
        {
          "label": "RequestTarget",
          "children": [
            {"label": "/", "children": []},
            {"label": "FileName", "children": [{"label": "index.html", "children": []}]}
          ]
        },
        {"label": "SP", "children": []},
        {"label": "HTTPVersion", "children": [{"label": "HTTP/1.1", "children": []}]}
      ]
    }
  ],
  "errors": [],
  "timestamp": "2024-01-20T15:30:00Z"
}
```

**Error Response:**
```json
{
  "is_valid": false,
  "request_line": "POST /index.html HTTP/1.1",
  "tokens": ["POST", " ", "/index.html", " ", "HTTP/1.1"],
  "parse_trees": [],
  "errors": ["Invalid HTTP method 'POST'. Only GET is supported."],
  "timestamp": "2024-01-20T15:30:00Z"
}
```

#### `POST /validate/batch`
Validate multiple HTTP request lines at once.

**Request Body:**
```json
{
  "requests": [
    "GET / HTTP/1.1",
    "GET /index.html HTTP/2.0",
    "POST /invalid HTTP/1.1"
  ]
}
```

**Response:**
```json
{
  "results": [
    {
      "is_valid": true,
      "request_line": "GET / HTTP/1.1",
      // ... validation result
    },
    {
      "is_valid": true,
      "request_line": "GET /index.html HTTP/2.0",
      // ... validation result
    },
    {
      "is_valid": false,
      "request_line": "POST /invalid HTTP/1.1",
      // ... validation result with errors
    }
  ],
  "total_processed": 3
}
```

### Grammar Information

#### `GET /grammar`
Get the Context-Free Grammar rules and structure.

**Response:**
```json
{
  "rules": [
    {
      "lhs": "RequestLine",
      "rhs": "GET SP RequestTarget SP HTTPVersion",
      "rule": "RequestLine → GET SP RequestTarget SP HTTPVersion"
    }
    // ... more rules
  ],
  "description": "Context-Free Grammar for HTTP GET Request Validation",
  "terminals": {
    "HTTP_METHODS": ["GET"],
    "FILENAMES": ["index.html", "about.html", "contact.html", "style.css"],
    "HTTP_VERSIONS": ["HTTP/1.0", "HTTP/1.1", "HTTP/2.0"],
    "SYMBOLS": ["/", " "]
  },
  "production_rules": [
    "RequestLine → GET SP RequestTarget SP HTTPVersion",
    "RequestTarget → \"/\" FileName | \"/\"",
    // ... more rules
  ]
}
```

### Example Requests

#### `GET /examples`
Get example HTTP requests for testing.

**Response:**
```json
{
  "examples": [
    {
      "request": "GET / HTTP/1.1",
      "description": "Basic root request",
      "expected": true
    },
    {
      "request": "POST /index.html HTTP/1.1",
      "description": "Invalid HTTP method (should fail)",
      "expected": false
    }
    // ... more examples
  ]
}
```

### Analytics

#### `GET /analytics`
Get validation analytics and statistics.

**Query Parameters:**
- `days` (optional): Number of days to analyze (default: 7, max: 365)

**Response:**
```json
{
  "total_requests": 1250,
  "valid_requests": 875,
  "invalid_requests": 375,
  "success_rate": 70.0,
  "error_counts": {
    "Invalid HTTP method": 45,
    "Invalid filename": 38,
    "Missing space": 32
  },
  "daily_stats": {
    "2024-01-20": {
      "valid": 120,
      "invalid": 45,
      "total": 165
    }
    // ... more daily data
  },
  "period_days": 7,
  "unique_sessions": 234,
  "avg_requests_per_session": 5.3,
  "most_common_errors": [
    ["Invalid HTTP method", 45],
    ["Invalid filename", 38]
  ]
}
```

#### `GET /analytics/detailed`
Get detailed analytics including recent request logs.

**Query Parameters:**
- `days` (optional): Number of days to analyze (default: 7)
- `limit` (optional): Maximum number of logs to return (default: 100)

**Response:**
```json
{
  "analytics": {
    // ... same as /analytics
  },
  "recent_logs": [
    {
      "id": 1,
      "request_line": "GET /index.html HTTP/1.1",
      "is_valid": true,
      "timestamp": "2024-01-20T15:30:00Z",
      // ... more log fields
    }
    // ... more logs
  ],
  "total_logs": 50
}
```

### Error Patterns

#### `GET /errors`
Get all error patterns and their explanations.

**Response:**
```json
{
  "error_patterns": [
    {
      "id": 1,
      "error_message": "Invalid HTTP method",
      "description": "The request line must start with the GET method...",
      "solution": "Ensure your request line starts with \"GET\"...",
      "example_correct": "GET /index.html HTTP/1.1",
      "example_incorrect": "POST /index.html HTTP/1.1",
      "occurrence_count": 145,
      "created_at": "2024-01-15T10:00:00Z",
      "updated_at": "2024-01-20T15:30:00Z"
    }
    // ... more error patterns
  ]
}
```

#### `GET /errors/{id}`
Get a specific error pattern by ID.

**Response:**
```json
{
  "id": 1,
  "error_message": "Invalid HTTP method",
  "description": "The request line must start with the GET method...",
  "solution": "Ensure your request line starts with \"GET\"...",
  "example_correct": "GET /index.html HTTP/1.1",
  "example_incorrect": "POST /index.html HTTP/1.1",
  "occurrence_count": 145,
  "created_at": "2024-01-15T10:00:00Z",
  "updated_at": "2024-01-20T15:30:00Z"
}
```

### Session Information

#### `GET /session`
Get current session information.

**Response:**
```json
{
  "id": 1,
  "session_id": "abc123...",
  "ip_address": "127.0.0.1",
  "user_agent": "Mozilla/5.0...",
  "first_request": "2024-01-20T15:00:00Z",
  "last_request": "2024-01-20T15:30:00Z",
  "request_count": 15,
  "valid_request_count": 12,
  "invalid_request_count": 3,
  "success_rate": 80.0
}
```

### Statistics Summary

#### `GET /stats/summary`
Get quick statistics summary.

**Response:**
```json
{
  "total_requests": 1250,
  "valid_requests": 875,
  "invalid_requests": 375,
  "success_rate": 70.0,
  "total_sessions": 234,
  "recent_requests_24h": 89
}
```

### AI Assistance

#### `POST /ai/help`
Get AI assistance for CFG rules and HTTP syntax.

**Request Body:**
```json
{
  "question": "What is CFG?"
}
```

**Response:**
```json
{
  "question": "What is CFG?",
  "answer": "CFG (Context-Free Grammar) is a formal grammar where each production rule has a single non-terminal on the left side...",
  "helpful_links": [
    {
      "title": "CFG Grammar Rules",
      "url": "/grammar"
    },
    {
      "title": "Request Examples",
      "url": "/examples"
    }
  ]
}
```

## Error Codes

- **200**: Success
- **400**: Bad Request (invalid input)
- **404**: Not Found (invalid endpoint or resource)
- **500**: Internal Server Error

## Rate Limiting

Currently, no rate limiting is implemented, but it's recommended for production use.

## CORS

CORS is enabled for all origins in development. Configure `CORS_ORIGINS` environment variable for production.

## Data Storage

- **Development**: SQLite database (`cfg_validator.db`)
- **Production**: PostgreSQL (configured via `DATABASE_URL`)

## Error Handling

All endpoints return consistent error responses:

```json
{
  "error": "Description of the error"
}
```