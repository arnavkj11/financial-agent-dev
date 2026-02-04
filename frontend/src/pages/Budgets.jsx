import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { Plus, Wallet, AlertCircle, CheckCircle, X } from 'lucide-react';

const Budgets = () => {
  const [budgets, setBudgets] = useState([]); // BudgetStatus list
  const [loading, setLoading] = useState(true);
  const [showModal, setShowModal] = useState(false);
  
  // Form State
  const [category, setCategory] = useState('');
  const [amount, setAmount] = useState('');
  const [submitting, setSubmitting] = useState(false);

  useEffect(() => {
    fetchBudgets();
  }, []);

  const fetchBudgets = async () => {
    setLoading(true);
    try {
      // We use the status endpoint to get both limit and spent
      const response = await api.get('/budgets/status');
      setBudgets(response.data);
    } catch (error) {
      console.error("Failed to fetch budgets", error);
    } finally {
      setLoading(false);
    }
  };

  const handleCreateBudget = async (e) => {
    e.preventDefault();
    if (!category || !amount) return;
    
    setSubmitting(true);
    try {
      await api.post('/budgets/', { 
        category, 
        amount: parseFloat(amount) 
      });
      setShowModal(false);
      setCategory('');
      setAmount('');
      fetchBudgets(); // Refresh list
    } catch (error) {
      console.error("Failed to create budget", error);
      alert("Failed to create budget");
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="container py-8 animate-fade-in relative">
      <div className="flex justify-between items-center mb-8">
        <div>
          <h1 className="text-3xl font-bold">Budget Management</h1>
          <p className="text-[var(--text-muted)]">Set limits and track your spending goals</p>
        </div>
        <button 
          onClick={() => setShowModal(true)} 
          className="btn btn-primary flex items-center gap-2"
        >
          <Plus size={18} /> New Budget
        </button>
      </div>

      {loading ? (
        <div className="text-center py-10">Loading budgets...</div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
          {budgets.length === 0 ? (
             <div className="col-span-full text-center py-20 bg-[var(--bg-card)] rounded-xl border border-[var(--border)] border-dashed">
                <Wallet className="mx-auto text-gray-500 mb-4" size={48} />
                <h3 className="text-xl font-bold mb-2">No budgets set</h3>
                <p className="text-[var(--text-muted)]">Create your first budget to start tracking.</p>
             </div>
          ) : (
            budgets.map((b) => (
              <BudgetCard key={b.category} budget={b} />
            ))
          )}
        </div>
      )}

      {/* Create Modal */}
      {showModal && (
        <div className="fixed inset-0 bg-black/50 backdrop-blur-sm z-50 flex items-center justify-center p-4 animate-fade-in">
          <div className="bg-[var(--bg-card)] border border-[var(--border)] rounded-xl w-full max-w-md p-6 shadow-2xl relative">
            <button 
              onClick={() => setShowModal(false)}
              className="absolute top-4 right-4 text-gray-400 hover:text-white"
            >
              <X size={20} />
            </button>
            
            <h2 className="text-xl font-bold mb-6">Set Budget Goal</h2>
            
            <form onSubmit={handleCreateBudget}>
              <div className="mb-4">
                <label className="block text-sm font-medium mb-1 text-[var(--text-muted)]">Category Name</label>
                <input
                  type="text"
                  className="input"
                  placeholder="e.g. Food, Travel, Shopping"
                  value={category}
                  onChange={(e) => setCategory(e.target.value)}
                  required
                />
              </div>
              
              <div className="mb-6">
                <label className="block text-sm font-medium mb-1 text-[var(--text-muted)]">Monthly Limit ($)</label>
                <input
                  type="number"
                  className="input"
                  placeholder="500"
                  min="1"
                  step="0.01"
                  value={amount}
                  onChange={(e) => setAmount(e.target.value)}
                  required
                />
              </div>

              <div className="flex justify-end gap-3">
                <button 
                  type="button"
                  onClick={() => setShowModal(false)}
                  className="btn btn-outline"
                >
                  Cancel
                </button>
                <button 
                  type="submit"
                  className="btn btn-primary"
                  disabled={submitting}
                >
                  {submitting ? 'Saving...' : 'Save Budget'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
};

const BudgetCard = ({ budget }) => {
  const isOver = budget.spent > budget.limit;
  const progress = Math.min(budget.percent_used, 100);
  const colorClass = isOver ? 'bg-red-500' : (progress > 80 ? 'bg-yellow-500' : 'bg-green-500');

  return (
    <div className="card">
      <div className="flex justify-between items-start mb-4">
        <h3 className="text-lg font-bold">{budget.category}</h3>
        <span className={`text-xs px-2 py-1 rounded-full border ${isOver ? 'border-red-500/50 text-red-400 bg-red-500/10' : 'border-green-500/50 text-green-400 bg-green-500/10'}`}>
          {isOver ? 'Over Budget' : 'On Track'}
        </span>
      </div>
      
      <div className="mb-2 flex justify-between text-sm">
        <span className="text-[var(--text-muted)]">Spent: <span className="text-white font-medium">${budget.spent.toLocaleString()}</span></span>
        <span className="text-[var(--text-muted)]">Limit: <span className="text-white font-medium">${budget.limit.toLocaleString()}</span></span>
      </div>

      {/* Progress Bar */}
      <div className="h-3 w-full bg-slate-800 rounded-full overflow-hidden mb-2">
        <div 
          className={`h-full ${colorClass} transition-all duration-500`} 
          style={{ width: `${progress}%` }} 
        />
      </div>
      
      <div className="text-right text-xs text-[var(--text-muted)]">
        {budget.percent_used}% used
      </div>
    </div>
  );
};

export default Budgets;
