import React, { useState, useEffect } from "react";
import { Copy, Search, Filter, CheckCircle, XCircle, BookOpen } from "lucide-react";

interface RequestTemplate {
  id: number;
  name: string;
  request_line: string;
  description: string;
  category: string;
  difficulty_level: string;
  expected_result: boolean;
  created_date: string;
}

// Mock RequestTemplate entity
const RequestTemplate = {
  list: async (orderBy?: string): Promise<RequestTemplate[]> => {
    // Comprehensive mock data - replace with actual API call
    return [
      // Valid Basic Requests
      {
        id: 1,
        name: "Basic Root Request",
        request_line: "GET / HTTP/1.1",
        description: "Simplest valid HTTP GET request to the root path",
        category: "valid_basic",
        difficulty_level: "beginner",
        expected_result: true,
        created_date: new Date().toISOString()
      },
      {
        id: 2,
        name: "HTML File Request",
        request_line: "GET /index.html HTTP/1.1",
        description: "Standard request for an HTML file",
        category: "valid_basic",
        difficulty_level: "beginner",
        expected_result: true,
        created_date: new Date().toISOString()
      },
      {
        id: 3,
        name: "About Page Request",
        request_line: "GET /about.html HTTP/1.1",
        description: "Request for about page with HTTP/1.1",
        category: "valid_basic",
        difficulty_level: "beginner",
        expected_result: true,
        created_date: new Date().toISOString()
      },
      {
        id: 4,
        name: "Contact Page Request",
        request_line: "GET /contact.html HTTP/1.0",
        description: "Request for contact page with older HTTP/1.0",
        category: "valid_basic",
        difficulty_level: "beginner",
        expected_result: true,
        created_date: new Date().toISOString()
      },
      {
        id: 5,
        name: "Services Page Request",
        request_line: "GET /services.html HTTP/2.0",
        description: "Request for services page using HTTP/2.0",
        category: "valid_basic",
        difficulty_level: "beginner",
        expected_result: true,
        created_date: new Date().toISOString()
      },

      // Valid Advanced Requests  
      {
        id: 6,
        name: "CSS Stylesheet Request",
        request_line: "GET /styles.css HTTP/1.1",
        description: "Request for a CSS stylesheet file",
        category: "valid_advanced",
        difficulty_level: "intermediate",
        expected_result: true,
        created_date: new Date().toISOString()
      },
      {
        id: 7,
        name: "JavaScript File Request",
        request_line: "GET /script.js HTTP/1.1",
        description: "Request for a JavaScript file",
        category: "valid_advanced",
        difficulty_level: "intermediate",
        expected_result: true,
        created_date: new Date().toISOString()
      },
      {
        id: 8,
        name: "Image File Request",
        request_line: "GET /logo.png HTTP/1.1",
        description: "Request for a PNG image file",
        category: "valid_advanced",
        difficulty_level: "intermediate",
        expected_result: true,
        created_date: new Date().toISOString()
      },
      {
        id: 9,
        name: "Font File Request",
        request_line: "GET /font.woff HTTP/1.1",
        description: "Request for a web font file",
        category: "valid_advanced",
        difficulty_level: "intermediate",
        expected_result: true,
        created_date: new Date().toISOString()
      },
      {
        id: 10,
        name: "API Endpoint Request",
        request_line: "GET /api.json HTTP/1.1",
        description: "Request for a JSON API endpoint",
        category: "valid_advanced",
        difficulty_level: "advanced",
        expected_result: true,
        created_date: new Date().toISOString()
      },
      {
        id: 11,
        name: "Data File Request",
        request_line: "GET /data.xml HTTP/1.1",
        description: "Request for an XML data file",
        category: "valid_advanced",
        difficulty_level: "advanced",
        expected_result: true,
        created_date: new Date().toISOString()
      },
      {
        id: 12,
        name: "Document Request",
        request_line: "GET /document.pdf HTTP/1.1",
        description: "Request for a PDF document",
        category: "valid_advanced",
        difficulty_level: "advanced",
        expected_result: true,
        created_date: new Date().toISOString()
      },

      // Invalid Method Errors
      {
        id: 13,
        name: "POST Method Error",
        request_line: "POST /index.html HTTP/1.1",
        description: "Invalid HTTP method - only GET is supported",
        category: "invalid_method",
        difficulty_level: "beginner",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 14,
        name: "PUT Method Error",
        request_line: "PUT /data.json HTTP/1.1",
        description: "PUT method not allowed in CFG rules",
        category: "invalid_method",
        difficulty_level: "beginner",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 15,
        name: "DELETE Method Error",
        request_line: "DELETE /item.html HTTP/1.1",
        description: "DELETE method not supported",
        category: "invalid_method",
        difficulty_level: "beginner",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 16,
        name: "PATCH Method Error",
        request_line: "PATCH /user.json HTTP/1.1",
        description: "PATCH method not allowed",
        category: "invalid_method",
        difficulty_level: "intermediate",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 17,
        name: "Lowercase Method Error",
        request_line: "get /index.html HTTP/1.1",
        description: "HTTP method must be uppercase",
        category: "invalid_method",
        difficulty_level: "beginner",
        expected_result: false,
        created_date: new Date().toISOString()
      },

      // Invalid Version Errors
      {
        id: 18,
        name: "HTTP/3.0 Version Error",
        request_line: "GET /index.html HTTP/3.0",
        description: "Unsupported HTTP version - HTTP/3.0 not allowed",
        category: "invalid_version",
        difficulty_level: "intermediate",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 19,
        name: "HTTP/0.9 Version Error",
        request_line: "GET /page.html HTTP/0.9",
        description: "Outdated HTTP version not supported",
        category: "invalid_version",
        difficulty_level: "intermediate",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 20,
        name: "Invalid Version Format",
        request_line: "GET /test.html HTTP/1.5",
        description: "Invalid HTTP version number",
        category: "invalid_version",
        difficulty_level: "intermediate",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 21,
        name: "Lowercase Version Error",
        request_line: "GET /file.txt http/1.1",
        description: "HTTP version must be uppercase",
        category: "invalid_version",
        difficulty_level: "beginner",
        expected_result: false,
        created_date: new Date().toISOString()
      },

      // Invalid Syntax Errors
      {
        id: 22,
        name: "Missing Space After Method",
        request_line: "GET/index.html HTTP/1.1",
        description: "Missing space after HTTP method",
        category: "invalid_syntax",
        difficulty_level: "beginner",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 23,
        name: "Missing Space Before Version",
        request_line: "GET /page.htmlHTTP/1.1",
        description: "Missing space before HTTP version",
        category: "invalid_syntax",
        difficulty_level: "beginner",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 24,
        name: "Extra Spaces Error",
        request_line: "GET  /index.html  HTTP/1.1",
        description: "Extra spaces between components not allowed",
        category: "invalid_syntax",
        difficulty_level: "intermediate",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 25,
        name: "Missing HTTP Version",
        request_line: "GET /index.html",
        description: "HTTP version is required",
        category: "invalid_syntax",
        difficulty_level: "beginner",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 26,
        name: "Missing Path",
        request_line: "GET HTTP/1.1",
        description: "Path component is required",
        category: "invalid_syntax",
        difficulty_level: "beginner",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 27,
        name: "Incomplete Request",
        request_line: "GET",
        description: "Incomplete HTTP request line",
        category: "invalid_syntax",
        difficulty_level: "beginner",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 28,
        name: "Invalid Path Format",
        request_line: "GET index.html HTTP/1.1",
        description: "Path must start with forward slash",
        category: "invalid_syntax",
        difficulty_level: "intermediate",
        expected_result: false,
        created_date: new Date().toISOString()
      },

      // Edge Cases
      {
        id: 29,
        name: "Empty Request Line",
        request_line: "",
        description: "Completely empty request line",
        category: "edge_cases",
        difficulty_level: "advanced",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 30,
        name: "Only Spaces",
        request_line: "   ",
        description: "Request line with only whitespace",
        category: "edge_cases",
        difficulty_level: "advanced",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 31,
        name: "Special Characters in Path",
        request_line: "GET /file@#$.html HTTP/1.1",
        description: "Path with special characters",
        category: "edge_cases",
        difficulty_level: "advanced",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 32,
        name: "Very Long Path",
        request_line: "GET /very/long/path/to/deeply/nested/file/structure/document.html HTTP/1.1",
        description: "Request with very long path structure",
        category: "edge_cases",
        difficulty_level: "advanced",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 33,
        name: "Mixed Case Method",
        request_line: "Get /index.html HTTP/1.1",
        description: "HTTP method with mixed case",
        category: "edge_cases",
        difficulty_level: "intermediate",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 34,
        name: "Tab Characters",
        request_line: "GET\t/index.html\tHTTP/1.1",
        description: "Request line with tab characters instead of spaces",
        category: "edge_cases",
        difficulty_level: "advanced",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 35,
        name: "Trailing Spaces",
        request_line: "GET /index.html HTTP/1.1 ",
        description: "Request line with trailing spaces",
        category: "edge_cases",
        difficulty_level: "intermediate",
        expected_result: false,
        created_date: new Date().toISOString()
      },
      {
        id: 36,
        name: "Leading Spaces",
        request_line: " GET /index.html HTTP/1.1",
        description: "Request line with leading spaces",
        category: "edge_cases",
        difficulty_level: "intermediate",
        expected_result: false,
        created_date: new Date().toISOString()
      }
    ];
  }
};

// Mock toast function
const toast = {
  success: (message: string) => {
    console.log('Success:', message);
    // You can implement actual toast notification here
  }
};

export const LibraryPage: React.FC = () => {
  const [templates, setTemplates] = useState<RequestTemplate[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [searchTerm, setSearchTerm] = useState('');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [difficultyFilter, setDifficultyFilter] = useState('all');

  useEffect(() => {
    loadTemplates();
  }, []);

  const loadTemplates = async () => {
    setIsLoading(true);
    try {
      const data = await RequestTemplate.list('-created_date');
      setTemplates(data);
    } catch (error) {
      console.error('Failed to load templates:', error);
    }
    setIsLoading(false);
  };

  const filteredTemplates = templates.filter(template => {
    const matchesSearch = template.name.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         template.request_line.toLowerCase().includes(searchTerm.toLowerCase()) ||
                         template.description.toLowerCase().includes(searchTerm.toLowerCase());
    
    const matchesCategory = categoryFilter === 'all' || template.category === categoryFilter;
    const matchesDifficulty = difficultyFilter === 'all' || template.difficulty_level === difficultyFilter;
    
    return matchesSearch && matchesCategory && matchesDifficulty;
  });

  const copyToClipboard = (text: string, templateName: string) => {
    navigator.clipboard.writeText(text);
    toast.success(`Copied "${templateName}" to clipboard`);
  };

  const getCategoryColor = (category: string) => {
    const colors: Record<string, string> = {
      valid_basic: 'bg-emerald-100 text-emerald-800 border-emerald-200',
      valid_advanced: 'bg-blue-100 text-blue-800 border-blue-200',
      invalid_syntax: 'bg-red-100 text-red-800 border-red-200',
      invalid_method: 'bg-orange-100 text-orange-800 border-orange-200',
      invalid_version: 'bg-purple-100 text-purple-800 border-purple-200',
      edge_cases: 'bg-gray-100 text-gray-800 border-gray-200'
    };
    return colors[category] || 'bg-gray-100 text-gray-800 border-gray-200';
  };

  const getDifficultyColor = (level: string) => {
    const colors: Record<string, string> = {
      beginner: 'bg-green-50 text-green-700',
      intermediate: 'bg-yellow-50 text-yellow-700',
      advanced: 'bg-red-50 text-red-700'
    };
    return colors[level] || 'bg-gray-50 text-gray-700';
  };

  return (
    <div className="min-h-screen px-6 py-8 lg:px-8">
      <div className="mx-auto max-w-7xl space-y-8">
        <div className="text-center space-y-4 opacity-0 animate-fade-in">
          <h1 className="text-4xl lg:text-5xl font-bold bg-gradient-to-r from-blue-600 via-purple-600 to-blue-800 bg-clip-text text-transparent">
            Request Library
          </h1>
          <p className="text-xl text-slate-600 max-w-2xl mx-auto leading-relaxed">
            Curated collection of HTTP request examples from basic to advanced patterns
          </p>
        </div>

        {/* Filters */}
        <div className="opacity-0 animate-fade-in-delayed flex flex-col md:flex-row gap-4 items-center justify-between">
          <div className="relative flex-1 max-w-md">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 w-4 h-4 text-slate-400" />
            <input
              placeholder="Search templates..."
              value={searchTerm}
              onChange={(e) => setSearchTerm(e.target.value)}
              className="w-full pl-10 pr-4 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500 focus:border-blue-500"
            />
          </div>
          
          <div className="flex gap-4 items-center">
            <div className="flex items-center gap-2">
              <Filter className="w-4 h-4 text-slate-500" />
              <select 
                value={categoryFilter} 
                onChange={(e) => setCategoryFilter(e.target.value)}
                className="w-36 px-3 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
              >
                <option value="all">All Categories</option>
                <option value="valid_basic">Valid Basic</option>
                <option value="valid_advanced">Valid Advanced</option>
                <option value="invalid_syntax">Invalid Syntax</option>
                <option value="invalid_method">Invalid Method</option>
                <option value="invalid_version">Invalid Version</option>
                <option value="edge_cases">Edge Cases</option>
              </select>
            </div>

            <select 
              value={difficultyFilter} 
              onChange={(e) => setDifficultyFilter(e.target.value)}
              className="w-32 px-3 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="all">All Levels</option>
              <option value="beginner">Beginner</option>
              <option value="intermediate">Intermediate</option>
              <option value="advanced">Advanced</option>
            </select>
          </div>
        </div>

        {/* Templates Grid */}
        <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
          {filteredTemplates.map((template) => (
            <div
              key={template.id}
              className="bg-white/70 backdrop-blur-sm border border-slate-200 hover:border-blue-200 transition-all duration-300 h-full group rounded-xl overflow-hidden hover:transform hover:-translate-y-1"
            >
              <div className="space-y-4 px-6 pt-6">
                <div className="flex items-start justify-between">
                  <div className="space-y-2">
                    <h3 className="text-lg font-bold group-hover:text-blue-700 transition-colors">
                      {template.name}
                    </h3>
                    <div className="flex flex-wrap gap-2">
                      <span className={`${getCategoryColor(template.category)} px-2 py-1 rounded-md text-xs font-medium border`}>
                        {template.category.replace(/_/g, ' ')}
                      </span>
                      <span className={`${getDifficultyColor(template.difficulty_level)} px-2 py-1 rounded-md text-xs font-medium border`}>
                        {template.difficulty_level}
                      </span>
                    </div>
                  </div>
                  <div className="flex items-center gap-1">
                    {template.expected_result ? (
                      <CheckCircle className="w-5 h-5 text-emerald-500" />
                    ) : (
                      <XCircle className="w-5 h-5 text-red-500" />
                    )}
                  </div>
                </div>
              </div>
              
              <div className="px-6 pb-6 space-y-4">
                <div className="space-y-2">
                  <div className="text-sm text-slate-600 font-medium">Request Line:</div>
                  <code className="block p-3 bg-slate-900 text-slate-100 rounded-lg text-sm font-mono break-all">
                    {template.request_line}
                  </code>
                </div>

                <p className="text-sm text-slate-600 leading-relaxed">
                  {template.description}
                </p>

                <button
                  onClick={() => copyToClipboard(template.request_line, template.name)}
                  className="w-full bg-gradient-to-r from-blue-500 to-blue-600 hover:from-blue-600 hover:to-blue-700 text-white transition-all duration-300 px-4 py-2 rounded-lg flex items-center justify-center"
                >
                  <Copy className="w-4 h-4 mr-2" />
                  Copy Request
                </button>
              </div>
            </div>
          ))}
        </div>

        {/* Empty State */}
        {filteredTemplates.length === 0 && !isLoading && (
          <div className="text-center py-16">
            <BookOpen className="w-16 h-16 text-slate-300 mx-auto mb-4" />
            <h3 className="text-xl font-semibold text-slate-600 mb-2">No templates found</h3>
            <p className="text-slate-500">Try adjusting your search criteria or filters</p>
          </div>
        )}

        {/* Loading State */}
        {isLoading && (
          <div className="grid md:grid-cols-2 lg:grid-cols-3 gap-6">
            {[...Array(6)].map((_, i) => (
              <div key={i} className="bg-white/70 backdrop-blur-sm border border-slate-200 h-64 animate-pulse rounded-xl overflow-hidden">
                <div className="px-6 pt-6">
                  <div className="h-4 bg-slate-200 rounded w-3/4 mb-2"></div>
                  <div className="flex gap-2">
                    <div className="h-5 bg-slate-200 rounded-full w-16"></div>
                    <div className="h-5 bg-slate-200 rounded-full w-20"></div>
                  </div>
                </div>
                <div className="px-6 pb-6 pt-4">
                  <div className="space-y-2">
                    <div className="h-3 bg-slate-200 rounded w-1/4"></div>
                    <div className="h-8 bg-slate-200 rounded"></div>
                    <div className="h-3 bg-slate-200 rounded w-full"></div>
                    <div className="h-3 bg-slate-200 rounded w-3/4"></div>
                  </div>
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
};