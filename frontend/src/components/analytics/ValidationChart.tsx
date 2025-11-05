import React from 'react';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';
import { motion } from 'framer-motion';

interface ValidationChartProps {
  data: any[];
  type?: 'timeline' | 'errors' | 'validation';
}

export default function ValidationChart({ data, type = 'timeline' }: ValidationChartProps) {
  const colors = {
    valid: '#10b981',
    invalid: '#ef4444',
    total: '#3b82f6'
  };

  // Error distribution should use red-based colors since all entries are errors
  const pieColors = ['#ef4444', '#dc2626', '#b91c1c', '#991b1b', '#7f1d1d'];
  
  // Validation distribution uses appropriate colors: green for valid, red for invalid
  const validationColors = ['#10b981', '#ef4444'];

  // Enhanced gradient definitions for 3D effect
  const gradients = {
    valid: 'url(#validGradient)',
    invalid: 'url(#invalidGradient)',
    validPie: 'url(#validPieGradient)',
    invalidPie: 'url(#invalidPieGradient)'
  };

  if (type === 'timeline') {
    return (
      <motion.div 
        initial={{ opacity: 0, scale: 0.95, rotateX: 10 }}
        animate={{ opacity: 1, scale: 1, rotateX: 0 }}
        transition={{ duration: 0.6, ease: "easeOut" }}
        className="bg-gradient-to-br from-white via-blue-50/20 to-white border border-slate-200/80 rounded-2xl overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-1"
        style={{ 
          background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(219,234,254,0.3) 50%, rgba(255,255,255,0.95) 100%)',
          boxShadow: '0 20px 40px -12px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255,255,255,0.8) inset'
        }}
      >
        <div className="px-6 py-4 border-b border-slate-200/50 bg-gradient-to-r from-blue-500/5 to-purple-500/5">
          <div className="flex items-center gap-2 text-lg font-bold text-blue-700">
            📈 Validation Timeline
          </div>
        </div>
        <div className="p-6">
          <ResponsiveContainer width="100%" height={300}>
            <AreaChart data={data}>
              <defs>
                <linearGradient id="validGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#10b981" stopOpacity={0.6}/>
                  <stop offset="50%" stopColor="#10b981" stopOpacity={0.3}/>
                  <stop offset="100%" stopColor="#10b981" stopOpacity={0.1}/>
                </linearGradient>
                <linearGradient id="invalidGradient" x1="0" y1="0" x2="0" y2="1">
                  <stop offset="0%" stopColor="#ef4444" stopOpacity={0.6}/>
                  <stop offset="50%" stopColor="#ef4444" stopOpacity={0.3}/>
                  <stop offset="100%" stopColor="#ef4444" stopOpacity={0.1}/>
                </linearGradient>
                <filter id="glow" x="-50%" y="-50%" width="200%" height="200%">
                  <feGaussianBlur stdDeviation="1.5" result="coloredBlur"/>
                  <feMerge> 
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/> 
                  </feMerge>
                </filter>
              </defs>
              <CartesianGrid 
                strokeDasharray="3 3" 
                stroke="#e2e8f0" 
                strokeOpacity={0.6}
                strokeWidth={1}
              />
              <XAxis 
                dataKey="date" 
                stroke="#64748b"
                fontSize={12}
                fontWeight={500}
                tick={{ fill: '#64748b' }}
              />
              <YAxis 
                stroke="#64748b" 
                fontSize={12}
                fontWeight={500}
                tick={{ fill: '#64748b' }}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.98)',
                  border: '1px solid rgba(226, 232, 240, 0.5)',
                  borderRadius: '8px',
                  boxShadow: '0 10px 15px -3px rgba(0, 0, 0, 0.1)',
                  fontSize: '14px',
                  fontWeight: '500'
                }}
                labelStyle={{ color: '#1e293b', fontWeight: '600' }}
              />
              <Area
                type="monotone"
                dataKey="valid"
                stackId="1"
                stroke="#10b981"
                strokeWidth={2}
                fill={gradients.valid}
              />
              <Area
                type="monotone"
                dataKey="invalid"
                stackId="1"
                stroke="#ef4444"
                strokeWidth={2}
                fill={gradients.invalid}
              />
            </AreaChart>
          </ResponsiveContainer>
        </div>
      </motion.div>
    );
  }

  if (type === 'validation') {
    return (
      <motion.div 
        initial={{ opacity: 0, scale: 0.95, rotateY: -10 }}
        animate={{ opacity: 1, scale: 1, rotateY: 0 }}
        transition={{ duration: 0.6, ease: "easeOut", delay: 0.2 }}
        className="bg-gradient-to-br from-white via-emerald-50/20 to-white border border-slate-200/80 rounded-2xl overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-1"
        style={{ 
          background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(209,250,229,0.3) 50%, rgba(255,255,255,0.95) 100%)',
          boxShadow: '0 20px 40px -12px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255,255,255,0.8) inset'
        }}
      >
        <div className="px-6 py-4 border-b border-slate-200/50 bg-gradient-to-r from-emerald-500/5 to-green-500/5">
          <div className="flex items-center gap-2 text-lg font-bold text-emerald-700">
            🎯 Validation Distribution
          </div>
        </div>
        <div className="p-6 relative">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <defs>
                <radialGradient id="validPieGradient" cx="50%" cy="50%">
                  <stop offset="0%" stopColor="#16a34a" stopOpacity={0.9}/>
                  <stop offset="100%" stopColor="#10b981" stopOpacity={0.8}/>
                </radialGradient>
                <radialGradient id="invalidPieGradient" cx="50%" cy="50%">
                  <stop offset="0%" stopColor="#dc2626" stopOpacity={0.9}/>
                  <stop offset="100%" stopColor="#ef4444" stopOpacity={0.8}/>
                </radialGradient>
                <filter id="pieGlow" x="-50%" y="-50%" width="200%" height="200%">
                  <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                  <feMerge> 
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/> 
                  </feMerge>
                </filter>
                <filter id="pieShadow" x="-50%" y="-50%" width="200%" height="200%">
                  <feDropShadow dx="1" dy="2" stdDeviation="2" floodOpacity="0.2"/>
                </filter>
              </defs>
              <Pie
                data={data}
                cx="50%"
                cy="45%"
                labelLine={false}
                label={({ name, percent }: any) => `${name}\n${((percent || 0) * 100).toFixed(1)}%`}
                outerRadius={90}
                innerRadius={25}
                fill="#8884d8"
                dataKey="value"
                stroke="rgba(255,255,255,0.6)"
                strokeWidth={1}
              >
                {data.map((entry, index) => {
                  const isValid = entry.name.toLowerCase().includes('valid') && !entry.name.toLowerCase().includes('invalid');
                  const fillColor = isValid ? gradients.validPie : gradients.invalidPie;
                  return (
                    <Cell 
                      key={`cell-${index}`} 
                      fill={fillColor}
                    />
                  );
                })}
              </Pie>
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.98)',
                  border: '1px solid rgba(226, 232, 240, 0.5)',
                  borderRadius: '12px',
                  boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
                  backdropFilter: 'blur(10px)',
                  fontSize: '14px',
                  fontWeight: '500'
                }}
                labelStyle={{ color: '#1e293b', fontWeight: '600' }}
              />
            </PieChart>
          </ResponsiveContainer>
          
          {/* Subtle background elements */}
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-32 h-32 bg-gradient-radial from-emerald-100/10 via-transparent to-transparent rounded-full"></div>
          </div>
        </div>
      </motion.div>
    );
  }

  if (type === 'errors') {
    return (
      <motion.div 
        initial={{ opacity: 0, scale: 0.95, rotateX: -10 }}
        animate={{ opacity: 1, scale: 1, rotateX: 0 }}
        transition={{ duration: 0.6, ease: "easeOut", delay: 0.4 }}
        className="bg-gradient-to-br from-white via-red-50/20 to-white border border-slate-200/80 rounded-2xl overflow-hidden shadow-xl hover:shadow-2xl transition-all duration-500 transform hover:-translate-y-1"
        style={{ 
          background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(254,226,226,0.3) 50%, rgba(255,255,255,0.95) 100%)',
          boxShadow: '0 20px 40px -12px rgba(0, 0, 0, 0.15), 0 0 0 1px rgba(255,255,255,0.8) inset'
        }}
      >
        <div className="px-6 py-4 border-b border-slate-200/50 bg-gradient-to-r from-red-500/5 to-pink-500/5">
          <div className="flex items-center gap-2 text-lg font-bold text-red-700">
            🎯 Error Distribution
          </div>
        </div>
        <div className="p-6 relative">
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <defs>
                {pieColors.map((color, index) => (
                  <radialGradient key={`errorGradient${index}`} id={`errorGradient${index}`} cx="30%" cy="30%">
                    <stop offset="0%" stopColor={color} stopOpacity={1}/>
                    <stop offset="70%" stopColor={color} stopOpacity={0.9}/>
                    <stop offset="100%" stopColor={color} stopOpacity={0.6}/>
                  </radialGradient>
                ))}
                <filter id="errorGlow" x="-50%" y="-50%" width="200%" height="200%">
                  <feGaussianBlur stdDeviation="2" result="coloredBlur"/>
                  <feMerge> 
                    <feMergeNode in="coloredBlur"/>
                    <feMergeNode in="SourceGraphic"/> 
                  </feMerge>
                </filter>
              </defs>
              <Pie
                data={data}
                cx="50%"
                cy="45%"
                labelLine={false}
                label={({ name, percent }: any) => `${name}\n${((percent || 0) * 100).toFixed(1)}%`}
                outerRadius={90}
                innerRadius={25}
                fill="#8884d8"
                dataKey="value"
                stroke="rgba(255,255,255,0.6)"
                strokeWidth={1}
              >
                {data.map((entry, index) => (
                  <Cell 
                    key={`cell-${index}`} 
                    fill={`url(#errorGradient${index % pieColors.length})`}
                  />
                ))}
              </Pie>
              <Tooltip 
                contentStyle={{
                  backgroundColor: 'rgba(255, 255, 255, 0.98)',
                  border: '1px solid rgba(226, 232, 240, 0.5)',
                  borderRadius: '12px',
                  boxShadow: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04)',
                  backdropFilter: 'blur(10px)',
                  fontSize: '14px',
                  fontWeight: '500'
                }}
                labelStyle={{ color: '#1e293b', fontWeight: '600' }}
              />
            </PieChart>
          </ResponsiveContainer>
          
          {/* Subtle background */}
          <div className="absolute inset-0 pointer-events-none">
            <div className="absolute top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-40 h-40 bg-gradient-radial from-red-100/10 via-transparent to-transparent rounded-full"></div>
          </div>
        </div>
      </motion.div>
    );
  }

  return null;
}