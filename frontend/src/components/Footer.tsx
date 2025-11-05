// Footer component for the CFG Validator application

import React from 'react';
import { Link } from 'react-router-dom';
import { Code2, Github, Heart } from 'lucide-react';

export const Footer: React.FC = () => {
  const currentYear = new Date().getFullYear();

  return (
    <footer className="bg-gray-900 text-white">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-12">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          {/* Brand section */}
          <div className="col-span-1 md:col-span-2">
            <div className="flex items-center space-x-2 mb-4">
              <div className="bg-gradient-to-br from-blue-600 to-indigo-600 p-2 rounded-lg">
                <Code2 className="w-6 h-6 text-white" />
              </div>
              <div>
                <h3 className="text-xl font-bold">CFG Validator</h3>
                <p className="text-gray-400 text-sm">HTTP Request Parser</p>
              </div>
            </div>
            <p className="text-gray-300 mb-4 max-w-md">
              A simple web app for validating HTTP GET requests using Context-Free Grammar. 
              Built to help students and developers understand CFG concepts better.
            </p>
            <div className="flex items-center space-x-4">
              <a
                href="https://github.com"
                target="_blank"
                rel="noopener noreferrer"
                className="flex items-center space-x-2 text-gray-400 hover:text-white transition-colors"
              >
                <Github className="w-5 h-5" />
                <span>GitHub</span>
              </a>
            </div>
          </div>

          {/* Quick Links */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Quick Links</h4>
            <ul className="space-y-2">
              <li>
                <Link to="/validator" className="text-gray-400 hover:text-white transition-colors">
                  Validator
                </Link>
              </li>
              <li>
                <Link to="/dashboard" className="text-gray-400 hover:text-white transition-colors">
                  Dashboard
                </Link>
              </li>
              <li>
                <Link to="/library" className="text-gray-400 hover:text-white transition-colors">
                  Request Library
                </Link>
              </li>
              <li>
                <Link to="/grammar" className="text-gray-400 hover:text-white transition-colors">
                  Grammar Rules
                </Link>
              </li>
            </ul>
          </div>

          {/* Features */}
          <div>
            <h4 className="text-lg font-semibold mb-4">Features</h4>
            <ul className="space-y-2 text-gray-400">
              <li>Real-time Validation</li>
              <li>Parse Tree Visualization</li>
              <li>Analytics Dashboard</li>
              <li>Error Pattern Analysis</li>
              <li>Interactive Grammar Explorer</li>
              <li>AI-Powered Help</li>
            </ul>
          </div>
        </div>

        {/* Bottom section */}
        <div className="border-t border-gray-800 pt-8 mt-8">
          <div className="flex flex-col md:flex-row justify-between items-center">
            <div className="flex items-center space-x-2 text-gray-400 mb-4 md:mb-0">
              <span>Built with</span>
              <Heart className="w-4 h-4 text-red-500" />
              <span>for learning</span>
            </div>
            <div className="text-gray-400 text-sm">
              © {currentYear} CFG Validator. Made for education.
            </div>
          </div>
        </div>
      </div>
    </footer>
  );
};