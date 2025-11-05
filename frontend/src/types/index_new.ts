// Type definitions for the CFG Validator application

export interface ValidationResult {
  is_valid: boolean;
  request_line: string;
  tokens: string[];
  parse_trees: ParseTree[];
  errors: string[];
  timestamp: string;
}

export interface ParseTree {
  label: string;
  children: ParseTree[];
}

export interface GrammarRule {
  lhs: string;
  rhs: string;
  rule: string;
}

export interface GrammarInfo {
  rules: GrammarRule[];
  description: string;
  terminals: {
    HTTP_METHODS: string[];
    FILENAMES: string[];
    HTTP_VERSIONS: string[];
    SYMBOLS: string[];
  };
  production_rules: string[];
}

export interface ExampleRequest {
  request: string;
  description: string;
  expected: boolean;
}

export interface Analytics {
  total_requests: number;
  valid_requests: number;
  invalid_requests: number;
  success_rate: number;
  error_counts: Record<string, number>;
  daily_stats: Record<string, {
    valid: number;
    invalid: number;
    total: number;
  }>;
  period_days: number;
  unique_sessions?: number;
  avg_requests_per_session?: number;
  most_common_errors?: [string, number][];
}

export interface ErrorPattern {
  id: number;
  error_message: string;
  description: string;
  solution: string;
  example_correct: string;
  example_incorrect: string;
  occurrence_count: number;
  created_at: string;
  updated_at: string;
}

export interface RequestLog {
  id: number;
  request_line: string;
  is_valid: boolean;
  tokens: string[];
  parse_trees: ParseTree[];
  errors: string[];
  timestamp: string;
  ip_address: string;
  user_agent: string;
  session_id: string;
}

export interface UserSession {
  id: number;
  session_id: string;
  ip_address: string;
  user_agent: string;
  first_request: string;
  last_request: string;
  request_count: number;
  valid_request_count: number;
  invalid_request_count: number;
  success_rate: number;
}

export interface APIResponse<T> {
  data?: T;
  error?: string;
}

export interface StatsSummary {
  total_requests: number;
  valid_requests: number;
  invalid_requests: number;
  success_rate: number;
  total_sessions: number;
  recent_requests_24h: number;
}

export interface AIHelpResponse {
  question: string;
  answer: string;
  helpful_links: {
    title: string;
    url: string;
  }[];
}

// Chart data types
export interface ChartData {
  name: string;
  value: number;
  date?: string;
  valid?: number;
  invalid?: number;
  total?: number;
}

// Notification types
export interface Notification {
  id: string;
  type: 'success' | 'error' | 'warning' | 'info';
  title: string;
  message: string;
  duration?: number;
}

// Form types
export interface ValidationFormState {
  requestLine: string;
  isValidating: boolean;
  result: ValidationResult | null;
  history: ValidationResult[];
}