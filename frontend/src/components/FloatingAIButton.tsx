import React from 'react';
import { motion } from 'framer-motion';
import { Bot, X, Sparkles } from 'lucide-react';
import { Link } from 'react-router-dom';

interface FloatingAIButtonProps {
  onClick?: () => void;
  isOpen?: boolean;
  className?: string;
}

export const FloatingAIButton: React.FC<FloatingAIButtonProps> = ({ 
  onClick, 
  isOpen = false, 
  className = "" 
}) => {
  return (
    <motion.div
      initial={{ scale: 0, rotate: -180 }}
      animate={{ scale: 1, rotate: 0 }}
      transition={{ delay: 1, type: "spring", stiffness: 200 }}
      whileHover={{ scale: 1.1 }}
      whileTap={{ scale: 0.9 }}
      className={`floating-ai-btn fixed bottom-6 right-6 z-50 ${className}`}
    >
      <Link
        to="/assistant"
        className={`group w-14 h-14 rounded-full shadow-lg transition-all duration-300 flex items-center justify-center overflow-hidden ${
          isOpen
            ? 'bg-gray-600 hover:bg-gray-700'
            : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700'
        }`}
        title={isOpen ? 'Close AI Assistant' : 'Open AI Assistant'}
        onClick={onClick}
      >
        <motion.div
          animate={isOpen ? { rotate: 180 } : { rotate: 0 }}
          transition={{ duration: 0.3 }}
        >
          {isOpen ? (
            <X className="w-6 h-6 text-white" />
          ) : (
            <>
              <motion.div
                animate={{ y: [0, -2, 0] }}
                transition={{ duration: 2, repeat: Infinity, ease: "easeInOut" }}
              >
                <Bot className="w-6 h-6 text-white" />
              </motion.div>
              
              {/* Floating particles effect */}
              <motion.div
                className="absolute -top-1 -right-1 w-4 h-4 bg-gradient-to-r from-green-400 to-emerald-500 rounded-full flex items-center justify-center"
                animate={{ scale: [1, 1.2, 1] }}
                transition={{ duration: 2, repeat: Infinity }}
              >
                <motion.div 
                  className="w-2 h-2 bg-white rounded-full"
                  animate={{ opacity: [1, 0.5, 1] }}
                  transition={{ duration: 1.5, repeat: Infinity }}
                ></motion.div>
              </motion.div>
              
              {/* Sparkle effect */}
              <motion.div
                className="absolute top-0 left-0 w-3 h-3 text-yellow-400"
                animate={{ 
                  scale: [0, 1, 0],
                  rotate: [0, 180, 360],
                  opacity: [0, 1, 0] 
                }}
                transition={{ 
                  duration: 3, 
                  repeat: Infinity,
                  repeatDelay: 2 
                }}
              >
                <Sparkles className="w-3 h-3" />
              </motion.div>
            </>
          )}
        </motion.div>
      </Link>
    </motion.div>
  );
};