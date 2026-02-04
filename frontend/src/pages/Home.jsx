import React from 'react';
import { Link } from 'react-router-dom';
import { ArrowRight, ShieldCheck, Zap, BarChart3, MessageSquare } from 'lucide-react';

const Home = () => {
  return (
    <div className="min-h-screen flex flex-col">
      {/* Hero Section */}
      <section className="flex-1 flex flex-col items-center justify-center text-center px-4 py-20 bg-[radial-gradient(ellipse_at_top,_var(--tw-gradient-stops))] from-slate-900 via-[#0f172a] to-[#0f172a]">
        <div className="animate-fade-in">
          <h1 className="text-5xl md:text-7xl font-bold mb-6 bg-gradient-to-r from-blue-400 via-purple-400 to-green-400 bg-clip-text text-transparent">
            Your Personal <br /> AI Financial Advisor
          </h1>
          <p className="text-xl text-[var(--text-muted)] max-w-2xl mx-auto mb-10">
            Stop guessing where your money goes. Upload your bank statements, chat with your data, and get instant actionable insights powered by GPT-4o.
          </p>
          <div className="flex gap-4 justify-center">
            <Link to="/signup" className="btn btn-primary text-lg px-8">
              Get Started <ArrowRight className="ml-2 w-5 h-5" />
            </Link>
            <Link to="/login" className="btn btn-outline text-lg px-8">
              Login
            </Link>
          </div>
        </div>
      </section>

      {/* Feature Grid */}
      <section className="container py-20 grid md:grid-cols-3 gap-8">
        <FeatureCard 
          icon={<Zap className="text-yellow-400" size={32} />}
          title="Instant Ingestion"
          description="Upload PDF statements and let our AI extract, clean, and categorize every transaction in seconds."
        />
        <FeatureCard 
          icon={<MessageSquare className="text-blue-400" size={32} />}
          title="Chat with Data"
          description="Ask questions like 'How much did I spend on coffee last month?' and get immediate answers."
        />
        <FeatureCard 
          icon={<BarChart3 className="text-green-400" size={32} />}
          title="Smart Analytics"
          description="Visualize spending trends, track budgets, and identify potential subscriptions automatically."
        />
      </section>
    </div>
  );
};

const FeatureCard = ({ icon, title, description }) => (
  <div className="card hover:border-[var(--primary)] transition-colors p-8">
    <div className="mb-4 bg-slate-800 w-14 h-14 rounded-full flex items-center justify-center">
      {icon}
    </div>
    <h3 className="text-xl font-bold mb-2 text-white">{title}</h3>
    <p className="text-[var(--text-muted)]">{description}</p>
  </div>
);

export default Home;
