import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import { useAuth } from '../context/AuthContext';
import { Lock, Mail, User, ChevronRight, AlertCircle, CheckCircle } from 'lucide-react';

const Signup = () => {
  const [formData, setFormData] = useState({
    email: '',
    fullName: '',
    password: '',
    confirmPassword: ''
  });
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);
  
  const { signup, login } = useAuth();
  const navigate = useNavigate();

  const handleChange = (e) => {
    setFormData({ ...formData, [e.target.name]: e.target.value });
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    if (formData.password !== formData.confirmPassword) {
      setError("Passwords don't match");
      return;
    }

    setLoading(true);

    try {
      await signup(formData.email, formData.fullName, formData.password);
      // Auto login after signup
      await login(formData.email, formData.password);
      navigate('/dashboard');
    } catch (err) {
      console.error(err);
      const errorDetail = err.response?.data?.detail;

      // Handle array of validation errors from FastAPI
      if (Array.isArray(errorDetail)) {
        setError(errorDetail.map(e => e.msg).join(', '));
      } else if (typeof errorDetail === 'string') {
        setError(errorDetail);
      } else {
        setError('Failed to create account. Email might be taken.');
      }
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-[calc(100vh-64px)] flex items-center justify-center p-4">
      <div className="w-full max-w-md animate-fade-in">
        <div className="card border-t-4 border-t-green-500">
          <div className="text-center mb-8">
            <h2 className="text-3xl font-bold mb-2">Create Account</h2>
            <p className="text-[var(--text-muted)]">Start your journey to financial freedom</p>
          </div>

          {error && (
            <div className="bg-red-500/10 border border-red-500/20 text-red-400 p-3 rounded-lg mb-6 flex items-center gap-2 text-sm">
              <AlertCircle size={16} />
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit}>
            <div className="mb-4">
              <label className="block text-sm font-medium mb-1 text-[var(--text-muted)]">Full Name</label>
              <div className="relative">
                <User className="absolute left-3 top-3 text-gray-500" size={18} />
                <input
                  type="text"
                  name="fullName"
                  className="input pl-10 mb-0"
                  placeholder="John Doe"
                  value={formData.fullName}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium mb-1 text-[var(--text-muted)]">Email Address</label>
              <div className="relative">
                <Mail className="absolute left-3 top-3 text-gray-500" size={18} />
                <input
                  type="email"
                  name="email"
                  className="input pl-10 mb-0"
                  placeholder="name@example.com"
                  value={formData.email}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <div className="mb-4">
              <label className="block text-sm font-medium mb-1 text-[var(--text-muted)]">Password</label>
              <div className="relative">
                <Lock className="absolute left-3 top-3 text-gray-500" size={18} />
                <input
                  type="password"
                  name="password"
                  className="input pl-10 mb-0"
                  placeholder="••••••••"
                  value={formData.password}
                  onChange={handleChange}
                  required
                  minLength={6}
                />
              </div>
            </div>

            <div className="mb-6">
              <label className="block text-sm font-medium mb-1 text-[var(--text-muted)]">Confirm Password</label>
              <div className="relative">
                <CheckCircle className="absolute left-3 top-3 text-gray-500" size={18} />
                <input
                  type="password"
                  name="confirmPassword"
                  className="input pl-10 mb-0"
                  placeholder="••••••••"
                  value={formData.confirmPassword}
                  onChange={handleChange}
                  required
                />
              </div>
            </div>

            <button 
              type="submit" 
              className="btn btn-primary w-full flex items-center justify-center gap-2 bg-green-600 hover:bg-green-700 shadow-green-900/20"
              disabled={loading}
            >
              {loading ? (
                <div className="w-5 h-5 border-2 border-white/30 border-t-white rounded-full animate-spin" />
              ) : (
                <>Create Account <ChevronRight size={18} /></>
              )}
            </button>
          </form>

          <div className="mt-6 text-center text-sm text-[var(--text-muted)]">
            Already have an account?{' '}
            <Link to="/login" className="text-blue-400 hover:text-blue-300 font-medium">
              Sign in instead
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
};

export default Signup;
