// AI Assistant component for helping users with CFG rules and HTTP syntax

import React, { useState, useRef, useEffect } from 'react';
import {
  MessageCircle,
  Send,
  Bot,
  User,
  Lightbulb,
  RefreshCw,
  Copy,
  ExternalLink,
  Minimize2,
  Maximize2
} from 'lucide-react';
import { useAPI } from '../contexts/APIContext';
import { useNotifications } from '../contexts/NotificationContext';
import type { AIHelpResponse } from '../types';

interface Message {
  id: string;
  type: 'user' | 'assistant';
  content: string;
  timestamp: Date;
  links?: { title: string; url: string }[];
}

interface AIAssistantProps {
  isCompact?: boolean;
  onToggleSize?: () => void;
}

export const AIAssistant: React.FC<AIAssistantProps> = ({ 
  isCompact = false, 
  onToggleSize 
}) => {
  const [messages, setMessages] = useState<Message[]>([
    {
      id: '1',
      type: 'assistant',
      content: 'Hello! I\'m your CFG assistant. I can help you understand Context-Free Grammar rules, HTTP syntax, validation errors, and more. What would you like to learn about?',
      timestamp: new Date(),
      links: [
        { title: 'Grammar Rules', url: '/grammar' },
        { title: 'Examples', url: '/library' },
        { title: 'Error Patterns', url: '/errors' }
      ]
    }
  ]);
  const [currentMessage, setCurrentMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  
  const { getAIHelp } = useAPI();
  const { showError, showSuccess } = useNotifications();

  // Quick suggestion buttons
  const quickSuggestions = [
    'What is CFG?',
    'How do HTTP requests work?',
    'Common validation errors',
    'Grammar rule examples',
    'Parse tree explanation'
  ];

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  const handleSendMessage = async (messageText?: string) => {
    const text = messageText || currentMessage.trim();
    if (!text) return;

    // Add user message
    const userMessage: Message = {
      id: Date.now().toString(),
      type: 'user',
      content: text,
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setCurrentMessage('');
    setIsLoading(true);

    try {
      const response = await getAIHelp(text);
      
      if (response) {
        const assistantMessage: Message = {
          id: (Date.now() + 1).toString(),
          type: 'assistant',
          content: response.answer,
          timestamp: new Date(),
          links: response.helpful_links
        };
        
        setMessages(prev => [...prev, assistantMessage]);
      } else {
        throw new Error('No response received');
      }
    } catch (error) {
      const errorMessage: Message = {
        id: (Date.now() + 1).toString(),
        type: 'assistant',
        content: 'I\'m sorry, I\'m having trouble responding right now. Please try asking about CFG rules, HTTP syntax, validation errors, or grammar examples.',
        timestamp: new Date()
      };
      
      setMessages(prev => [...prev, errorMessage]);
      showError('AI Assistant', 'Failed to get response');
    } finally {
      setIsLoading(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleCopyMessage = (content: string) => {
    navigator.clipboard.writeText(content).then(() => {
      showSuccess('Copied', 'Message copied to clipboard');
    }).catch(() => {
      showError('Copy Failed', 'Failed to copy message');
    });
  };

  const clearChat = () => {
    setMessages([
      {
        id: '1',
        type: 'assistant',
        content: 'Chat cleared! How can I help you with CFG and HTTP validation?',
        timestamp: new Date()
      }
    ]);
  };

  return (
    <div className={`bg-white rounded-xl shadow-sm border border-gray-200 flex flex-col ${
      isCompact ? 'h-96' : 'h-128'
    }`}>
      {/* Header */}
      <div className="flex items-center justify-between p-4 border-b border-gray-200">
        <div className="flex items-center space-x-2">
          <div className="p-2 bg-gradient-to-r from-blue-500 to-indigo-500 rounded-lg">
            <Bot className="w-5 h-5 text-white" />
          </div>
          <div>
            <h3 className="font-semibold text-gray-900">CFG Assistant</h3>
            <p className="text-xs text-gray-500">Always ready to help</p>
          </div>
        </div>
        
        <div className="flex items-center space-x-2">
          <button
            onClick={clearChat}
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
            title="Clear chat"
          >
            <RefreshCw className="w-4 h-4" />
          </button>
          {onToggleSize && (
            <button
              onClick={onToggleSize}
              className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
              title={isCompact ? 'Expand' : 'Minimize'}
            >
              {isCompact ? <Maximize2 className="w-4 h-4" /> : <Minimize2 className="w-4 h-4" />}
            </button>
          )}
        </div>
      </div>

      {/* Messages */}
      <div className="flex-1 overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex items-start space-x-3 ${
              message.type === 'user' ? 'flex-row-reverse space-x-reverse' : ''
            }`}
          >
            {/* Avatar */}
            <div className={`flex-shrink-0 w-8 h-8 rounded-full flex items-center justify-center ${
              message.type === 'user'
                ? 'bg-blue-600'
                : 'bg-gradient-to-r from-green-500 to-emerald-500'
            }`}>
              {message.type === 'user' ? (
                <User className="w-4 h-4 text-white" />
              ) : (
                <Bot className="w-4 h-4 text-white" />
              )}
            </div>
            
            {/* Message Bubble */}
            <div className={`flex-1 max-w-xs lg:max-w-sm ${
              message.type === 'user' ? 'text-right' : ''
            }`}>
              <div className={`inline-block p-3 rounded-lg ${
                message.type === 'user'
                  ? 'bg-blue-600 text-white'
                  : 'bg-gray-100 text-gray-900'
              }`}>
                <p className="text-sm whitespace-pre-wrap">{message.content}</p>
                
                {/* Links */}
                {message.links && message.links.length > 0 && (
                  <div className="mt-3 pt-3 border-t border-gray-200 space-y-2">
                    {message.links.map((link, index) => (
                      <a
                        key={index}
                        href={link.url}
                        className="flex items-center text-xs text-blue-600 hover:text-blue-700 transition-colors"
                      >
                        <ExternalLink className="w-3 h-3 mr-1" />
                        {link.title}
                      </a>
                    ))}
                  </div>
                )}
              </div>
              
              {/* Message Actions */}
              <div className="flex items-center mt-1 space-x-2">
                <span className="text-xs text-gray-500">
                  {message.timestamp.toLocaleTimeString([], { 
                    hour: '2-digit', 
                    minute: '2-digit' 
                  })}
                </span>
                {message.type === 'assistant' && (
                  <button
                    onClick={() => handleCopyMessage(message.content)}
                    className="text-gray-400 hover:text-gray-600 transition-colors"
                    title="Copy message"
                  >
                    <Copy className="w-3 h-3" />
                  </button>
                )}
              </div>
            </div>
          </div>
        ))}
        
        {/* Loading Indicator */}
        {isLoading && (
          <div className="flex items-start space-x-3">
            <div className="w-8 h-8 rounded-full bg-gradient-to-r from-green-500 to-emerald-500 flex items-center justify-center">
              <Bot className="w-4 h-4 text-white" />
            </div>
            <div className="bg-gray-100 p-3 rounded-lg">
              <div className="flex space-x-1">
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce"></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.1s' }}></div>
                <div className="w-2 h-2 bg-gray-400 rounded-full animate-bounce" style={{ animationDelay: '0.2s' }}></div>
              </div>
            </div>
          </div>
        )}
        
        <div ref={messagesEndRef} />
      </div>

      {/* Quick Suggestions */}
      {messages.length <= 1 && (
        <div className="px-4 pb-2">
          <div className="flex flex-wrap gap-2">
            {quickSuggestions.map((suggestion, index) => (
              <button
                key={index}
                onClick={() => handleSendMessage(suggestion)}
                className="px-3 py-1 bg-blue-50 text-blue-700 rounded-full text-xs hover:bg-blue-100 transition-colors"
              >
                {suggestion}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Input */}
      <div className="p-4 border-t border-gray-200">
        <div className="flex space-x-2">
          <input
            ref={inputRef}
            type="text"
            value={currentMessage}
            onChange={(e) => setCurrentMessage(e.target.value)}
            onKeyPress={handleKeyPress}
            placeholder="Ask about CFG rules, HTTP syntax, errors..."
            className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 text-sm transition-colors"
            disabled={isLoading}
          />
          <button
            onClick={() => handleSendMessage()}
            disabled={isLoading || !currentMessage.trim()}
            className="p-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors"
          >
            <Send className="w-4 h-4" />
          </button>
        </div>
        
        <div className="flex items-center mt-2 space-x-2">
          <Lightbulb className="w-3 h-3 text-yellow-500" />
          <span className="text-xs text-gray-500">
            Ask about grammar rules, HTTP syntax, validation errors, or examples
          </span>
        </div>
      </div>
    </div>
  );
};

// Floating AI Assistant Button for global access
interface FloatingAIButtonProps {
  onClick: () => void;
  isOpen: boolean;
}

export const FloatingAIButton: React.FC<FloatingAIButtonProps> = ({ onClick, isOpen }) => {
  return (
    <button
      onClick={onClick}
      className={`fixed bottom-6 right-6 w-14 h-14 rounded-full shadow-lg transition-all duration-300 z-50 ${
        isOpen
          ? 'bg-gray-600 hover:bg-gray-700'
          : 'bg-gradient-to-r from-blue-600 to-indigo-600 hover:from-blue-700 hover:to-indigo-700'
      }`}
      title={isOpen ? 'Close AI Assistant' : 'Open AI Assistant'}
    >
      {isOpen ? (
        <X className="w-6 h-6 text-white mx-auto" />
      ) : (
        <>
          <MessageCircle className="w-6 h-6 text-white mx-auto" />
          <div className="absolute -top-1 -right-1 w-4 h-4 bg-green-500 rounded-full flex items-center justify-center">
            <div className="w-2 h-2 bg-white rounded-full"></div>
          </div>
        </>
      )}
    </button>
  );
};

// Import X icon
const X = ({ className }: { className?: string }) => (
  <svg className={className} fill="none" stroke="currentColor" viewBox="0 0 24 24">
    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M6 18L18 6M6 6l12 12" />
  </svg>
);