import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { AreaChart, Area, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer, PieChart, Pie, Cell, Legend } from 'recharts';
import { DollarSign, TrendingUp, ShoppingBag, Calendar, ArrowUpRight, ArrowDownRight } from 'lucide-react';

const Dashboard = () => {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [timeRange, setTimeRange] = useState('30d');

  const COLORS = ['#3b82f6', '#10b981', '#f59e0b', '#ef4444', '#8b5cf6', '#ec4899'];

  // Custom tooltip for pie chart
  const CustomPieTooltip = ({ active, payload }) => {
    if (active && payload && payload.length) {
      const data = payload[0];
      return (
        <div className="bg-[#1e293b] border border-[#334155] px-3 py-2 rounded-lg shadow-lg">
          <p style={{ color: data.payload.fill }} className="font-semibold">
            {data.name}
          </p>
          <p className="text-white text-sm">
            ${data.value.toLocaleString()} ({data.payload.percentage}%)
          </p>
        </div>
      );
    }
    return null;
  };

  useEffect(() => {
    fetchStats();
  }, [timeRange]);

  const fetchStats = async () => {
    setLoading(true);
    try {
      const response = await api.get(`/dashboard/stats?time_range=${timeRange}`);
      setStats(response.data);
    } catch (error) {
      console.error("Failed to fetch dashboard stats", error);
    } finally {
      setLoading(false);
    }
  };

  if (loading && !stats) return <div className="p-10 text-center">Loading dashboard...</div>;

  return (
    <div className="container py-8 animate-fade-in">
      {/* Header */}
      <div className="flex flex-col md:flex-row justify-between items-start md:items-center mb-8 gap-4">
        <div>
          <h1 className="text-3xl font-bold">Financial Overview</h1>
          <p className="text-[var(--text-muted)]">Track your spending and financial health</p>
        </div>
        
        <div className="bg-[var(--bg-card)] p-1 rounded-lg border border-[var(--border)] flex">
          {['7d', '30d', '3m', '6m', '1y'].map(range => (
            <button
              key={range}
              onClick={() => setTimeRange(range)}
              className={`px-3 py-1 text-sm rounded-md transition-all ${timeRange === range ? 'bg-[var(--primary)] text-white shadow-sm' : 'text-[var(--text-muted)] hover:text-white'}`}
            >
              {range.toUpperCase()}
            </button>
          ))}
        </div>
      </div>

      {/* Summary Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mb-8">
        <StatCard 
          title="Total Spent" 
          value={`$${stats?.total_spent?.toLocaleString() || '0'}`} 
          icon={<DollarSign className="text-blue-400" />}
          trend="+12% vs last period" // Placeholder trend logic
          trendUp={false}
        />
        <StatCard 
          title="Top Category" 
          value={stats?.top_category || 'N/A'} 
          icon={<ShoppingBag className="text-purple-400" />}
          trend="Most frequent"
          trendUp={true}
        />
        <StatCard 
          title="Active Trends" 
          value={stats?.monthly_trend?.length || 0} 
          icon={<TrendingUp className="text-green-400" />}
          trend="Data points"
          trendUp={true}
        />
      </div>

      {/* Charts Section */}
      <div className="grid grid-cols-1 lg:grid-cols-3 gap-8">
        
        {/* Main Trend Chart */}
        <div className="card lg:col-span-2">
          <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
            <Calendar size={18} className="text-blue-400" /> Spending Trend
          </h3>
          <div className="h-[300px] w-full">
            <ResponsiveContainer width="100%" height="100%">
              <AreaChart data={stats?.monthly_trend || []}>
                <defs>
                  <linearGradient id="colorAmount" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#3b82f6" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#3b82f6" stopOpacity={0}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#334155" vertical={false} />
                <XAxis 
                  dataKey="period" 
                  stroke="#94a3b8" 
                  tick={{fontSize: 12}} 
                  tickFormatter={(val) => val.split('-').slice(1).join('/') || val}
                />
                <YAxis stroke="#94a3b8" tick={{fontSize: 12}} tickFormatter={(val) => `$${val}`} />
                <Tooltip 
                  contentStyle={{backgroundColor: '#1e293b', borderColor: '#334155', color: '#f8fafc'}}
                  itemStyle={{color: '#fff'}}
                  formatter={(value) => [`$${value}`, 'Spent']}
                />
                <Area 
                  type="monotone" 
                  dataKey="amount" 
                  stroke="#3b82f6" 
                  strokeWidth={2}
                  fillOpacity={1} 
                  fill="url(#colorAmount)" 
                />
              </AreaChart>
            </ResponsiveContainer>
          </div>
        </div>

        {/* Category Breakdown */}
        <div className="card">
          <h3 className="text-lg font-bold mb-6 flex items-center gap-2">
            <PieChart size={18} className="text-purple-400" /> Category Breakdown
          </h3>
          <div className="h-[300px] w-full relative">
             <ResponsiveContainer width="100%" height="100%">
              <PieChart>
                <Pie
                  data={stats?.category_breakdown || []}
                  cx="50%"
                  cy="45%"
                  innerRadius={60}
                  outerRadius={80}
                  paddingAngle={5}
                  dataKey="amount"
                  nameKey="category"
                >
                  {(stats?.category_breakdown || []).map((entry, index) => (
                    <Cell key={`cell-${index}`} fill={COLORS[index % COLORS.length]} />
                  ))}
                </Pie>
                <Tooltip content={<CustomPieTooltip />} />
                <Legend layout="horizontal" verticalAlign="bottom" align="center" wrapperStyle={{paddingTop: '20px'}}/>
              </PieChart>
            </ResponsiveContainer>

            {/* Center Text */}
            <div className="absolute left-1/2 transform -translate-x-1/2 text-center pointer-events-none" style={{ top: 'calc(45% - 10px)' }}>
              <div className="text-xs text-[var(--text-muted)] mb-1">Total</div>
              <div className="font-bold text-xl text-white">${(stats?.total_spent || 0).toLocaleString()}</div>
            </div>
          </div>
        </div>

      </div>
    </div>
  );
};

const StatCard = ({ title, value, icon, trend, trendUp }) => (
  <div className="card hover:border-[var(--primary)] transition-colors">
    <div className="flex justify-between items-start mb-4">
      <div>
        <p className="text-[var(--text-muted)] text-sm font-medium mb-1">{title}</p>
        <h2 className="text-2xl font-bold">{value}</h2>
      </div>
      <div className="p-2 bg-slate-800 rounded-lg">{icon}</div>
    </div>
    <div className={`flex items-center text-sm ${trendUp ? 'text-green-400' : 'text-red-400'}`}>
      {trendUp ? <ArrowUpRight size={16} className="mr-1" /> : <ArrowDownRight size={16} className="mr-1" />}
      {trend}
    </div>
  </div>
);

export default Dashboard;
