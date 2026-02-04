import React from 'react';
import { Link, useNavigate, useLocation } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { LayoutDashboard, Wallet, Upload, MessageSquare, LogOut, PieChart } from 'lucide-react';

const Navbar = () => {
  const { user, logout } = useAuth();
  const navigate = useNavigate();
  const location = useLocation();

  const handleLogout = () => {
    logout();
    navigate('/login');
  };

  const isActive = (path) => location.pathname === path ? 'text-blue-500' : 'text-gray-400 hover:text-white';

  return (
    <nav className="border-b border-[var(--border)] bg-[var(--bg-card)] sticky top-0 z-50">
      <div className="container flex items-center justify-between h-16">
        <Link to="/" className="text-xl font-bold bg-gradient-to-r from-blue-400 to-green-400 bg-clip-text text-transparent">
          FinanceAgent
        </Link>
        
        <div className="flex items-center gap-6">
          {user ? (
            <>
              <NavLink to="/dashboard" icon={<LayoutDashboard size={20} />} label="Dashboard" />
              <NavLink to="/budgets" icon={<Wallet size={20} />} label="Budgets" />
              <NavLink to="/upload" icon={<Upload size={20} />} label="Upload" />
              <NavLink to="/chat" icon={<MessageSquare size={20} />} label="Advisor" />
              <button onClick={handleLogout} className="flex items-center gap-2 text-red-400 hover:text-red-300 ml-4 font-medium transition-colors">
                <LogOut size={20} />
                <span>Logout</span>
              </button>
            </>
          ) : (
            <div className="flex gap-4">
               <Link to="/login" className="btn btn-outline">Login</Link>
               <Link to="/signup" className="btn btn-primary">Sign Up</Link>
            </div>
          )}
        </div>
      </div>
    </nav>
  );
};

const NavLink = ({ to, icon, label }) => {
  const location = useLocation();
  const active = location.pathname === to;
  
  return (
    <Link to={to} className={`flex items-center gap-2 font-medium transition-colors ${active ? 'text-[var(--primary)]' : 'text-[var(--text-muted)] hover:text-white'}`}>
      {icon}
      <span>{label}</span>
    </Link>
  );
};

export default Navbar;
