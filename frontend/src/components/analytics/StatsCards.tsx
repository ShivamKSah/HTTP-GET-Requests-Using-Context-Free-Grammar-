import React from 'react';
import { TrendingUp, TrendingDown } from 'lucide-react';

interface StatsCardsProps {
  stats: {
    total?: number;
    valid?: number;
    invalid?: number;
    successRate?: number;
    avgResponseTime?: number;
    commonError?: string;
  };
}

export default function StatsCards({ stats }: StatsCardsProps) {
  const cards = [
    {
      title: "Total Validations",
      value: stats.total || 0,
      icon: "🔍",
      color: "from-blue-500 to-blue-600",
      change: null
    },
    {
      title: "Success Rate",
      value: `${stats.successRate || 0}%`,
      icon: "✅",
      color: "from-emerald-500 to-emerald-600",
      change: (stats.successRate || 0) >= 75 ? 'up' : 'down'
    },
    {
      title: "Avg Response Time",
      value: `${stats.avgResponseTime || 0}ms`,
      icon: "⚡",
      color: "from-purple-500 to-purple-600",
      change: (stats.avgResponseTime || 0) <= 100 ? 'up' : 'down'
    },
    {
      title: "Most Common Error",
      value: stats.commonError || "None",
      icon: "⚠️",
      color: "from-orange-500 to-orange-600",
      change: null
    }
  ];

  return (
    <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6 mb-8">
      {cards.map((card, index) => (
        <div key={index} className="bg-white/70 backdrop-blur-sm border border-slate-200 hover:border-blue-200 transition-all duration-300 relative overflow-hidden rounded-xl">
          <div className={`absolute top-0 right-0 w-32 h-32 bg-gradient-to-br ${card.color} opacity-5 rounded-full transform translate-x-8 -translate-y-8`} />
          <div className="pb-3 px-6 pt-6">
            <div className="flex items-center justify-between">
              <div className="text-sm font-semibold text-slate-600">
                {card.title}
              </div>
              <span className="text-2xl">{card.icon}</span>
            </div>
          </div>
          <div className="px-6 pb-6 space-y-2">
            <div className="text-2xl font-bold text-slate-900">
              {card.value}
            </div>
            {card.change && (
              <div className={`flex items-center gap-1 text-sm ${
                card.change === 'up' ? 'text-emerald-600' : 'text-red-600'
              }`}>
                {card.change === 'up' ? (
                  <TrendingUp className="w-4 h-4" />
                ) : (
                  <TrendingDown className="w-4 h-4" />
                )}
                <span className="font-medium">
                  {card.change === 'up' ? 'Good' : 'Needs attention'}
                </span>
              </div>
            )}
          </div>
        </div>
      ))}
    </div>
  );
}