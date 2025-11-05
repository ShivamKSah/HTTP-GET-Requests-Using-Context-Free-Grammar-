// API utility functions for the CFG Validator application

import axios from 'axios';
import type {
  ValidationResult,
  GrammarInfo,
  ExampleRequest,
  Analytics,
  ErrorPattern,
  RequestLog,
  UserSession,
  StatsSummary,
  AIHelpResponse,
  APIResponse
} from '../types';

// Create axios instance with base configuration
const api = axios.create({
  baseURL: import.meta.env.VITE_API_URL || 'http://localhost:5000/api',
  timeout: 10000,
  withCredentials: true,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Request interceptor
api.interceptors.request.use(
  (config) => {
    // Add any auth headers or request modifications here
    return config;
  },
  (error) => {
    return Promise.reject(error);
  }
);

// Response interceptor
api.interceptors.response.use(
  (response) => {
    return response;
  },
  (error) => {
    // Handle common errors
    if (error.response?.status === 401) {
      // Handle unauthorized
    } else if (error.response?.status >= 500) {
      // Handle server errors
    }
    return Promise.reject(error);
  }
);

// API functions
export const apiClient = {
  // Health check
  async healthCheck(): Promise<APIResponse<{ status: string; timestamp: string; version: string }>> {
    try {
      const response = await api.get('/health');
      return { data: response.data };
    } catch (error) {
      return { error: this.getErrorMessage(error) };
    }
  },

  // Validation endpoints
  async validateRequest(requestLine: string): Promise<APIResponse<ValidationResult>> {
    try {
      const response = await api.post('/validate', { request_line: requestLine });
      return { data: response.data };
    } catch (error) {
      return { error: this.getErrorMessage(error) };
    }
  },

  async validateBatch(requests: string[]): Promise<APIResponse<{ results: ValidationResult[]; total_processed: number }>> {
    try {
      const response = await api.post('/validate/batch', { requests });
      return { data: response.data };
    } catch (error) {
      return { error: this.getErrorMessage(error) };
    }
  },

  // Grammar endpoints
  async getGrammar(): Promise<APIResponse<GrammarInfo>> {
    try {
      const response = await api.get('/grammar');
      return { data: response.data };
    } catch (error) {
      return { error: this.getErrorMessage(error) };
    }
  },

  // Examples endpoints
  async getExamples(): Promise<APIResponse<{ examples: ExampleRequest[] }>> {
    try {
      const response = await api.get('/examples');
      return { data: response.data };
    } catch (error) {
      return { error: this.getErrorMessage(error) };
    }
  },

  // Analytics endpoints
  async getAnalytics(days: number = 7): Promise<APIResponse<Analytics>> {
    try {
      const response = await api.get(`/analytics?days=${days}`);
      return { data: response.data };
    } catch (error) {
      return { error: this.getErrorMessage(error) };
    }
  },

  async getDetailedAnalytics(days: number = 7, limit: number = 100): Promise<APIResponse<{ analytics: Analytics; recent_logs: RequestLog[]; total_logs: number }>> {
    try {
      const response = await api.get(`/analytics/detailed?days=${days}&limit=${limit}`);
      return { data: response.data };
    } catch (error) {
      return { error: this.getErrorMessage(error) };
    }
  },

  // Error patterns endpoints
  async getErrorPatterns(): Promise<APIResponse<{ error_patterns: ErrorPattern[] }>> {
    try {
      const response = await api.get('/errors');
      return { data: response.data };
    } catch (error) {
      return { error: this.getErrorMessage(error) };
    }
  },

  async getErrorPattern(id: number): Promise<APIResponse<ErrorPattern>> {
    try {
      const response = await api.get(`/errors/${id}`);
      return { data: response.data };
    } catch (error) {
      return { error: this.getErrorMessage(error) };
    }
  },

  // Session endpoints
  async getSessionInfo(): Promise<APIResponse<UserSession>> {
    try {
      const response = await api.get('/session');
      return { data: response.data };
    } catch (error) {
      return { error: this.getErrorMessage(error) };
    }
  },

  // Stats endpoints
  async getStatsSummary(): Promise<APIResponse<StatsSummary>> {
    try {
      const response = await api.get('/stats/summary');
      return { data: response.data };
    } catch (error) {
      return { error: this.getErrorMessage(error) };
    }
  },

  // AI help endpoint
  async getAIHelp(question: string): Promise<APIResponse<AIHelpResponse>> {
    try {
      const response = await api.post('/ai/help', { question });
      return { data: response.data };
    } catch (error) {
      return { error: this.getErrorMessage(error) };
    }
  },

  // Utility method to extract error messages
  getErrorMessage(error: any): string {
    if (error.response?.data?.error) {
      return error.response.data.error;
    }
    if (error.message) {
      return error.message;
    }
    return 'An unexpected error occurred';
  },
};

// Export individual functions for convenience
export const {
  healthCheck,
  validateRequest,
  validateBatch,
  getGrammar,
  getExamples,
  getAnalytics,
  getDetailedAnalytics,
  getErrorPatterns,
  getErrorPattern,
  getSessionInfo,
  getStatsSummary,
  getAIHelp,
} = apiClient;

export default apiClient;