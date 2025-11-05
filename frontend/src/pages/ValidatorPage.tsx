import React, { useState } from 'react';
import { motion } from "framer-motion";
import { ValidationForm } from '../components/ValidationForm';
import { useValidation } from '../contexts/ValidationContext';
import { Zap, Code, CheckCircle } from 'lucide-react';
import type { ValidationResult } from '../types';

export const ValidatorPage: React.FC = () => {
  const [sessionId] = useState(() => `session_${Date.now()}_${Math.random().toString(36).substr(2, 9)}`);
  const { addValidationLog } = useValidation();

  const handleValidationResult = async (inputText: string, result: ValidationResult) => {
    try {
      // Add to validation context for real-time tracking
      addValidationLog(inputText, result, sessionId);
      
      // Debug logging
      console.log('✅ Validation logged successfully:', {
        request_line: inputText,
        is_valid: result.is_valid,
        errors: result.errors,
        timestamp: new Date().toISOString(),
        user_session: sessionId
      });
    } catch (error) {
      console.error('❌ Failed to log validation result:', error);
    }
  };

  return (
    <div className="min-h-screen px-6 py-8 lg:px-8 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 gradient-overlay opacity-30"></div>
      <div className="absolute top-20 left-10 w-64 h-64 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-pulse-slow"></div>
      <div className="absolute bottom-20 right-10 w-80 h-80 bg-gradient-to-r from-purple-400 to-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-pulse-slow" style={{animationDelay: '2s'}}></div>
      
      <div className="relative mx-auto max-w-4xl space-y-8">
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="text-center space-y-4"
        >
          <motion.div
            initial={{ scale: 0 }}
            animate={{ scale: 1 }}
            transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
            className="inline-flex items-center gap-2 px-4 py-2 bg-green-100 rounded-full text-green-800 text-sm font-medium mb-4 border border-green-200"
          >
            <span className="w-2 h-2 bg-green-500 rounded-full animate-pulse"></span>
            Ready to validate
          </motion.div>
          
          <motion.h1 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3, duration: 0.8 }}
            className="text-4xl lg:text-5xl font-bold text-gray-900"
          >
            HTTP Request Validator
          </motion.h1>
          
          <motion.p 
            initial={{ opacity: 0, y: 20 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5, duration: 0.8 }}
            className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed"
          >
            Test your HTTP GET requests against proper grammar rules. 
            Get instant feedback and learn from detailed explanations.
          </motion.p>
        </motion.div>

        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.7, duration: 0.8 }}
        >
          <ValidationForm onValidationResult={handleValidationResult} />
        </motion.div>
      </div>
    </div>
  );
};