import React, { useState, useRef, useEffect } from 'react';
import api from '../services/api';
import { Send, Bot, User, Loader2 } from 'lucide-react';

const Chat = () => {
  const [messages, setMessages] = useState([
    { role: 'assistant', content: "Hello! I'm your AI Financial Advisor. Ask me anything about your spending, trends, or budget." }
  ]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!input.trim() || loading) return;

    const userMessage = input;
    setInput('');
    setMessages(prev => [...prev, { role: 'user', content: userMessage }]);
    setLoading(true);

    try {
      const response = await api.post('/chat/message', { message: userMessage });
      const assistantMessage = response.data.response;
      setMessages(prev => [...prev, { role: 'assistant', content: assistantMessage }]);
    } catch (error) {
       console.error(error);
       setMessages(prev => [...prev, { role: 'assistant', content: "Sorry, I encountered an error accessing your data. Please try again." }]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="container py-8 h-[calc(100vh-64px)] flex flex-col animate-fade-in">
      {/* Header */}
      <div className="mb-4">
        <h1 className="text-2xl font-bold flex items-center gap-2">
          <Bot className="text-blue-400" /> AI Advisor
        </h1>
        <p className="text-[var(--text-muted)] text-sm">Powered by GPT-4o & LangGraph</p>
      </div>

      {/* Chat Container */}
      <div className="flex-1 bg-[var(--bg-card)] border border-[var(--border)] rounded-xl overflow-hidden flex flex-col shadow-lg">
        {/* Messages */}
        <div className="flex-1 overflow-y-auto p-4 space-y-4">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex ${msg.role === 'user' ? 'justify-end' : 'justify-start'}`}>
              <div 
                className={`max-w-[80%] rounded-2xl px-4 py-3 text-sm leading-relaxed ${
                  msg.role === 'user' 
                    ? 'bg-blue-600 text-white rounded-br-none' 
                    : 'bg-slate-800 text-[var(--text-main)] rounded-bl-none border border-[var(--border)]'
                }`}
              >
                {/* 
                  Note: For production, we'd use ReactMarkdown here to render nice tables/bold text 
                  from the LLM. For now, simple text display.
                */}
                <div style={{whiteSpace: 'pre-wrap'}}>{msg.content}</div>
              </div>
            </div>
          ))}
          {loading && (
             <div className="flex justify-start">
               <div className="bg-slate-800 rounded-2xl px-4 py-3 rounded-bl-none border border-[var(--border)] flex items-center gap-2">
                 <Loader2 size={16} className="animate-spin text-blue-400" />
                 <span className="text-sm text-[var(--text-muted)]">Thinking...</span>
               </div>
             </div>
          )}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Area */}
        <div className="p-4 border-t border-[var(--border)] bg-slate-900/50">
          <form onSubmit={handleSubmit} className="flex gap-2">
            <input
              type="text"
              className="flex-1 bg-[var(--bg-dark)] border border-[var(--border)] rounded-full px-4 py-3 text-sm focus:outline-none focus:border-blue-500 focus:ring-1 focus:ring-blue-500 transition-all"
              placeholder="Ask e.g., 'How much did I spend on Uber last month?'..."
              value={input}
              onChange={(e) => setInput(e.target.value)}
            />
            <button 
              type="submit" 
              className="btn btn-primary rounded-full w-12 h-12 flex items-center justify-center p-0 flex-shrink-0"
              disabled={!input.trim() || loading}
            >
              <Send size={18} />
            </button>
          </form>
        </div>
      </div>
    </div>
  );
};

export default Chat;
