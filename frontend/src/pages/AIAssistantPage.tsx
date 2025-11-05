import React, { useState, useEffect, useRef } from "react";
import { Send, Bot, User, Loader2, MessageSquare, Lightbulb, Sparkles, Brain } from "lucide-react";
import { motion, AnimatePresence } from "framer-motion";
import { useAPI } from '../contexts/APIContext';
import ReactMarkdown from 'react-markdown';

interface Message {
  id: number;
  role: 'user' | 'assistant';
  content: string;
  timestamp: Date;
}

export const AIAssistantPage: React.FC = () => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [input, setInput] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);
  const { getAIHelp } = useAPI();

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  useEffect(() => {
    // Add welcome message
    setMessages([{
      id: 1,
      role: 'assistant',
      content: `# Welcome to the CFG HTTP Request Assistant! 🤖

I'm here to help you understand Context-Free Grammar rules and HTTP GET request validation. Here are some things I can help you with:

## 🎯 What I Can Do:
- Explain CFG rules and syntax
- Help debug HTTP request validation errors
- Provide examples of valid and invalid requests
- Explain HTTP protocol basics
- Guide you through parse tree interpretation

## 🚀 Try asking me:
- "Why is 'GET/index.html HTTP/1.1' invalid?"
- "Show me examples of valid request targets"
- "What's the difference between HTTP/1.1 and HTTP/2.0?"
- "How does CFG parsing work?"

Feel free to ask me anything about CFG, HTTP requests, or validation rules!`,
      timestamp: new Date()
    }]);
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!input.trim() || isLoading) return;

    const userMessage: Message = {
      id: Date.now(),
      role: 'user',
      content: input.trim(),
      timestamp: new Date()
    };

    setMessages(prev => [...prev, userMessage]);
    setInput('');
    setIsLoading(true);

    try {
      const response = await getAIHelp(input.trim());
      
      let assistantContent = '';
      
      if (response?.answer) {
        assistantContent = response.answer;
      } else {
        // Fallback responses for common questions
        const lowerInput = input.trim().toLowerCase();
        if (lowerInput.includes('cfg') || lowerInput.includes('context-free grammar')) {
          assistantContent = `## Context-Free Grammar for HTTP Requests

CFG (Context-Free Grammar) defines the syntax rules for valid HTTP GET requests:

### Grammar Rules:
- **RequestLine** → GET SP RequestTarget SP HTTPVersion
- **RequestTarget** → "/" | "/index.html" | "/about.html" | "/contact.html" | "/style.css"
- **HTTPVersion** → "HTTP/1.0" | "HTTP/1.1" | "HTTP/2.0"
- **SP** → " " (single space)

### Example Valid Requests:
\`\`\`
GET / HTTP/1.1
GET /index.html HTTP/2.0
GET /about.html HTTP/1.0
\`\`\`

Each component must be separated by exactly one space character.`;
        } else if (lowerInput.includes('error') || lowerInput.includes('invalid')) {
          assistantContent = `## Common HTTP Request Validation Errors

### 1. Missing Spaces
**Invalid:** \`GET/index.htmlHTTP/1.1\`
**Valid:** \`GET /index.html HTTP/1.1\`

### 2. Wrong HTTP Method
**Invalid:** \`POST /index.html HTTP/1.1\`
**Valid:** \`GET /index.html HTTP/1.1\`

### 3. Invalid HTTP Version
**Invalid:** \`GET /index.html HTTP/1.2\`
**Valid:** \`GET /index.html HTTP/1.1\`

### 4. Invalid Path Format
**Invalid:** \`GET index.html HTTP/1.1\` (missing /)
**Valid:** \`GET /index.html HTTP/1.1\`

Remember: Our CFG only accepts GET requests with specific predefined paths.`;
        } else if (lowerInput.includes('parse tree') || lowerInput.includes('parsing')) {
          assistantContent = `## Parse Tree Structure

A parse tree shows how a request is broken down according to CFG rules:

\`\`\`
RequestLine
├─ GET
├─ SP (" ")
├─ RequestTarget ("/index.html")
├─ SP (" ")
└─ HTTPVersion ("HTTP/1.1")
\`\`\`

### Color Coding:
- **Blue**: Root symbols (RequestLine)
- **Purple**: Non-terminal symbols (RequestTarget, HTTPVersion)
- **Green**: Terminal symbols (actual text values)

The parser validates each component matches the grammar rules exactly.`;
        } else {
          assistantContent = `I'm here to help with CFG and HTTP request validation! You can ask me about:

- **Grammar Rules**: How CFG defines valid HTTP requests
- **Validation Errors**: Why requests fail and how to fix them
- **Parse Trees**: How requests are structured
- **HTTP Syntax**: Proper formatting and components

Try asking something like "Why is my request invalid?" or "Explain parse trees".`;
        }
      }
      
      const assistantMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: assistantContent,
        timestamp: new Date()
      };

      setMessages(prev => [...prev, assistantMessage]);
    } catch (error) {
      const errorMessage: Message = {
        id: Date.now() + 1,
        role: 'assistant',
        content: 'Sorry, I encountered an error while processing your request. Please try again.',
        timestamp: new Date()
      };
      setMessages(prev => [...prev, errorMessage]);
    }

    setIsLoading(false);
  };

  const quickQuestions = [
    "Explain CFG parsing process",
    "Show HTTP request examples",
    "What are common validation errors?",
    "How do parse trees work?"
  ];

  const handleQuickQuestion = (question: string) => {
    setInput(question);
  };

  return (
    <div className="min-h-screen px-6 py-8 lg:px-8 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 gradient-overlay opacity-20"></div>
      <div className="absolute top-20 left-10 w-72 h-72 bg-gradient-to-r from-purple-400 to-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-15 animate-pulse-slow"></div>
      <div className="absolute bottom-20 right-10 w-96 h-96 bg-gradient-to-r from-blue-400 to-cyan-500 rounded-full mix-blend-multiply filter blur-xl opacity-15 animate-pulse-slow" style={{animationDelay: '2s'}}></div>
      
      <div className="relative mx-auto max-w-4xl space-y-6">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.6 }}
          className="text-center space-y-4"
        >
          <div className="inline-flex items-center gap-2 px-4 py-2 bg-purple-100 rounded-full text-purple-800 text-sm font-medium mb-4 border border-purple-200">
            <Bot className="w-4 h-4" />
            CFG Assistant
          </div>
          
          <h1 className="text-4xl lg:text-5xl font-bold text-gray-900">
            AI Assistant
          </h1>
          
          <p className="text-lg text-gray-600 max-w-2xl mx-auto leading-relaxed">
            Ask questions about CFG rules, HTTP syntax, or get help with validation errors. 
            I'm here to help you understand Context-Free Grammar better.
          </p>
        </motion.div>

        {/* Enhanced Chat Container */}
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.6, duration: 0.8 }}
          className="glass-card border border-slate-200 shadow-xl rounded-xl overflow-hidden"
        >
          <div className="border-b border-slate-100 px-6 py-4">
            <motion.div 
              initial={{ opacity: 0, x: -20 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.8 }}
              className="flex items-center gap-3"
            >
              <motion.div 
                whileHover={{ scale: 1.1, rotate: 5 }}
                className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center"
              >
                <MessageSquare className="w-4 h-4 text-white" />
              </motion.div>
              <div>
                <h3 className="text-lg font-bold text-slate-900">CFG Expert Assistant</h3>
                <div className="flex items-center gap-2">
                  <motion.div 
                    animate={{ scale: [1, 1.2, 1] }}
                    transition={{ duration: 2, repeat: Infinity }}
                    className="w-2 h-2 bg-emerald-500 rounded-full"
                  ></motion.div>
                  <span className="text-xs text-emerald-700 bg-emerald-100 px-2 py-1 rounded-full border border-emerald-200">Online</span>
                </div>
              </div>
            </motion.div>
          </div>
          
          <div className="p-0">
            {/* Messages Area */}
            <div className="h-96 overflow-y-auto p-6 space-y-4">
              <AnimatePresence>
                {messages.map((message) => (
                  <motion.div
                    key={message.id}
                    initial={{ opacity: 0, y: 20 }}
                    animate={{ opacity: 1, y: 0 }}
                    exit={{ opacity: 0, y: -20 }}
                    transition={{ duration: 0.3 }}
                    className={`flex gap-3 ${message.role === 'user' ? 'justify-end' : 'justify-start'}`}
                  >
                    {message.role === 'assistant' && (
                      <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center flex-shrink-0 mt-1">
                        <Bot className="w-4 h-4 text-white" />
                      </div>
                    )}
                    <div className={`max-w-[85%] ${message.role === 'user' ? 'order-2' : ''}`}>
                      <div className={`rounded-2xl px-4 py-3 ${
                        message.role === 'user' 
                          ? 'bg-gradient-to-r from-blue-500 to-blue-600 text-white' 
                          : 'bg-white border border-slate-200'
                      }`}>
                        {message.role === 'user' ? (
                          <p className="text-sm leading-relaxed">{message.content}</p>
                        ) : (
                          <div className="prose prose-sm max-w-none [&>*:first-child]:mt-0 [&>*:last-child]:mb-0 [&_code]:bg-slate-100 [&_code]:px-1 [&_code]:py-0.5 [&_code]:rounded [&_code]:text-xs [&_pre]:bg-slate-900 [&_pre]:text-slate-100 [&_pre]:p-3 [&_pre]:rounded-lg [&_pre]:overflow-x-auto">
                            <ReactMarkdown 
                              components={{
                                h1: ({ children }) => <h1 className="text-lg font-bold mb-2 text-slate-900">{children}</h1>,
                                h2: ({ children }) => <h2 className="text-base font-semibold mb-2 text-slate-800">{children}</h2>,
                                h3: ({ children }) => <h3 className="text-sm font-semibold mb-1 text-slate-700">{children}</h3>,
                                p: ({ children }) => <p className="mb-2 last:mb-0 leading-relaxed text-slate-700">{children}</p>,
                                ul: ({ children }) => <ul className="list-disc list-inside mb-2 space-y-1">{children}</ul>,
                                li: ({ children }) => <li className="text-sm text-slate-600">{children}</li>
                              }}
                            >
                              {message.content}
                            </ReactMarkdown>
                          </div>
                        )}
                      </div>
                    </div>
                    {message.role === 'user' && (
                      <div className="w-8 h-8 bg-gradient-to-br from-slate-400 to-slate-500 rounded-lg flex items-center justify-center flex-shrink-0 mt-1 order-1">
                        <User className="w-4 h-4 text-white" />
                      </div>
                    )}
                  </motion.div>
                ))}
              </AnimatePresence>
              
              {isLoading && (
                <motion.div
                  initial={{ opacity: 0, y: 20 }}
                  animate={{ opacity: 1, y: 0 }}
                  className="flex gap-3 justify-start"
                >
                  <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                  <div className="bg-white border border-slate-200 rounded-2xl px-4 py-3">
                    <div className="flex items-center gap-2 text-slate-600">
                      <Loader2 className="w-4 h-4 animate-spin" />
                      <span className="text-sm">Thinking...</span>
                    </div>
                  </div>
                </motion.div>
              )}
              
              <div ref={messagesEndRef} />
            </div>

            {/* Quick Questions */}
            {messages.length <= 1 && (
              <div className="px-6 pb-4 border-b border-slate-100">
                <div className="flex items-center gap-2 mb-3">
                  <Lightbulb className="w-4 h-4 text-amber-500" />
                  <span className="text-sm font-medium text-slate-600">Quick Questions:</span>
                </div>
                <div className="flex flex-wrap gap-2">
                  {quickQuestions.map((question, index) => (
                    <button
                      key={index}
                      onClick={() => handleQuickQuestion(question)}
                      className="text-xs px-3 py-2 bg-slate-50 hover:bg-blue-50 text-slate-600 hover:text-blue-700 rounded-lg transition-colors border border-slate-200 hover:border-blue-200"
                    >
                      {question}
                    </button>
                  ))}
                </div>
              </div>
            )}

            {/* Input Area */}
            <div className="p-6">
              <form onSubmit={handleSubmit} className="flex gap-3">
                <input
                  value={input}
                  onChange={(e) => setInput(e.target.value)}
                  placeholder="Ask about CFG rules, HTTP syntax, or validation errors..."
                  className="flex-1 px-4 py-2 border border-slate-200 rounded-lg focus:border-blue-400 focus:ring-2 focus:ring-blue-400/20 focus:outline-none transition-all duration-200"
                  disabled={isLoading}
                />
                <button 
                  type="submit" 
                  disabled={!input.trim() || isLoading}
                  className="bg-gradient-to-r from-blue-500 to-purple-600 hover:from-blue-600 hover:to-purple-700 text-white px-4 py-2 rounded-lg disabled:opacity-50 disabled:cursor-not-allowed transition-all duration-300 flex items-center justify-center min-w-[44px]"
                >
                  {isLoading ? (
                    <Loader2 className="w-4 h-4 animate-spin" />
                  ) : (
                    <Send className="w-4 h-4" />
                  )}
                </button>
              </form>
            </div>
          </div>
        </motion.div>
      </div>
    </div>
  );
};