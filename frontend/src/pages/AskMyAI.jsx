import React, { useState, useEffect, useRef } from 'react';
import {
  MessageSquareCode,
  Send,
  Sparkles,
  Bot,
  User,
  ShieldCheck,
  Cpu,
  Layers,
  ArrowRight,
  Loader2
} from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';

const SUGGESTED_PROMPTS = [
  "Why did my Dynamic Programming solution fail on large inputs?",
  "What boundary invariants am I repeatedly missing in search problems?",
  "How does distributed caching connect to my target Backend Software Engineer role?",
  "Explain when to use Sliding Window versus a Monotonic Deque."
];

export default function AskMyAI() {
  const { user } = useAuth();
  const { addToast } = useToast();
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState('');
  const [loading, setLoading] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    const fetchHistory = async () => {
      try {
        const history = await api.getChatHistory();
        if (history && history.length > 0) {
          setMessages(history);
        } else {
          // Pre-populate welcoming contextual message
          setMessages([
            {
              id: 'init-1',
              role: 'assistant',
              content: `Hello ${user?.full_name?.split(' ')[0] || 'Friend'}! I am CodePilot, your personal technical AI companion.\n\nI have loaded your active profile:\n* **Target Role:** Backend Software Engineer\n* **Strong Disciplines:** Binary Search (88%), Sliding Window (82%)\n* **Active Revision Focus:** Dynamic Programming State Transitions\n\nAsk me any technical question, and I'll explain it using what you already know!`,
              context_used: [
                'Target: Backend Software Engineer',
                'DSA Practice History: 23 Problems',
                'Active Focus: DP Boundaries'
              ]
            }
          ]);
        }
      } catch (err) {
        // ignore
      }
    };
    fetchHistory();
  }, [user]);

  useEffect(() => {
    scrollToBottom();
  }, [messages, loading]);

  const handleSend = async (messageText) => {
    const text = messageText || input;
    if (!text.trim() || loading) return;

    const userMsg = {
      id: Date.now(),
      role: 'user',
      content: text,
      context_used: []
    };
    setMessages((prev) => [...prev, userMsg]);
    setInput('');
    setLoading(true);

    try {
      const resp = await api.sendChatMessage(text);
      const asstMsg = {
        id: Date.now() + 1,
        role: 'assistant',
        content: resp.reply,
        context_used: resp.context_used
      };
      setMessages((prev) => [...prev, asstMsg]);
    } catch (err) {
      addToast('Failed to reach AI companion: ' + err.message, 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="max-w-5xl mx-auto h-[calc(100vh-7rem)] flex flex-col bg-dark-850 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
      {/* Companion Top Bar */}
      <div className="px-6 py-4 border-b border-slate-800 bg-dark-900/80 flex items-center justify-between shrink-0">
        <div className="flex items-center gap-3">
          <div className="w-9 h-9 rounded-xl bg-brand-500/15 border border-brand-500/30 text-brand-400 flex items-center justify-center">
            <Bot className="w-5 h-5" />
          </div>
          <div>
            <h2 className="text-sm font-bold text-white flex items-center gap-2">
              Ask My AI
              <span className="text-[10px] px-2 py-0.5 rounded-full bg-emerald-500/10 text-emerald-400 border border-emerald-500/20 font-mono">
                Context-Grounded
              </span>
            </h2>
            <p className="text-[11px] text-slate-400">
              Personalized technical answers grounded in your verified learning history
            </p>
          </div>
        </div>

        <div className="hidden sm:flex items-center gap-2 text-xs text-slate-400">
          <Cpu className="w-3.5 h-3.5 text-emerald-400" />
          <span>Local Open-Weight Model</span>
        </div>
      </div>

      {/* Messages Scroll Area */}
      <div className="flex-1 p-6 overflow-y-auto space-y-6">
        {messages.map((m) => (
          <div
            key={m.id}
            className={`flex gap-3.5 max-w-3xl ${m.role === 'user' ? 'ml-auto flex-row-reverse' : ''}`}
          >
            {/* Avatar */}
            <div
              className={`w-8 h-8 rounded-xl shrink-0 flex items-center justify-center font-bold text-xs ${
                m.role === 'user'
                  ? 'bg-indigo-600 text-white shadow-md shadow-indigo-600/30'
                  : 'bg-brand-500/20 border border-brand-500/40 text-brand-300'
              }`}
            >
              {m.role === 'user' ? <User className="w-4 h-4" /> : <Bot className="w-4 h-4" />}
            </div>

            {/* Message Body */}
            <div className="space-y-2 max-w-[85%]">
              {/* Context Badges (Only for Assistant) */}
              {m.context_used && m.context_used.length > 0 && (
                <div className="flex flex-wrap gap-1.5 pb-1">
                  {m.context_used.map((ctx, idx) => (
                    <span
                      key={idx}
                      className="px-2 py-0.5 rounded-md bg-dark-900 border border-slate-700/80 text-[10px] text-brand-300 font-medium flex items-center gap-1 shadow-sm"
                    >
                      <Sparkles className="w-2.5 h-2.5 text-brand-400" />
                      {ctx}
                    </span>
                  ))}
                </div>
              )}

              <div
                className={`p-4 rounded-2xl text-xs sm:text-sm leading-relaxed whitespace-pre-wrap shadow-sm ${
                  m.role === 'user'
                    ? 'bg-brand-600 text-white rounded-tr-none'
                    : 'bg-dark-900 border border-slate-800 text-slate-200 rounded-tl-none font-sans'
                }`}
              >
                {m.content}
              </div>
            </div>
          </div>
        ))}

        {loading && (
          <div className="flex gap-3.5 max-w-2xl">
            <div className="w-8 h-8 rounded-xl bg-brand-500/20 border border-brand-500/40 text-brand-300 flex items-center justify-center">
              <Bot className="w-4 h-4" />
            </div>
            <div className="p-4 rounded-2xl bg-dark-900 border border-slate-800 text-xs text-slate-400 flex items-center gap-2">
              <Loader2 className="w-4 h-4 animate-spin text-brand-400" />
              <span>Synthesizing response using your personal technical profile...</span>
            </div>
          </div>
        )}
        <div ref={messagesEndRef} />
      </div>

      {/* Suggested Prompts Pills */}
      {messages.length <= 2 && (
        <div className="px-6 py-2 bg-dark-900/40 border-t border-slate-800/60 overflow-x-auto flex items-center gap-2">
          <span className="text-[10px] font-bold text-slate-500 uppercase tracking-wider shrink-0">Try asking:</span>
          {SUGGESTED_PROMPTS.map((prompt, idx) => (
            <button
              key={idx}
              onClick={() => handleSend(prompt)}
              className="px-2.5 py-1 text-[11px] rounded-lg bg-dark-850 hover:bg-dark-800 border border-slate-700 text-slate-300 whitespace-nowrap transition-colors"
            >
              {prompt}
            </button>
          ))}
        </div>
      )}

      {/* Input Field Form */}
      <form onSubmit={(e) => { e.preventDefault(); handleSend(); }} className="p-4 border-t border-slate-800 bg-dark-900 flex items-center gap-3">
        <input
          type="text"
          placeholder="Ask a technical question (e.g. Why does this DP approach work? How does Kafka partitioning scale?)..."
          value={input}
          onChange={(e) => setInput(e.target.value)}
          disabled={loading}
          className="flex-1 px-4 py-2.5 bg-dark-850 border border-slate-800 rounded-xl text-xs sm:text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-colors"
        />
        <button
          type="submit"
          disabled={loading || !input.trim()}
          className="p-2.5 bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white rounded-xl shadow-md shadow-brand-500/20 transition-all hover:scale-105"
        >
          <Send className="w-4 h-4" />
        </button>
      </form>
    </div>
  );
}
