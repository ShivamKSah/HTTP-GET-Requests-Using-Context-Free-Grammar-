// Navigation component for the CFG Validator application

import React, { useState } from 'react';
import { Link, useLocation } from 'react-router-dom';
import { motion, AnimatePresence } from 'framer-motion';
import { 
  Menu, 
  X, 
  Home, 
  CheckCircle, 
  TrendingUp,
  BookOpen, 
  AlertTriangle, 
  Code2,
  Bot,
  Sparkles,
  ExternalLink
} from 'lucide-react';

export const Navigation: React.FC = () => {
  const [isOpen, setIsOpen] = useState(false);
  const location = useLocation();

  const navItems = [
    { path: '/', label: 'Home', icon: Home },
    { path: '/validator', label: 'Validator', icon: CheckCircle },
    { path: '/analytics', label: 'Analytics', icon: TrendingUp },
    { path: '/library', label: 'Library', icon: BookOpen },
    { path: '/errors', label: 'Errors', icon: AlertTriangle },
    { path: '/grammar', label: 'Grammar', icon: Code2 },
    { path: '/assistant', label: 'AI Assistant', icon: Bot },
  ];

  const isActive = (path: string) => {
    return location.pathname === path;
  };

  return (
    <motion.nav 
      initial={{ y: -100 }}
      animate={{ y: 0 }}
      transition={{ duration: 0.6, ease: "easeOut" }}
      className="bg-white/80 backdrop-blur-md shadow-lg border-b border-blue-100 sticky top-0 z-50"
    >
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
        <div className="flex justify-between h-16">
          {/* More Natural Logo and brand */}
          <div className="flex items-center">
            <Link to="/" className="flex items-center space-x-3 group">
              <motion.div 
                whileHover={{ scale: 1.05 }}
                className="bg-blue-600 p-2 rounded-md group-hover:bg-blue-700 transition-colors duration-200"
              >
                <Code2 className="w-6 h-6 text-white" />
              </motion.div>
              <div>
                <h1 className="text-xl font-bold text-gray-900">
                  CFG Validator
                </h1>
                <p className="text-xs text-gray-500 hidden sm:block">HTTP Request Parser</p>
              </div>
            </Link>
          </div>

          {/* More Natural Desktop navigation */}
          <div className="hidden md:flex md:items-center md:space-x-1">
            {navItems.map(({ path, label, icon: Icon }, index) => (
              <Link
                key={path}
                to={path}
                className={`
                  px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 flex items-center space-x-2
                  ${
                    isActive(path)
                      ? 'bg-blue-100 text-blue-700 shadow-sm'
                      : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                  }
                `}
              >
                <Icon className="w-4 h-4" />
                <span>{label}</span>
              </Link>
            ))}
            
            {/* RFC 7230 Reference */}
            <div className="h-6 w-px bg-gray-300 mx-2" /> {/* Divider */}
            <a
              href="https://datatracker.ietf.org/doc/html/rfc7230"
              target="_blank"
              rel="noopener noreferrer"
              className="px-3 py-2 rounded-md text-sm font-medium transition-colors duration-200 flex items-center space-x-2 text-gray-600 hover:text-blue-600 hover:bg-blue-50 group"
              title="RFC 7230 - HTTP/1.1 Message Syntax and Routing"
            >
              <ExternalLink className="w-4 h-4" />
              <span>RFC 7230</span>
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                whileHover={{ opacity: 1, scale: 1 }}
                className="text-xs bg-blue-100 text-blue-700 px-1.5 py-0.5 rounded-full"
              >
                HTTP/1.1
              </motion.div>
            </a>
          </div>

          {/* Enhanced Mobile menu button */}
          <div className="md:hidden flex items-center">
            <motion.button
              onClick={() => setIsOpen(!isOpen)}
              whileHover={{ scale: 1.05 }}
              whileTap={{ scale: 0.95 }}
              className="p-2 rounded-md text-gray-600 hover:text-blue-600 hover:bg-blue-50 transition-colors relative"
              aria-label="Toggle menu"
            >
              <AnimatePresence mode="wait">
                {isOpen ? (
                  <motion.div
                    key="close"
                    initial={{ rotate: -90, opacity: 0 }}
                    animate={{ rotate: 0, opacity: 1 }}
                    exit={{ rotate: 90, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <X className="w-6 h-6" />
                  </motion.div>
                ) : (
                  <motion.div
                    key="menu"
                    initial={{ rotate: 90, opacity: 0 }}
                    animate={{ rotate: 0, opacity: 1 }}
                    exit={{ rotate: -90, opacity: 0 }}
                    transition={{ duration: 0.2 }}
                  >
                    <Menu className="w-6 h-6" />
                  </motion.div>
                )}
              </AnimatePresence>
            </motion.button>
          </div>
        </div>
      </div>

      {/* Enhanced Mobile navigation */}
      <AnimatePresence>
        {isOpen && (
          <motion.div 
            initial={{ opacity: 0, height: 0 }}
            animate={{ opacity: 1, height: "auto" }}
            exit={{ opacity: 0, height: 0 }}
            transition={{ duration: 0.3, ease: "easeInOut" }}
            className="md:hidden bg-white/90 backdrop-blur-md border-t border-gray-200 shadow-lg overflow-hidden"
          >
            <div className="px-2 pt-2 pb-3 space-y-1">
              {navItems.map(({ path, label, icon: Icon }, index) => (
                <motion.div
                  key={path}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  transition={{ delay: index * 0.05, duration: 0.3 }}
                >
                  <Link
                    to={path}
                    onClick={() => setIsOpen(false)}
                    className={`
                      block px-3 py-3 rounded-lg text-base font-medium transition-all duration-300 flex items-center space-x-3 group
                      ${
                        isActive(path)
                          ? 'bg-gradient-to-r from-blue-100 to-indigo-100 text-blue-700 shadow-sm'
                          : 'text-gray-600 hover:text-blue-600 hover:bg-blue-50'
                      }
                    `}
                  >
                    <motion.div
                      whileHover={{ scale: 1.1, rotate: 5 }}
                      className={`p-2 rounded-md ${
                        isActive(path) 
                          ? 'bg-blue-200' 
                          : 'bg-gray-100 group-hover:bg-blue-100'
                      }`}
                    >
                      <Icon className="w-4 h-4" />
                    </motion.div>
                    <span>{label}</span>
                  </Link>
                </motion.div>
              ))}
              
              {/* RFC 7230 Reference - Mobile */}
              <motion.div
                initial={{ opacity: 0, x: -20 }}
                animate={{ opacity: 1, x: 0 }}
                transition={{ delay: navItems.length * 0.05, duration: 0.3 }}
                className="pt-2 border-t border-gray-200 mt-2"
              >
                <a
                  href="https://datatracker.ietf.org/doc/html/rfc7230"
                  target="_blank"
                  rel="noopener noreferrer"
                  onClick={() => setIsOpen(false)}
                  className="block px-3 py-3 rounded-lg text-base font-medium transition-all duration-300 flex items-center space-x-3 group text-gray-600 hover:text-blue-600 hover:bg-blue-50"
                >
                  <motion.div
                    whileHover={{ scale: 1.1, rotate: 5 }}
                    className="p-2 rounded-md bg-gray-100 group-hover:bg-blue-100"
                  >
                    <ExternalLink className="w-4 h-4" />
                  </motion.div>
                  <div>
                    <span>RFC 7230 Reference</span>
                    <p className="text-xs text-gray-500 mt-0.5">HTTP/1.1 Message Syntax</p>
                  </div>
                </a>
              </motion.div>
            </div>
          </motion.div>
        )}
      </AnimatePresence>
    </motion.nav>
  );
};