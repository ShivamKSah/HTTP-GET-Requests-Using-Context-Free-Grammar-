import React, { useState } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import { AlertCircle, CheckCircle, Play, RotateCcw, Clock, Zap, Sparkles } from 'lucide-react';
import { useAPI } from '../contexts/APIContext';
import { useNotifications } from '../contexts/NotificationContext';
import type { ValidationResult } from '../types';

interface ValidationFormProps {
  onValidationResult?: (inputText: string, result: ValidationResult) => void;
}

export const ValidationForm: React.FC<ValidationFormProps> = ({ onValidationResult }) => {
  const [input, setInput] = useState('');
  const [isValidating, setIsValidating] = useState(false);
  const [result, setResult] = useState<ValidationResult | null>(null);
  
  const { validateRequest } = useAPI();
  const { showSuccess, showError } = useNotifications();

  const handleValidate = async () => {
    if (!input.trim()) return;
    
    setIsValidating(true);
    
    // Simulate processing time for better UX
    await new Promise(resolve => setTimeout(resolve, 300));
    
    try {
      const validationResult = await validateRequest(input.trim());
      
      if (validationResult) {
        setResult(validationResult);
        
        // Callback to parent component for analytics
        if (onValidationResult) {
          onValidationResult(input, validationResult);
        }
        
        // Show notification
        if (validationResult.is_valid) {
          showSuccess('Validation Successful', 'HTTP request is valid according to CFG rules');
        } else {
          showError('Validation Failed', `Found ${validationResult.errors.length} error(s)`);
        }
      }
    } catch (error) {
      showError('Validation Error', 'Failed to validate request');
    } finally {
      setIsValidating(false);
    }
  };

  const handleClear = () => {
    setInput('');
    setResult(null);
  };

  const loadExample = (example: string) => {
    setInput(example);
    setResult(null);
  };

  const examples = [
    'GET / HTTP/1.1',
    'GET /index.html HTTP/1.0',
    'GET /about.html HTTP/2.0',
    'GET /style.css HTTP/1.1'
  ];

  const getErrorSuggestions = (errorType: string, inputText: string): string[] => {
    const suggestions = [
      'Ensure your request starts with "GET"',
      'Include a valid path (e.g., "/index.html")',
      'End with a valid HTTP version (e.g., "HTTP/1.1")',
      'Use proper spacing between components'
    ];
    return suggestions;
  };

  return (
    <div className="space-y-6">
      {/* Enhanced Input Section */}
      <motion.div 
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="glass-card border border-blue-100 shadow-xl rounded-xl overflow-hidden"
      >
        <div className="pb-4 px-6 pt-6">
          <motion.div 
            initial={{ opacity: 0, x: -20 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
            className="flex items-center gap-3 text-xl font-bold mb-2"
          >
            <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
              <Zap className="w-4 h-4 text-white" />
            </div>
            <span className="text-gray-900">HTTP Request Validator</span>
          </motion.div>
          <p className="text-gray-600">Enter your HTTP GET request below to check if it follows proper grammar rules</p>
        </div>
        
        <div className="px-6 pb-6 space-y-6">
          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.3 }}
            className="space-y-3"
          >
            <motion.textarea
              placeholder="GET /index.html HTTP/1.1"
              value={input}
              onChange={(e) => setInput(e.target.value)}
              whileFocus={{ scale: 1.02 }}
              className="w-full min-h-[80px] font-mono text-base border-2 border-slate-200 rounded-lg px-4 py-3 focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20 focus:outline-none transition-all duration-300 glass-card"
              onKeyDown={(e) => {
                if (e.key === 'Enter' && e.ctrlKey) {
                  e.preventDefault();
                  handleValidate();
                }
              }}
            />
            <div className="flex flex-wrap gap-2">
              <span className="text-sm text-gray-500 font-medium">Try these examples:</span>
              {examples.map((example, index) => (
                <button
                  key={index}
                  onClick={() => loadExample(example)}
                  className="text-xs px-3 py-1.5 bg-gray-100 hover:bg-blue-50 text-gray-700 hover:text-blue-700 rounded-md transition-colors duration-200 font-mono border border-gray-200 hover:border-blue-200"
                >
                  {example}
                </button>
              ))}
            </div>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.5 }}
            className="flex gap-3"
          >
            <motion.button
              onClick={handleValidate}
              disabled={!input.trim() || isValidating}
              whileHover={{ scale: 1.02 }}
              whileTap={{ scale: 0.98 }}
              className="bg-blue-600 hover:bg-blue-700 disabled:bg-gray-400 text-white font-medium px-6 py-2 rounded-lg transition-colors duration-200 flex items-center disabled:cursor-not-allowed"
            >
              {isValidating ? (
                <RotateCcw className="w-4 h-4 mr-2 animate-spin" />
              ) : (
                <Play className="w-4 h-4 mr-2" />
              )}
              {isValidating ? 'Checking...' : 'Validate Request'}
            </motion.button>
            
            <button
              onClick={handleClear}
              className="border border-gray-300 hover:bg-gray-50 text-gray-700 px-4 py-2 rounded-lg transition-colors duration-200"
            >
              Clear
            </button>
          </motion.div>
        </div>
      </motion.div>

      {/* Enhanced Results Section */}
      <AnimatePresence>
        {result && (
          <motion.div 
            initial={{ opacity: 0, y: 30, scale: 0.95 }}
            animate={{ opacity: 1, y: 0, scale: 1 }}
            exit={{ opacity: 0, y: -30, scale: 0.95 }}
            transition={{ duration: 0.5, type: "spring", stiffness: 100 }}
            className={`glass-card shadow-xl border-2 rounded-xl overflow-hidden transition-all duration-400 ${
              result.is_valid 
                ? 'border-emerald-300 bg-emerald-50/30' 
                : 'border-red-300 bg-red-50/30'
            }`}
          >
            <div className="p-6 space-y-4">
              {/* Enhanced Status Header */}
              <motion.div 
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: 0.2 }}
                className="flex items-center justify-between"
              >
                <div className="flex items-center gap-3">
                  <motion.div
                    initial={{ scale: 0, rotate: -180 }}
                    animate={{ scale: 1, rotate: 0 }}
                    transition={{ delay: 0.3, type: "spring", stiffness: 200 }}
                  >
                    {result.is_valid ? (
                      <CheckCircle className="w-6 h-6 text-emerald-600" />
                    ) : (
                      <AlertCircle className="w-6 h-6 text-red-600" />
                    )}
                  </motion.div>
                  <div>
                    <motion.h3 
                      className="font-bold text-lg"
                      initial={{ opacity: 0 }}
                      animate={{ opacity: 1 }}
                      transition={{ delay: 0.4 }}
                    >
                      {result.is_valid ? 'Valid Request ✨' : 'Invalid Request ⚠️'}
                    </motion.h3>
                    <div className="flex items-center gap-2 mt-1">
                      <span className={`text-xs px-2 py-1 rounded ${
                        result.is_valid 
                          ? 'bg-emerald-100 text-emerald-800' 
                          : 'bg-red-100 text-red-800'
                      }`}>
                        {result.is_valid ? 'success' : 'error'}
                      </span>
                      <div className="flex items-center gap-1 text-xs text-slate-500">
                        <Clock className="w-3 h-3" />
                        <span>~300ms</span>
                      </div>
                    </div>
                  </div>
                </div>
              </motion.div>

              {/* Error Message */}
              {!result.is_valid && result.errors.length > 0 && (
                <div className="border border-red-200 bg-red-50 rounded-lg p-4">
                  <div className="flex items-start gap-2">
                    <AlertCircle className="h-4 w-4 text-red-600 mt-0.5" />
                    <div className="text-red-800">
                      <strong>Error:</strong> {result.errors[0]}
                    </div>
                  </div>
                </div>
              )}

              {/* Success Message */}
              {result.is_valid && (
                <div className="border border-emerald-200 bg-emerald-50 rounded-lg p-4">
                  <div className="flex items-start gap-2">
                    <CheckCircle className="h-4 w-4 text-emerald-600 mt-0.5" />
                    <div className="text-emerald-800">
                      <strong>Success:</strong> Your HTTP request follows proper CFG syntax and is valid.
                    </div>
                  </div>
                </div>
              )}

              {/* Parse Tree Visualization */}
              {result.parse_trees && result.parse_trees.length > 0 && (
                <div className="space-y-3">
                  <h4 className="font-semibold text-slate-700">Parse Tree Structure</h4>
                  <div className="bg-white rounded-lg p-4 border border-slate-200 font-mono text-sm">
                    <div className="space-y-2">
                      <div className="text-blue-700 font-semibold">RequestLine</div>
                      <div className="ml-4 space-y-1">
                        {result.parse_trees[0].children?.map((child: any, index: number) => (
                          <div key={index} className={`ml-${index * 2} ${
                            child.label?.includes('"') ? 'text-green-700' : 'text-purple-700'
                          }`}>
                            {index === (result.parse_trees?.[0]?.children?.length || 0) - 1 ? '└─ ' : '├─ '}
                            {child.label?.includes('"') ? child.label : child.label}
                            {!child.label?.includes('"') && child.children && (
                              <span className="text-slate-500 ml-2">→ "{child.children[0]?.label}"</span>
                            )}
                          </div>
                        ))}
                      </div>
                    </div>
                  </div>
                </div>
              )}

              {/* Suggestions */}
              {!result.is_valid && (
                <div className="space-y-3">
                  <h4 className="font-semibold text-slate-700">Suggestions</h4>
                  <ul className="space-y-1 text-sm text-slate-600">
                    {getErrorSuggestions('error', input).map((suggestion, index) => (
                      <li key={index} className="flex items-start gap-2">
                        <span className="text-blue-500 mt-1">•</span>
                        {suggestion}
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
};