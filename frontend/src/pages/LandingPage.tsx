// Landing Page component - Main homepage with hero section and features

import React, { useEffect, useState } from 'react';
import { Link } from 'react-router-dom';
import { motion } from 'framer-motion';
import { 
  CheckCircle, 
  BarChart3, 
  BookOpen, 
  Code2, 
  Play, 
  ArrowRight,
  Zap,
  Shield,
  Eye,
  Brain,
  TrendingUp,
  Users,
  Star,
  Sparkles,
  AlertTriangle
} from 'lucide-react';
import { useAPI } from '../contexts/APIContext';
import { useValidation } from '../contexts/ValidationContext';
import { useNotifications } from '../contexts/NotificationContext';

interface FeatureProps {
  icon: React.ElementType;
  title: string;
  description: string;
  color: string;
}

const Feature: React.FC<FeatureProps> = ({ icon: Icon, title, description, color }) => (
  <motion.div 
    initial={{ opacity: 0, y: 20 }}
    whileInView={{ opacity: 1, y: 0 }}
    transition={{ duration: 0.6 }}
    whileHover={{ y: -8, scale: 1.02 }}
    className="group p-6 glass-card rounded-xl shadow-lg hover:shadow-xl transition-all duration-300 border border-white/20"
  >
    <motion.div 
      whileHover={{ scale: 1.1, rotate: 5 }}
      className={`inline-flex p-3 rounded-lg bg-gradient-to-br ${color} mb-4 transition-transform`}
    >
      <Icon className="w-6 h-6 text-white" />
    </motion.div>
    <h3 className="text-xl font-semibold text-gray-900 mb-3">{title}</h3>
    <p className="text-gray-600 leading-relaxed">{description}</p>
    <motion.div 
      className="mt-4 text-blue-600 font-medium opacity-0 group-hover:opacity-100 transition-opacity"
      initial={{ x: -10 }}
      whileHover={{ x: 0 }}
    >
      Learn more →
    </motion.div>
  </motion.div>
);

interface StatProps {
  label: string;
  value: string;
  icon: React.ElementType;
}

const Stat: React.FC<StatProps> = ({ label, value, icon: Icon }) => (
  <motion.div 
    initial={{ opacity: 0, scale: 0.9 }}
    whileInView={{ opacity: 1, scale: 1 }}
    transition={{ duration: 0.5 }}
    whileHover={{ scale: 1.05 }}
    className="text-center p-6 glass-card rounded-xl border border-white/20"
  >
    <motion.div
      initial={{ scale: 0 }}
      whileInView={{ scale: 1 }}
      transition={{ delay: 0.2, type: "spring", stiffness: 200 }}
    >
      <Icon className="w-8 h-8 text-blue-600 mx-auto mb-3" />
    </motion.div>
    <motion.div 
      className="text-3xl font-bold text-gray-900 mb-1"
      initial={{ opacity: 0 }}
      whileInView={{ opacity: 1 }}
      transition={{ delay: 0.3 }}
    >
      {value}
    </motion.div>
    <div className="text-gray-600 font-medium">{label}</div>
  </motion.div>
);

export const LandingPage: React.FC = () => {
  const { getStatsSummary } = useAPI();
  const { stats: validationStats } = useValidation();
  const { showError } = useNotifications();
  const [stats, setStats] = useState({
    totalRequests: '0',
    successRate: '0%',
    totalSessions: '0'
  });

  useEffect(() => {
    const loadStats = async () => {
      try {
        // Always use real-time validation stats from ValidationContext
        setStats({
          totalRequests: validationStats.total.toLocaleString(),
          successRate: `${validationStats.successRate}%`,
          totalSessions: '1' // Current session
        });
      } catch (error) {
        // Silently handle error for better UX
        console.warn('Failed to load stats:', error);
      }
    };

    loadStats();
  }, [validationStats]);

  const features = [
    {
      icon: Zap,
      title: "Real-time Validation",
      description: "Instantly check if your HTTP GET requests follow proper Context-Free Grammar rules with immediate feedback.",
      color: "from-blue-500 to-blue-600"
    },
    {
      icon: Eye,
      title: "Parse Tree Visualization",
      description: "See how your HTTP requests are broken down into grammar components with clear, visual parse trees.",
      color: "from-green-500 to-green-600"
    },
    {
      icon: BarChart3,
      title: "Simple Analytics",
      description: "Track your validation attempts and see patterns in your requests to improve your understanding.",
      color: "from-purple-500 to-purple-600"
    },
    {
      icon: BookOpen,
      title: "Example Library",
      description: "Browse through example HTTP requests to learn what works and what doesn't in CFG validation.",
      color: "from-orange-500 to-orange-600"
    },
    {
      icon: AlertTriangle,
      title: "Error Explanations",
      description: "Get clear explanations when requests fail validation, helping you understand CFG rules better.",
      color: "from-red-500 to-red-600"
    },
    {
      icon: Brain,
      title: "AI Helper",
      description: "Ask questions about CFG rules and HTTP syntax. Get explanations tailored to your learning needs.",
      color: "from-indigo-500 to-indigo-600"
    }
  ];

  return (
    <div className="min-h-screen">
      {/* Hero Section */}
      <section className="relative overflow-hidden">
        {/* Enhanced Background */}
        <div className="absolute inset-0 gradient-bg-blue opacity-10">
          <div className="absolute inset-0 bg-grid-pattern opacity-5"></div>
          <div className="absolute top-20 left-10 w-72 h-72 bg-gradient-to-r from-blue-400 to-purple-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse-slow"></div>
          <div className="absolute top-40 right-10 w-96 h-96 bg-gradient-to-r from-purple-400 to-pink-500 rounded-full mix-blend-multiply filter blur-xl opacity-20 animate-pulse-slow" style={{animationDelay: '2s'}}></div>
        </div>
        
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 pt-20 pb-16">
          <div className="text-center">
            {/* More Human Badge */}
            <motion.div 
              initial={{ opacity: 0, y: -20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.6 }}
              className="inline-flex items-center px-5 py-2 bg-white/90 rounded-full text-blue-700 text-sm font-medium mb-6 border border-blue-100 shadow-sm backdrop-blur-sm"
            >
              <span className="w-2 h-2 bg-green-500 rounded-full mr-2 animate-pulse"></span>
              Live CFG Validation Tool
            </motion.div>
            
            {/* More Natural Main Heading */}
            <motion.h1 
              initial={{ opacity: 0, y: 30 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.2 }}
              className="text-4xl md:text-6xl font-bold text-gray-900 mb-6 leading-tight"
            >
              Validate HTTP Requests
              <motion.span 
                className="block text-blue-600 mt-2"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                transition={{ delay: 0.5 }}
              >
                with Context-Free Grammar
              </motion.span>
            </motion.h1>
            
            {/* More Conversational Description */}
            <motion.p 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.4 }}
              className="text-lg md:text-xl text-gray-600 mb-12 max-w-3xl mx-auto leading-relaxed"
            >
              Ever wondered if your HTTP requests follow proper grammar rules? 
              Our tool uses <strong>Context-Free Grammar</strong> to validate GET requests in real-time, 
              helping developers and students understand protocol syntax better.
            </motion.p>
            
            {/* More Natural CTA Buttons */}
            <motion.div 
              initial={{ opacity: 0, y: 20 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.8, delay: 0.6 }}
              className="flex flex-col sm:flex-row gap-4 justify-center items-center mb-16"
            >
              <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                <Link
                  to="/validator"
                  className="group inline-flex items-center px-7 py-3 bg-blue-600 hover:bg-blue-700 text-white font-medium rounded-lg shadow-md hover:shadow-lg transition-all duration-200"
                >
                  <Play className="w-4 h-4 mr-2" />
                  Try the Validator
                  <ArrowRight className="w-4 h-4 ml-2 group-hover:translate-x-0.5 transition-transform" />
                </Link>
              </motion.div>
              
              <motion.div whileHover={{ scale: 1.02 }} whileTap={{ scale: 0.98 }}>
                <Link
                  to="/grammar"
                  className="group inline-flex items-center px-7 py-3 bg-white text-gray-700 font-medium rounded-lg shadow-md hover:shadow-lg border border-gray-200 hover:border-gray-300 transition-all duration-200"
                >
                  <BookOpen className="w-4 h-4 mr-2" />
                  Learn Grammar Rules
                </Link>
              </motion.div>
            </motion.div>
            
            {/* Enhanced Quick Stats */}
            <motion.div 
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
              transition={{ duration: 0.8, delay: 0.8 }}
              className="grid grid-cols-1 sm:grid-cols-3 gap-4 max-w-2xl mx-auto"
            >
              <Stat label="Requests Validated" value={stats.totalRequests} icon={CheckCircle} />
              <Stat label="Success Rate" value={stats.successRate} icon={TrendingUp} />
              <Stat label="Active Sessions" value={stats.totalSessions} icon={Users} />
            </motion.div>
          </div>
        </div>
      </section>

      {/* Enhanced Features Section */}
      <section className="py-20 relative overflow-hidden">
        <div className="absolute inset-0 gradient-overlay"></div>
        <div className="relative max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <motion.div 
            initial={{ opacity: 0, y: 30 }}
            whileInView={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.8 }}
            className="text-center mb-16"
          >
            <motion.h2 
              className="text-4xl md:text-5xl font-bold text-gray-900 mb-6"
              initial={{ opacity: 0 }}
              whileInView={{ opacity: 1 }}
              transition={{ duration: 0.6 }}
            >
              Powerful Features for
              <motion.span 
                className="block text-shimmer"
                initial={{ opacity: 0 }}
                whileInView={{ opacity: 1 }}
                transition={{ delay: 0.3 }}
              >
                CFG Learning
              </motion.span>
            </motion.h2>
            <motion.p 
              className="text-xl text-gray-600 max-w-3xl mx-auto"
              initial={{ opacity: 0, y: 20 }}
              whileInView={{ opacity: 1, y: 0 }}
              transition={{ delay: 0.4 }}
            >
              Everything you need to understand Context-Free Grammar and HTTP request validation in one <span className="text-blue-600 font-semibold">comprehensive platform</span>.
            </motion.p>
          </motion.div>
          
          <motion.div 
            className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-8"
            initial={{ opacity: 0 }}
            whileInView={{ opacity: 1 }}
            transition={{ duration: 0.8, staggerChildren: 0.1 }}
          >
            {features.map((feature, index) => (
              <motion.div
                key={index}
                initial={{ opacity: 0, y: 30 }}
                whileInView={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.6, delay: index * 0.1 }}
              >
                <Feature {...feature} />
              </motion.div>
            ))}
          </motion.div>
        </div>
      </section>

      {/* Getting Started Section */}
      <section className="py-20 bg-gradient-to-br from-blue-50 to-indigo-100">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8">
          <div className="text-center mb-16">
            <h2 className="text-4xl md:text-5xl font-bold text-gray-900 mb-4">
              Get Started in
              <span className="block text-transparent bg-clip-text bg-gradient-to-r from-blue-600 to-indigo-600">
                Three Easy Steps
              </span>
            </h2>
            <p className="text-xl text-gray-600 max-w-2xl mx-auto">
              Begin your journey with Context-Free Grammar and HTTP validation.
            </p>
          </div>
          
          <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
            <div className="text-center group">
              <div className="bg-white p-8 rounded-2xl shadow-lg group-hover:shadow-xl transition-shadow">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-blue-500 to-indigo-500 text-white rounded-xl mb-6 text-2xl font-bold">
                  1
                </div>
                <h3 className="text-2xl font-semibold text-gray-900 mb-4">Learn the Grammar</h3>
                <p className="text-gray-600 mb-6">
                  Explore our interactive grammar rules and understand how Context-Free Grammar defines HTTP request structure.
                </p>
                <Link
                  to="/grammar"
                  className="inline-flex items-center text-blue-600 hover:text-blue-700 font-medium"
                >
                  View Grammar Rules
                  <ArrowRight className="w-4 h-4 ml-1" />
                </Link>
              </div>
            </div>
            
            <div className="text-center group">
              <div className="bg-white p-8 rounded-2xl shadow-lg group-hover:shadow-xl transition-shadow">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-green-500 to-emerald-500 text-white rounded-xl mb-6 text-2xl font-bold">
                  2
                </div>
                <h3 className="text-2xl font-semibold text-gray-900 mb-4">Try Examples</h3>
                <p className="text-gray-600 mb-6">
                  Start with our curated library of example requests to see how validation works in practice.
                </p>
                <Link
                  to="/library"
                  className="inline-flex items-center text-green-600 hover:text-green-700 font-medium"
                >
                  Browse Examples
                  <ArrowRight className="w-4 h-4 ml-1" />
                </Link>
              </div>
            </div>
            
            <div className="text-center group">
              <div className="bg-white p-8 rounded-2xl shadow-lg group-hover:shadow-xl transition-shadow">
                <div className="inline-flex items-center justify-center w-16 h-16 bg-gradient-to-br from-purple-500 to-violet-500 text-white rounded-xl mb-6 text-2xl font-bold">
                  3
                </div>
                <h3 className="text-2xl font-semibold text-gray-900 mb-4">Validate & Learn</h3>
                <p className="text-gray-600 mb-6">
                  Use our validator to test your own HTTP requests and learn from detailed feedback and visualizations.
                </p>
                <Link
                  to="/validator"
                  className="inline-flex items-center text-purple-600 hover:text-purple-700 font-medium"
                >
                  Start Validating
                  <ArrowRight className="w-4 h-4 ml-1" />
                </Link>
              </div>
            </div>
          </div>
        </div>
      </section>

      {/* CTA Section */}
      <section className="py-20 bg-gradient-to-r from-blue-600 to-indigo-600 text-white">
        <div className="max-w-4xl mx-auto text-center px-4 sm:px-6 lg:px-8">
          <h2 className="text-4xl md:text-5xl font-bold mb-6">
            Ready to Master CFG?
          </h2>
          <p className="text-xl mb-12 opacity-90">
            Join thousands of students and developers learning Context-Free Grammar through hands-on HTTP request validation.
          </p>
          <div className="flex flex-col sm:flex-row gap-4 justify-center">
            <Link
              to="/validator"
              className="group inline-flex items-center px-8 py-4 bg-white text-blue-600 font-semibold rounded-xl shadow-lg hover:shadow-xl transform hover:-translate-y-1 transition-all duration-300"
            >
              <Play className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform" />
              Start Learning Now
              <ArrowRight className="w-5 h-5 ml-2 group-hover:translate-x-1 transition-transform" />
            </Link>
            
            <Link
              to="/dashboard"
              className="group inline-flex items-center px-8 py-4 bg-blue-700 text-white font-semibold rounded-xl shadow-lg hover:shadow-xl hover:bg-blue-800 transform hover:-translate-y-1 transition-all duration-300"
            >
              <BarChart3 className="w-5 h-5 mr-2 group-hover:scale-110 transition-transform" />
              View Analytics
            </Link>
          </div>
        </div>
      </section>
    </div>
  );
};