import React from 'react';
import { ArrowRight, Info } from 'lucide-react';

interface Rule {
  left: string;
  right: string[];
  description: string;
  type: 'production' | 'terminal';
  color: string;
}

export const CFGRules: React.FC = () => {
  const rules: Rule[] = [
    {
      left: 'RequestLine',
      right: ['GET', 'SP', 'RequestTarget', 'SP', 'HTTPVersion'],
      description: 'A complete HTTP request line structure',
      type: 'production',
      color: 'from-blue-500 to-blue-600'
    },
    {
      left: 'RequestTarget',
      right: ['/', '/index.html', '/about.html', '/contact.html', '/style.css'],
      description: 'Valid request paths and file targets',
      type: 'terminal',
      color: 'from-emerald-500 to-emerald-600'
    },
    {
      left: 'HTTPVersion',
      right: ['HTTP/1.0', 'HTTP/1.1', 'HTTP/2.0'],
      description: 'Supported HTTP protocol versions',
      type: 'terminal',
      color: 'from-purple-500 to-purple-600'
    },
    {
      left: 'SP',
      right: ['" "'],
      description: 'Single space character separator',
      type: 'terminal',
      color: 'from-orange-500 to-orange-600'
    }
  ];

  return (
    <div className="bg-white/70 backdrop-blur-sm border border-slate-200 shadow-xl rounded-xl overflow-hidden">
      <div className="px-6 py-4 border-b border-slate-200">
        <div className="flex items-center gap-3 text-2xl font-bold">
          <div className="w-8 h-8 bg-gradient-to-br from-blue-500 to-blue-600 rounded-lg flex items-center justify-center">
            <Info className="w-4 h-4 text-white" />
          </div>
          Context-Free Grammar Rules
        </div>
        <p className="text-slate-600 mt-2">
          Formal grammar definition for HTTP GET request validation
        </p>
      </div>
      <div className="p-6">
        <div className="space-y-6">
          {rules.map((rule, index) => (
            <div key={index} className="group">
              <div className="border border-slate-100 hover:border-blue-200 transition-all duration-300 hover:shadow-lg rounded-xl overflow-hidden">
                <div className="p-6">
                  <div className="space-y-4">
                    {/* Rule Header */}
                    <div className="flex items-center gap-3">
                      <span className={`bg-gradient-to-r ${rule.color} text-white border-0 px-3 py-1 rounded-lg text-sm font-medium`}>
                        {rule.type === 'production' ? 'Production Rule' : 'Terminal Rule'}
                      </span>
                      <span className="text-sm text-slate-500">Rule {index + 1}</span>
                    </div>

                    {/* Rule Definition */}
                    <div className="space-y-3">
                      <div className="flex items-center gap-4 font-mono text-lg">
                        <span className="font-semibold text-blue-700 bg-blue-50 px-3 py-1 rounded-lg">
                          {rule.left}
                        </span>
                        <ArrowRight className="w-5 h-5 text-slate-400 group-hover:text-blue-500 transition-colors" />
                        <div className="flex flex-wrap items-center gap-2">
                          {rule.right.map((term, termIndex) => (
                            <React.Fragment key={termIndex}>
                              <span className={`px-3 py-1 rounded-lg ${
                                term.startsWith('/') || term.startsWith('HTTP') || term === 'GET' || term.includes('"')
                                  ? 'bg-emerald-50 text-emerald-700 border border-emerald-200'
                                  : 'bg-purple-50 text-purple-700 border border-purple-200'
                              }`}>
                                {term}
                              </span>
                              {termIndex < rule.right.length - 1 && rule.type === 'production' && (
                                <span className="text-slate-400 text-sm">·</span>
                              )}
                              {termIndex < rule.right.length - 1 && rule.type === 'terminal' && (
                                <span className="text-slate-400">|</span>
                              )}
                            </React.Fragment>
                          ))}
                        </div>
                      </div>

                      <div className="bg-slate-50 rounded-lg p-4 border-l-4 border-blue-400">
                        <p className="text-slate-700 text-sm leading-relaxed">
                          <strong>Description:</strong> {rule.description}
                        </p>
                      </div>
                    </div>

                    {/* Examples */}
                    {rule.left === 'RequestLine' && (
                      <div className="space-y-2">
                        <h4 className="text-sm font-semibold text-slate-700">Valid Examples:</h4>
                        <div className="space-y-1">
                          {[
                            'GET / HTTP/1.1',
                            'GET /index.html HTTP/2.0',
                            'GET /about.html HTTP/1.0'
                          ].map((example, i) => (
                            <code key={i} className="block text-xs bg-slate-900 text-slate-100 px-3 py-2 rounded font-mono">
                              {example}
                            </code>
                          ))}
                        </div>
                      </div>
                    )}
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* Grammar Notes */}
        <div className="mt-8 p-6 bg-blue-50 rounded-xl border border-blue-100">
          <h3 className="font-bold text-blue-900 mb-3 flex items-center gap-2">
            <Info className="w-5 h-5" />
            Grammar Notes
          </h3>
          <ul className="space-y-2 text-sm text-blue-800">
            <li>• Non-terminal symbols are shown in <strong>colored backgrounds</strong></li>
            <li>• Terminal symbols represent actual text that must appear in the request</li>
            <li>• The pipe symbol (|) indicates alternative choices for terminal rules</li>
            <li>• SP represents a single space character that separates components</li>
            <li>• All parsing is case-sensitive and whitespace-sensitive</li>
          </ul>
        </div>
      </div>
    </div>
  );
};