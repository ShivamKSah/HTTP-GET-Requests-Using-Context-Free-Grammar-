// Validation Context for tracking validation data in real-time

import React, { createContext, useContext, useState, useEffect } from 'react';
import type { ReactNode } from 'react';
import type { ValidationResult } from '../types';

interface RequestLog {
  id: number;
  request_line: string;
  is_valid: boolean;
  error_type?: string;
  error_message?: string;
  parse_tree?: string;
  validation_time_ms?: number;
  user_session: string;
  created_date: string;
}

interface ValidationStats {
  total: number;
  valid: number;
  invalid: number;
  successRate: number;
  avgResponseTime: number;
  commonError: string;
}

interface ValidationContextType {
  // State
  validationLogs: RequestLog[];
  stats: ValidationStats;
  
  // Functions
  addValidationLog: (inputText: string, result: ValidationResult, sessionId: string) => void;
  getFilteredLogs: (days: number) => RequestLog[];
  clearLogs: () => void;
  addSampleData: () => void;
}

const ValidationContext = createContext<ValidationContextType | undefined>(undefined);

export const useValidation = () => {
  const context = useContext(ValidationContext);
  if (context === undefined) {
    throw new Error('useValidation must be used within a ValidationProvider');
  }
  return context;
};

interface ValidationProviderProps {
  children: ReactNode;
}

export const ValidationProvider: React.FC<ValidationProviderProps> = ({ children }) => {
  const [validationLogs, setValidationLogs] = useState<RequestLog[]>([]);
  const [nextId, setNextId] = useState(1);

  // Load data from localStorage on mount
  useEffect(() => {
    const savedLogs = localStorage.getItem('validation_logs');
    const savedNextId = localStorage.getItem('validation_next_id');
    
    if (savedLogs) {
      try {
        const logs = JSON.parse(savedLogs);
        setValidationLogs(logs);
      } catch (error) {
        console.error('Failed to parse saved validation logs:', error);
      }
    }
    
    if (savedNextId) {
      setNextId(parseInt(savedNextId, 10));
    }
  }, []);

  // Save data to localStorage whenever logs change
  useEffect(() => {
    localStorage.setItem('validation_logs', JSON.stringify(validationLogs));
    localStorage.setItem('validation_next_id', nextId.toString());
  }, [validationLogs, nextId]);

  const addValidationLog = (inputText: string, result: ValidationResult, sessionId: string) => {
    const newLog: RequestLog = {
      id: nextId,
      request_line: inputText,
      is_valid: result.is_valid,
      error_type: result.errors.length > 0 ? 'validation_error' : undefined,
      error_message: result.errors.join(', '),
      parse_tree: JSON.stringify(result.parse_trees),
      validation_time_ms: Math.floor(Math.random() * 100) + 20, // Simulate response time
      user_session: sessionId,
      created_date: new Date().toISOString()
    };

    setValidationLogs(prev => [newLog, ...prev]);
    setNextId(prev => prev + 1);
  };

  const getFilteredLogs = (days: number): RequestLog[] => {
    const cutoffDate = new Date();
    cutoffDate.setDate(cutoffDate.getDate() - days);
    
    return validationLogs.filter(log => {
      const logDate = new Date(log.created_date);
      return logDate >= cutoffDate;
    });
  };

  const clearLogs = () => {
    setValidationLogs([]);
    setNextId(1);
    localStorage.removeItem('validation_logs');
    localStorage.removeItem('validation_next_id');
  };

  const addSampleData = () => {
    const sampleLogs: RequestLog[] = [
      {
        id: nextId,
        request_line: "GET /index.html HTTP/1.1",
        is_valid: true,
        validation_time_ms: 45,
        user_session: "sample_session_1",
        created_date: new Date().toISOString()
      },
      {
        id: nextId + 1,
        request_line: "GET /about.html HTTP/2.0",
        is_valid: true,
        validation_time_ms: 32,
        user_session: "sample_session_2",
        created_date: new Date(Date.now() - 3600000).toISOString() // 1 hour ago
      },
      {
        id: nextId + 2,
        request_line: "GET /style.css HTTP/1.0",
        is_valid: true,
        validation_time_ms: 41,
        user_session: "sample_session_3",
        created_date: new Date(Date.now() - 7200000).toISOString() // 2 hours ago
      },
      {
        id: nextId + 3,
        request_line: "GET /contact.html HTTP/1.1",
        is_valid: true,
        validation_time_ms: 38,
        user_session: "sample_session_4",
        created_date: new Date(Date.now() - 86400000).toISOString() // 1 day ago
      },
      {
        id: nextId + 4,
        request_line: "GET /assets/script.js HTTP/2.0",
        is_valid: true,
        validation_time_ms: 42,
        user_session: "sample_session_5",
        created_date: new Date(Date.now() - 172800000).toISOString() // 2 days ago
      },
      {
        id: nextId + 5,
        request_line: "GET /api/data.json HTTP/1.1",
        is_valid: true,
        validation_time_ms: 36,
        user_session: "sample_session_6",
        created_date: new Date(Date.now() - 259200000).toISOString() // 3 days ago
      },
      {
        id: nextId + 6,
        request_line: "GET /images/logo.png HTTP/1.0",
        is_valid: true,
        validation_time_ms: 44,
        user_session: "sample_session_7",
        created_date: new Date(Date.now() - 345600000).toISOString() // 4 days ago
      },
      {
        id: nextId + 7,
        request_line: "POST /submit HTTP/1.1",
        is_valid: false,
        error_type: "invalid_method",
        error_message: "Invalid HTTP method, only GET allowed",
        validation_time_ms: 39,
        user_session: "sample_session_8",
        created_date: new Date(Date.now() - 432000000).toISOString() // 5 days ago
      },
      {
        id: nextId + 8,
        request_line: "INVALID /test.html HTTP/1.1",
        is_valid: false,
        error_type: "invalid_method",
        error_message: "Invalid HTTP method",
        validation_time_ms: 28,
        user_session: "sample_session_9",
        created_date: new Date(Date.now() - 518400000).toISOString() // 6 days ago
      },
      {
        id: nextId + 9,
        request_line: "GET /missing HTTP/1.1",
        is_valid: false,
        error_type: "missing_extension",
        error_message: "Missing file extension",
        validation_time_ms: 33,
        user_session: "sample_session_10",
        created_date: new Date(Date.now() - 604800000).toISOString() // 7 days ago
      }
    ];

    setValidationLogs(prev => [...sampleLogs, ...prev]);
    setNextId(prev => prev + 10);
  };

  // Calculate real-time stats
  const calculateStats = (): ValidationStats => {
    const total = validationLogs.length;
    const valid = validationLogs.filter(log => log.is_valid).length;
    const invalid = total - valid;
    const successRate = total > 0 ? Math.round((valid / total) * 100) : 0;
    
    const avgResponseTime = total > 0 
      ? Math.round(validationLogs.reduce((sum, log) => sum + (log.validation_time_ms || 0), 0) / total)
      : 0;

    // Find most common error
    const errorCounts: Record<string, number> = {};
    validationLogs.filter(log => !log.is_valid && log.error_type).forEach(log => {
      const errorType = log.error_type!;
      errorCounts[errorType] = (errorCounts[errorType] || 0) + 1;
    });

    const commonError = Object.keys(errorCounts).length > 0
      ? Object.entries(errorCounts).reduce((a, b) => errorCounts[a[0]] > errorCounts[b[0]] ? a : b)[0]
      : 'None';

    return {
      total,
      valid,
      invalid,
      successRate,
      avgResponseTime,
      commonError: commonError.replace('_', ' ')
    };
  };

  const stats = calculateStats();

  const value: ValidationContextType = {
    validationLogs,
    stats,
    addValidationLog,
    getFilteredLogs,
    clearLogs,
    addSampleData
  };

  return (
    <ValidationContext.Provider value={value}>
      {children}
    </ValidationContext.Provider>
  );
};