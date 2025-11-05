import React, { useState, useEffect, useCallback } from "react";
import { motion } from "framer-motion";
import { Calendar, Filter, RefreshCw, BarChart, TrendingUp, Users } from "lucide-react";
import { format, subDays, startOfDay } from "date-fns";
import StatsCards from "../components/analytics/StatsCards";
import ValidationChart from "../components/analytics/ValidationChart";
import { useValidation } from '../contexts/ValidationContext';

interface RequestLog {
  id: number;
  request_line: string;
  is_valid: boolean;
  error_type?: string;
  error_message?: string;
  parse_tree?: string;
  validation_time_ms?: number;
  user_session: string;
  created_date: string;
}

export const AnalyticsPage: React.FC = () => {
  const [isLoading, setIsLoading] = useState(false);
  const [timeRange, setTimeRange] = useState('7d');
  const { validationLogs, stats, getFilteredLogs, addSampleData, clearLogs } = useValidation();

  const [refreshKey, setRefreshKey] = useState(0);

  const refresh = () => {
    setRefreshKey(prev => prev + 1);
  };

  const getFilteredData = () => {
    const days = parseInt(timeRange.replace('d', ''));
    return getFilteredLogs(days);
  };

  const getTimelineData = () => {
    const filteredLogs = getFilteredData();
    const days = timeRange === '7d' ? 7 : timeRange === '30d' ? 30 : 90;
    const timeline: Record<string, any> = {};
    
    // Initialize timeline
    for (let i = 0; i < days; i++) {
      const date = format(subDays(new Date(), i), 'MMM dd');
      timeline[date] = { date, valid: 0, invalid: 0 };
    }
    
    // Fill with data
    filteredLogs.forEach(log => {
      const date = format(new Date(log.created_date), 'MMM dd');
      if (timeline[date]) {
        if (log.is_valid) {
          timeline[date].valid++;
        } else {
          timeline[date].invalid++;
        }
      }
    });
    
    return Object.values(timeline).reverse();
  };

  const getValidationDistribution = () => {
    const filteredLogs = getFilteredData();
    const validCount = filteredLogs.filter(log => log.is_valid).length;
    const invalidCount = filteredLogs.filter(log => !log.is_valid).length;
    
    return [
      { name: 'Valid Requests', value: validCount },
      { name: 'Invalid Requests', value: invalidCount }
    ].filter(item => item.value > 0); // Only show non-zero values
  };

  const getErrorDistribution = () => {
    const filteredLogs = getFilteredData().filter(log => !log.is_valid);
    const errorCounts: Record<string, number> = {};
    
    filteredLogs.forEach(log => {
      const errorType = (log.error_type || 'unknown').replace('_', ' ');
      errorCounts[errorType] = (errorCounts[errorType] || 0) + 1;
    });
    
    return Object.entries(errorCounts).map(([name, value]) => ({
      name: name.charAt(0).toUpperCase() + name.slice(1),
      value
    }));
  };

  const getRecentValidations = () => {
    return getFilteredData().slice(0, 10);
  };

  return (
    <div className="min-h-screen px-6 py-8 lg:px-8 relative overflow-hidden">
      {/* Background Elements */}
      <div className="absolute inset-0 gradient-overlay opacity-20"></div>
      <div className="absolute top-20 right-10 w-96 h-96 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-10 animate-pulse-slow"></div>
      
      <div className="relative mx-auto max-w-7xl space-y-8">
        <motion.div 
          initial={{ opacity: 0, y: 30 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8 }}
          className="flex flex-col md:flex-row justify-between items-start md:items-center gap-4"
        >
          <motion.div
            initial={{ opacity: 0, x: -30 }}
            animate={{ opacity: 1, x: 0 }}
            transition={{ delay: 0.2 }}
          >
            <div className="flex items-center gap-3 mb-2">
              <motion.div
                whileHover={{ scale: 1.1, rotate: 5 }}
                className="w-10 h-10 bg-gradient-to-br from-blue-500 to-purple-600 rounded-lg flex items-center justify-center"
              >
                <BarChart className="w-5 h-5 text-white" />
              </motion.div>
              <h1 className="text-4xl lg:text-5xl font-bold text-shimmer">
                Analytics Dashboard
              </h1>
            </div>
            <p className="text-xl text-slate-600">
              Comprehensive <span className="text-blue-600 font-semibold">validation insights</span> and <span className="text-purple-600 font-semibold">performance metrics</span>
            </p>
          </motion.div>

          <div className="flex items-center gap-4">
            {validationLogs.length === 0 && (
              <button
                onClick={addSampleData}
                className="flex items-center gap-2 px-3 py-2 text-sm bg-green-600 text-white rounded-lg hover:bg-green-700 transition-colors"
              >
                Add Sample Data
              </button>
            )}
            {validationLogs.length > 0 && (
              <button
                onClick={clearLogs}
                className="flex items-center gap-2 px-3 py-2 text-sm bg-red-600 text-white rounded-lg hover:bg-red-700 transition-colors"
              >
                Clear Data
              </button>
            )}
            <button
              onClick={refresh}
              className="flex items-center gap-2 px-3 py-2 text-sm bg-blue-600 text-white rounded-lg hover:bg-blue-700 transition-colors"
            >
              <RefreshCw className="w-4 h-4" />
              Refresh
            </button>
            <div className="flex items-center gap-2 text-sm text-slate-600">
              <Calendar className="w-4 h-4" />
              Time Range:
            </div>
            <select 
              value={timeRange} 
              onChange={(e) => setTimeRange(e.target.value)}
              className="w-32 px-3 py-2 border border-slate-200 rounded-lg focus:outline-none focus:ring-2 focus:ring-blue-500"
            >
              <option value="7d">7 Days</option>
              <option value="30d">30 Days</option>
              <option value="90d">90 Days</option>
            </select>
          </div>
        </motion.div>

        <div className="opacity-0 animate-fade-in-delayed space-y-8" key={refreshKey}>
          <div>
            <StatsCards stats={stats} />
          </div>

          <div className="grid lg:grid-cols-2 gap-8">
            <div>
              <ValidationChart data={getTimelineData()} type="timeline" />
            </div>
            <div>
              <ValidationChart data={getValidationDistribution()} type="validation" />
            </div>
          </div>

          <div>
            <div className="bg-white/70 backdrop-blur-sm border border-slate-200 rounded-xl overflow-hidden">
              <div className="px-6 py-4 border-b border-slate-200">
                <div className="flex items-center justify-between">
                  <div className="flex items-center gap-2 text-lg font-bold">
                    📋 Recent Validations
                  </div>
                  <div className="text-sm text-slate-500">
                    Total: {validationLogs.length} validations
                  </div>
                </div>
              </div>
              <div className="p-6">
                {getRecentValidations().length === 0 ? (
                  <div className="text-center py-12 text-slate-500">
                    <div className="mb-4">
                      <svg className="mx-auto h-16 w-16 text-slate-300" fill="currentColor" viewBox="0 0 20 20">
                        <path fillRule="evenodd" d="M3 4a1 1 0 011-1h12a1 1 0 011 1v2a1 1 0 01-1 1H4a1 1 0 01-1-1V4zm0 4a1 1 0 011-1h12a1 1 0 011 1v6a1 1 0 01-1 1H4a1 1 0 01-1-1V8z" clipRule="evenodd" />
                      </svg>
                    </div>
                    <p className="text-lg font-medium mb-2">No validation data available</p>
                    <p className="text-sm">Start validating HTTP requests to see analytics data here</p>
                  </div>
                ) : (
                  <div className="space-y-4">
                    {getRecentValidations().map((log, index) => (
                      <div key={log.id} className="flex items-center justify-between p-4 bg-white/50 rounded-lg border border-slate-100">
                        <div className="space-y-1">
                          <code className="text-sm bg-slate-100 px-2 py-1 rounded font-mono">
                            {log.request_line}
                          </code>
                          <div className="flex items-center gap-2">
                            <span className={`text-xs px-2 py-1 rounded ${
                              log.is_valid 
                                ? 'bg-emerald-100 text-emerald-800' 
                                : 'bg-red-100 text-red-800'
                            }`}>
                              {log.is_valid ? "Valid" : "Invalid"}
                            </span>
                            {!log.is_valid && (
                              <span className="text-xs text-slate-500">
                                {log.error_type?.replace('_', ' ')}
                              </span>
                            )}
                          </div>
                        </div>
                        <div className="text-right text-sm text-slate-500">
                          <div>{log.validation_time_ms}ms</div>
                          <div>{format(new Date(log.created_date), 'MMM dd, HH:mm')}</div>
                        </div>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
};