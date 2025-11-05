// Errors Page - Detailed error insights and explanations

import React, { useEffect, useState } from 'react';
import {
  AlertTriangle,
  XCircle,
  CheckCircle,
  Lightbulb,
  Search,
  TrendingUp,
  Book,
  Copy,
  ExternalLink,
  Filter,
  BarChart3
} from 'lucide-react';
import { useAPI } from '../contexts/APIContext';
import { useNotifications } from '../contexts/NotificationContext';
import { Link } from 'react-router-dom';
import type { ErrorPattern } from '../types';

interface ErrorCardProps {
  error: ErrorPattern;
  onCopy: (text: string) => void;
  onTest: (request: string) => void;
}

const ErrorCard: React.FC<ErrorCardProps> = ({ error, onCopy, onTest }) => {
  const [isExpanded, setIsExpanded] = useState(false);

  return (
    <div className="bg-white rounded-xl shadow-sm border border-gray-200 hover:shadow-md transition-all duration-200">
      <div className="p-6">
        {/* Header */}
        <div className="flex items-start justify-between mb-4">
          <div className="flex items-start space-x-3">
            <div className="p-2 bg-red-100 rounded-lg">
              <XCircle className="w-5 h-5 text-red-600" />
            </div>
            <div>
              <h3 className="text-lg font-semibold text-gray-900 mb-1">
                {error.error_message}
              </h3>
              <div className="flex items-center space-x-4 text-sm text-gray-600">
                <span className="flex items-center">
                  <TrendingUp className="w-4 h-4 mr-1" />
                  {error.occurrence_count} occurrences
                </span>
                <span>#{error.id}</span>
              </div>
            </div>
          </div>
          
          <button
            onClick={() => setIsExpanded(!isExpanded)}
            className="p-2 text-gray-400 hover:text-gray-600 hover:bg-gray-100 rounded-lg transition-colors"
          >
            <Book className="w-5 h-5" />
          </button>
        </div>

        {/* Description */}
        {error.description && (
          <div className="mb-4">
            <p className="text-gray-700 leading-relaxed">{error.description}</p>
          </div>
        )}

        {/* Examples Preview */}
        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
          {error.example_incorrect && (
            <div>
              <h4 className="text-sm font-medium text-red-800 mb-2 flex items-center">
                <XCircle className="w-4 h-4 mr-1" />
                Incorrect Example
              </h4>
              <div className="bg-red-50 border border-red-200 rounded-lg p-3">
                <code className="text-sm font-mono text-red-800">
                  {error.example_incorrect}
                </code>
                <div className="flex space-x-2 mt-2">
                  <button
                    onClick={() => onCopy(error.example_incorrect)}
                    className="text-xs text-red-600 hover:text-red-700"
                  >
                    Copy
                  </button>
                  <button
                    onClick={() => onTest(error.example_incorrect)}
                    className="text-xs text-red-600 hover:text-red-700"
                  >
                    Test
                  </button>
                </div>
              </div>
            </div>
          )}
          
          {error.example_correct && (
            <div>
              <h4 className="text-sm font-medium text-green-800 mb-2 flex items-center">
                <CheckCircle className="w-4 h-4 mr-1" />
                Correct Example
              </h4>
              <div className="bg-green-50 border border-green-200 rounded-lg p-3">
                <code className="text-sm font-mono text-green-800">
                  {error.example_correct}
                </code>
                <div className="flex space-x-2 mt-2">
                  <button
                    onClick={() => onCopy(error.example_correct)}
                    className="text-xs text-green-600 hover:text-green-700"
                  >
                    Copy
                  </button>
                  <button
                    onClick={() => onTest(error.example_correct)}
                    className="text-xs text-green-600 hover:text-green-700"
                  >
                    Test
                  </button>
                </div>
              </div>
            </div>
          )}
        </div>

        {/* Expanded Content */}
        {isExpanded && (
          <div className="border-t border-gray-200 pt-4">
            {error.solution && (
              <div className="mb-4">
                <h4 className="text-sm font-medium text-blue-800 mb-2 flex items-center">
                  <Lightbulb className="w-4 h-4 mr-1" />
                  Solution
                </h4>
                <div className="bg-blue-50 border border-blue-200 rounded-lg p-3">
                  <p className="text-sm text-blue-900">{error.solution}</p>
                </div>
              </div>
            )}
            
            {/* Metadata */}
            <div className="grid grid-cols-2 gap-4 text-xs text-gray-500">
              <div>
                <span className="font-medium">Created:</span>{' '}
                {new Date(error.created_at).toLocaleDateString()}
              </div>
              <div>
                <span className="font-medium">Last Updated:</span>{' '}
                {new Date(error.updated_at).toLocaleDateString()}
              </div>
            </div>
          </div>
        )}
        
        {/* Action Buttons */}
        <div className="flex space-x-2 mt-4">
          <Link
            to="/validator"
            className="flex-1 flex items-center justify-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors text-sm"
          >
            Test in Validator
          </Link>
          <Link
            to="/grammar"
            className="flex items-center justify-center px-4 py-2 bg-gray-100 text-gray-700 rounded-lg hover:bg-gray-200 transition-colors text-sm"
          >
            <ExternalLink className="w-4 h-4" />
          </Link>
        </div>
      </div>
    </div>
  );
};

interface StatsCardProps {
  title: string;
  value: string | number;
  description: string;
  icon: React.ElementType;
  color: string;
}

const StatsCard: React.FC<StatsCardProps> = ({ title, value, description, icon: Icon, color }) => (
  <div className="bg-white p-6 rounded-xl shadow-sm border border-gray-200">
    <div className="flex items-center justify-between mb-4">
      <div className={`p-3 rounded-lg ${color}`}>
        <Icon className="w-6 h-6 text-white" />
      </div>
      <div className="text-right">
        <div className="text-2xl font-bold text-gray-900">{value}</div>
        <div className="text-sm text-gray-600">{title}</div>
      </div>
    </div>
    <p className="text-sm text-gray-600">{description}</p>
  </div>
);

export const ErrorsPage: React.FC = () => {
  const [errorPatterns, setErrorPatterns] = useState<ErrorPattern[]>([]);
  const [filteredErrors, setFilteredErrors] = useState<ErrorPattern[]>([]);
  const [searchTerm, setSearchTerm] = useState('');
  const [sortBy, setSortBy] = useState<'frequency' | 'recent' | 'alphabetical'>('frequency');
  const [isLoading, setIsLoading] = useState(true);
  
  const { getErrorPatterns } = useAPI();
  const { showSuccess, showError } = useNotifications();

  // Mock error patterns for demonstration
  const mockErrorPatterns: ErrorPattern[] = [
    {
      id: 1,
      error_message: 'Invalid HTTP method',
      description: 'The request line must start with the GET method. Other HTTP methods like POST, PUT, DELETE are not supported by this validator according to the CFG rules.',
      solution: 'Ensure your request line starts with "GET" (case-sensitive) followed by a space. Example: "GET /index.html HTTP/1.1"',
      example_correct: 'GET /index.html HTTP/1.1',
      example_incorrect: 'POST /index.html HTTP/1.1',
      occurrence_count: 145,
      created_at: '2024-01-15T10:00:00Z',
      updated_at: '2024-01-20T15:30:00Z'
    },
    {
      id: 2,
      error_message: 'Invalid filename',
      description: 'Only specific filenames are allowed in the request target according to the CFG rules. The validator supports a limited set of files for educational purposes.',
      solution: 'Use one of the allowed filenames: index.html, about.html, contact.html, or style.css. Example: "GET /about.html HTTP/1.1"',
      example_correct: 'GET /contact.html HTTP/1.1',
      example_incorrect: 'GET /page.html HTTP/1.1',
      occurrence_count: 128,
      created_at: '2024-01-15T10:00:00Z',
      updated_at: '2024-01-19T12:15:00Z'
    },
    {
      id: 3,
      error_message: 'Missing space',
      description: 'HTTP request components must be separated by exactly one space character. The CFG requires specific spacing between the method, target, and version.',
      solution: 'Ensure there is exactly one space between GET and the request target, and between the request target and HTTP version.',
      example_correct: 'GET /index.html HTTP/1.1',
      example_incorrect: 'GET/index.html HTTP/1.1',
      occurrence_count: 89,
      created_at: '2024-01-15T10:00:00Z',
      updated_at: '2024-01-18T09:45:00Z'
    },
    {
      id: 4,
      error_message: 'Invalid HTTP version',
      description: 'Only specific HTTP versions are supported according to the CFG rules. The validator accepts HTTP/1.0, HTTP/1.1, and HTTP/2.0.',
      solution: 'Use one of the supported HTTP versions: HTTP/1.0, HTTP/1.1, or HTTP/2.0 (case-sensitive).',
      example_correct: 'GET /index.html HTTP/2.0',
      example_incorrect: 'GET /index.html HTTP/3.0',
      occurrence_count: 76,
      created_at: '2024-01-15T10:00:00Z',
      updated_at: '2024-01-17T14:20:00Z'
    },
    {
      id: 5,
      error_message: 'Incomplete request line',
      description: 'The HTTP request line is missing required components. A complete request line must have three parts: method, target, and version, separated by spaces.',
      solution: 'Include all three components: GET, request target (starting with /), and HTTP version. Example: "GET /index.html HTTP/1.1"',
      example_correct: 'GET /index.html HTTP/1.1',
      example_incorrect: 'GET /index.html',
      occurrence_count: 63,
      created_at: '2024-01-15T10:00:00Z',
      updated_at: '2024-01-16T11:10:00Z'
    },
    {
      id: 6,
      error_message: 'Invalid request target',
      description: 'The request target must start with a forward slash (/) and can either be just "/" for the root or "/{filename}" for specific files.',
      solution: 'Use "/" for root requests or "/{filename}" where filename is one of the allowed files.',
      example_correct: 'GET /about.html HTTP/1.1',
      example_incorrect: 'GET about.html HTTP/1.1',
      occurrence_count: 52,
      created_at: '2024-01-15T10:00:00Z',
      updated_at: '2024-01-15T16:30:00Z'
    }
  ];

  useEffect(() => {
    const loadErrorPatterns = async () => {
      setIsLoading(true);
      try {
        const patterns = await getErrorPatterns();
        if (patterns) {
          setErrorPatterns(patterns);
        } else {
          // Use mock data if API fails
          setErrorPatterns(mockErrorPatterns);
        }
      } catch (error) {
        setErrorPatterns(mockErrorPatterns);
        showError('Warning', 'Using demo data - API not available');
      } finally {
        setIsLoading(false);
      }
    };

    loadErrorPatterns();
  }, [getErrorPatterns, showError]);

  useEffect(() => {
    let filtered = errorPatterns;
    
    // Apply search
    if (searchTerm) {
      filtered = filtered.filter(error => 
        error.error_message.toLowerCase().includes(searchTerm.toLowerCase()) ||
        error.description.toLowerCase().includes(searchTerm.toLowerCase()) ||
        error.solution.toLowerCase().includes(searchTerm.toLowerCase())
      );
    }
    
    // Apply sorting
    filtered = [...filtered].sort((a, b) => {
      switch (sortBy) {
        case 'frequency':
          return b.occurrence_count - a.occurrence_count;
        case 'recent':
          return new Date(b.updated_at).getTime() - new Date(a.updated_at).getTime();
        case 'alphabetical':
          return a.error_message.localeCompare(b.error_message);
        default:
          return 0;
      }
    });
    
    setFilteredErrors(filtered);
  }, [errorPatterns, searchTerm, sortBy]);

  const handleCopyText = (text: string) => {
    navigator.clipboard.writeText(text).then(() => {
      showSuccess('Copied', 'Text copied to clipboard');
    }).catch(() => {
      showError('Copy Failed', 'Failed to copy to clipboard');
    });
  };

  const handleTestRequest = (request: string) => {
    // This would typically navigate to validator with the request
    showSuccess('Redirecting', 'Opening validator with example request');
  };

  const totalOccurrences = errorPatterns.reduce((sum, error) => sum + error.occurrence_count, 0);
  const mostCommonError = errorPatterns.reduce((max, error) => 
    error.occurrence_count > (max?.occurrence_count || 0) ? error : max, errorPatterns[0]
  );

  if (isLoading) {
    return (
      <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100 flex items-center justify-center">
        <div className="text-center">
          <div className="loading-spinner w-12 h-12 mx-auto mb-4"></div>
          <p className="text-gray-600">Loading error patterns...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-gradient-to-br from-blue-50 to-indigo-100">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8">
        {/* Header */}
        <div className="text-center mb-8">
          <h1 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
            Error
            <span className="block text-transparent bg-clip-text bg-gradient-to-r from-red-600 to-pink-600">
              Insights
            </span>
          </h1>
          <p className="text-xl text-gray-600 max-w-3xl mx-auto">
            Understand common validation errors and learn how to fix them. 
            Each error pattern includes detailed explanations, examples, and solutions.
          </p>
        </div>

        {/* Stats */}
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
          <StatsCard
            title="Total Patterns"
            value={errorPatterns.length}
            description="Different types of errors tracked"
            icon={AlertTriangle}
            color="bg-gradient-to-r from-red-500 to-red-600"
          />
          <StatsCard
            title="Total Occurrences"
            value={totalOccurrences.toLocaleString()}
            description="Total error instances recorded"
            icon={BarChart3}
            color="bg-gradient-to-r from-orange-500 to-orange-600"
          />
          <StatsCard
            title="Most Common"
            value={mostCommonError?.occurrence_count || 0}
            description={mostCommonError?.error_message.substring(0, 20) + '...' || 'N/A'}
            icon={TrendingUp}
            color="bg-gradient-to-r from-yellow-500 to-yellow-600"
          />
          <StatsCard
            title="Filtered Results"
            value={filteredErrors.length}
            description="Matching your current filters"
            icon={Filter}
            color="bg-gradient-to-r from-blue-500 to-blue-600"
          />
        </div>

        {/* Controls */}
        <div className="bg-white rounded-xl shadow-sm border border-gray-200 p-6 mb-8">
          <div className="flex flex-col lg:flex-row lg:items-center lg:justify-between space-y-4 lg:space-y-0">
            {/* Search */}
            <div className="relative flex-1 max-w-md">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-5 h-5 text-gray-400" />
              <input
                type="text"
                placeholder="Search errors, descriptions, solutions..."
                value={searchTerm}
                onChange={(e) => setSearchTerm(e.target.value)}
                className="w-full pl-10 pr-4 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              />
            </div>
            
            {/* Sort */}
            <div className="flex items-center space-x-3">
              <label className="text-sm font-medium text-gray-700">Sort by:</label>
              <select
                value={sortBy}
                onChange={(e) => setSortBy(e.target.value as any)}
                className="px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-blue-500 transition-colors"
              >
                <option value="frequency">Most Frequent</option>
                <option value="recent">Recently Updated</option>
                <option value="alphabetical">Alphabetical</option>
              </select>
            </div>
          </div>
        </div>

        {/* Error Patterns Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-6 mb-8">
          {filteredErrors.map((error) => (
            <ErrorCard
              key={error.id}
              error={error}
              onCopy={handleCopyText}
              onTest={handleTestRequest}
            />
          ))}
        </div>
        
        {filteredErrors.length === 0 && (
          <div className="text-center py-12">
            <AlertTriangle className="w-16 h-16 text-gray-300 mx-auto mb-4" />
            <h3 className="text-lg font-medium text-gray-900 mb-2">No error patterns found</h3>
            <p className="text-gray-600 mb-4">Try adjusting your search criteria or check back later.</p>
            <Link
              to="/validator"
              className="inline-flex items-center px-4 py-2 bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              Test Requests in Validator
            </Link>
          </div>
        )}

        {/* Help Section */}
        <div className="bg-gradient-to-r from-blue-600 to-indigo-600 rounded-xl p-8 text-white text-center">
          <h3 className="text-2xl font-bold mb-4">Still Having Issues?</h3>
          <p className="text-blue-100 mb-6">
            Use our validator to test your requests and get real-time feedback, 
            or explore our grammar rules to understand the CFG better.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/validator"
              className="inline-flex items-center px-6 py-3 bg-white text-blue-600 font-semibold rounded-lg hover:bg-blue-50 transition-colors"
            >
              <XCircle className="w-5 h-5 mr-2" />
              Test Requests
            </Link>
            <Link
              to="/grammar"
              className="inline-flex items-center px-6 py-3 bg-blue-700 text-white font-semibold rounded-lg hover:bg-blue-800 transition-colors"
            >
              <Book className="w-5 h-5 mr-2" />
              Study Grammar
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};