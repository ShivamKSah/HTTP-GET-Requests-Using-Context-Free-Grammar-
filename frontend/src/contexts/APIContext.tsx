// API Context for managing API state and functions

import React, { createContext, useContext, useState, useCallback, ReactNode } from 'react';
import { apiClient } from '../utils/api';
import type {
  ValidationResult,
  GrammarInfo,
  ExampleRequest,
  Analytics,
  ErrorPattern,
  UserSession,
  StatsSummary,
  AIHelpResponse
} from '../types';

interface APIContextType {
  // State
  loading: boolean;
  error: string | null;
  grammar: GrammarInfo | null;
  examples: ExampleRequest[];
  session: UserSession | null;
  
  // Functions
  validateRequest: (requestLine: string) => Promise<ValidationResult | null>;
  validateBatch: (requests: string[]) => Promise<{ results: ValidationResult[]; total_processed: number } | null>;
  loadGrammar: () => Promise<void>;
  loadExamples: () => Promise<void>;
  getAnalytics: (days?: number) => Promise<Analytics | null>;
  getDetailedAnalytics: (days?: number, limit?: number) => Promise<{ analytics: Analytics; recent_logs: any[]; total_logs: number } | null>;
  getErrorPatterns: () => Promise<ErrorPattern[] | null>;
  getErrorPattern: (id: number) => Promise<ErrorPattern | null>;
  getSessionInfo: () => Promise<void>;
  getStatsSummary: () => Promise<StatsSummary | null>;
  getAIHelp: (question: string) => Promise<AIHelpResponse | null>;
  clearError: () => void;
}

const APIContext = createContext<APIContextType | undefined>(undefined);

export const useAPI = () => {
  const context = useContext(APIContext);
  if (context === undefined) {
    throw new Error('useAPI must be used within an APIProvider');
  }
  return context;
};

interface APIProviderProps {
  children: ReactNode;
}

export const APIProvider: React.FC<APIProviderProps> = ({ children }) => {
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [grammar, setGrammar] = useState<GrammarInfo | null>(null);
  const [examples, setExamples] = useState<ExampleRequest[]>([]);
  const [session, setSession] = useState<UserSession | null>(null);

  const handleError = (error: string) => {
    setError(error);
    console.error('API Error:', error);
  };

  const clearError = useCallback(() => {
    setError(null);
  }, []);

  const validateRequest = useCallback(async (requestLine: string): Promise<ValidationResult | null> => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.validateRequest(requestLine);
      if (response.error) {
        handleError(response.error);
        return null;
      }
      return response.data || null;
    } catch (err) {
      handleError('Failed to validate request');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const validateBatch = useCallback(async (requests: string[]) => {
    setLoading(true);
    setError(null);
    
    try {
      const response = await apiClient.validateBatch(requests);
      if (response.error) {
        handleError(response.error);
        return null;
      }
      return response.data || null;
    } catch (err) {
      handleError('Failed to validate batch requests');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const loadGrammar = useCallback(async () => {
    if (grammar) return; // Already loaded
    
    setLoading(true);
    try {
      const response = await apiClient.getGrammar();
      if (response.error) {
        handleError(response.error);
      } else if (response.data) {
        setGrammar(response.data);
      }
    } catch (err) {
      handleError('Failed to load grammar');
    } finally {
      setLoading(false);
    }
  }, [grammar]);

  const loadExamples = useCallback(async () => {
    if (examples.length > 0) return; // Already loaded
    
    setLoading(true);
    try {
      const response = await apiClient.getExamples();
      if (response.error) {
        handleError(response.error);
      } else if (response.data) {
        setExamples(response.data.examples);
      }
    } catch (err) {
      handleError('Failed to load examples');
    } finally {
      setLoading(false);
    }
  }, [examples.length]);

  const getAnalytics = useCallback(async (days: number = 7): Promise<Analytics | null> => {
    setLoading(true);
    try {
      const response = await apiClient.getAnalytics(days);
      if (response.error) {
        handleError(response.error);
        return null;
      }
      return response.data || null;
    } catch (err) {
      handleError('Failed to load analytics');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const getDetailedAnalytics = useCallback(async (days: number = 7, limit: number = 100) => {
    setLoading(true);
    try {
      const response = await apiClient.getDetailedAnalytics(days, limit);
      if (response.error) {
        handleError(response.error);
        return null;
      }
      return response.data || null;
    } catch (err) {
      handleError('Failed to load detailed analytics');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const getErrorPatterns = useCallback(async (): Promise<ErrorPattern[] | null> => {
    setLoading(true);
    try {
      const response = await apiClient.getErrorPatterns();
      if (response.error) {
        handleError(response.error);
        return null;
      }
      return response.data?.error_patterns || null;
    } catch (err) {
      handleError('Failed to load error patterns');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const getErrorPattern = useCallback(async (id: number): Promise<ErrorPattern | null> => {
    setLoading(true);
    try {
      const response = await apiClient.getErrorPattern(id);
      if (response.error) {
        handleError(response.error);
        return null;
      }
      return response.data || null;
    } catch (err) {
      handleError('Failed to load error pattern');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const getSessionInfo = useCallback(async () => {
    try {
      const response = await apiClient.getSessionInfo();
      if (response.error) {
        console.warn('Failed to load session info:', response.error);
      } else if (response.data) {
        setSession(response.data);
      }
    } catch (err) {
      console.warn('Failed to load session info:', err);
    }
  }, []);

  const getStatsSummary = useCallback(async (): Promise<StatsSummary | null> => {
    try {
      const response = await apiClient.getStatsSummary();
      if (response.error) {
        handleError(response.error);
        return null;
      }
      return response.data || null;
    } catch (err) {
      handleError('Failed to load stats summary');
      return null;
    }
  }, []);

  const getAIHelp = useCallback(async (question: string): Promise<AIHelpResponse | null> => {
    setLoading(true);
    try {
      const response = await apiClient.getAIHelp(question);
      if (response.error) {
        handleError(response.error);
        return null;
      }
      return response.data || null;
    } catch (err) {
      handleError('Failed to get AI help');
      return null;
    } finally {
      setLoading(false);
    }
  }, []);

  const value: APIContextType = {
    loading,
    error,
    grammar,
    examples,
    session,
    validateRequest,
    validateBatch,
    loadGrammar,
    loadExamples,
    getAnalytics,
    getDetailedAnalytics,
    getErrorPatterns,
    getErrorPattern,
    getSessionInfo,
    getStatsSummary,
    getAIHelp,
    clearError,
  };

  return (
    <APIContext.Provider value={value}>
      {children}
    </APIContext.Provider>
  );
};