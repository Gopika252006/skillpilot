import React, { useState } from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { Sparkles, Terminal, ArrowRight, ShieldCheck, UserCheck, Loader2 } from 'lucide-react';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';

export default function Login() {
  const { login, loginDemo } = useAuth();
  const { addToast } = useToast();
  const navigate = useNavigate();

  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [loading, setLoading] = useState(false);
  const [demoLoading, setDemoLoading] = useState(false);

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      const user = await login(email, password);
      addToast(`Welcome back, ${user.full_name}!`, 'success');
      if (!user.onboarding_completed) {
        navigate('/onboarding');
      } else {
        navigate('/');
      }
    } catch (err) {
      addToast(err.message || 'Login failed.', 'error');
    } finally {
      setLoading(false);
    }
  };

  const handleDemoLogin = async (role = 'USER') => {
    setDemoLoading(true);
    try {
      const user = await loginDemo(role);
      addToast(`Logged in as ${user.full_name}!`, 'success');
      navigate('/');
    } catch (err) {
      addToast('Demo login failed: ' + err.message, 'error');
    } finally {
      setDemoLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-900 flex flex-col justify-center items-center p-4">
      <div className="w-full max-w-md space-y-6">
        {/* Brand header */}
        <div className="text-center space-y-2">
          <div className="inline-flex items-center justify-center w-12 h-12 rounded-2xl bg-gradient-to-tr from-brand-600 to-indigo-500 shadow-xl shadow-brand-500/25 text-white mb-2">
            <Sparkles className="w-6 h-6" />
          </div>
          <h1 className="text-2xl font-bold tracking-tight text-white">CodePilot</h1>
          <p className="text-xs text-slate-400">“An AI that knows what you know.”</p>
        </div>

        {/* Demo Fast Login Callout */}
        <div className="p-4 rounded-2xl bg-gradient-to-r from-brand-500/15 via-indigo-500/10 to-transparent border border-brand-500/30 space-y-2.5">
          <div className="flex items-center justify-between">
            <span className="text-xs font-bold text-brand-300 flex items-center gap-1.5">
              <UserCheck className="w-4 h-4" />
              Hackathon Judge / Reviewer Demo
            </span>
            <span className="text-[10px] uppercase font-bold px-1.5 py-0.5 rounded bg-brand-500/20 text-brand-300">
              Instant
            </span>
          </div>
          <p className="text-[11px] text-slate-300 leading-relaxed">
            Login as our real developer friend <strong>Arjun Sharma</strong> with pre-seeded LeetCode analyses, knowledge memory, and Knowledge Vault items ready to demo immediately.
          </p>
          <div className="flex items-center gap-2 pt-1">
            <button
              type="button"
              onClick={() => handleDemoLogin('USER')}
              disabled={demoLoading}
              className="flex-1 py-2 px-3 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold shadow-md shadow-brand-500/20 transition-all flex items-center justify-center gap-1.5"
            >
              {demoLoading ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Terminal className="w-3.5 h-3.5" />}
              <span>Login as Arjun (Friend Profile)</span>
            </button>
            <button
              type="button"
              onClick={() => handleDemoLogin('ADMIN')}
              disabled={demoLoading}
              className="py-2 px-3 bg-dark-850 hover:bg-dark-800 border border-slate-700 text-slate-300 rounded-xl text-xs font-medium transition-all"
              title="Admin role"
            >
              Admin Demo
            </button>
          </div>
        </div>

        {/* Login Card */}
        <div className="p-6 md:p-8 rounded-2xl bg-dark-850 border border-slate-800 shadow-xl space-y-5">
          <form onSubmit={handleSubmit} className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Email Address</label>
              <input
                type="email"
                placeholder="developer@example.com"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Password</label>
              <input
                type="password"
                placeholder="••••••••"
                value={password}
                onChange={(e) => setPassword(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                required
              />
            </div>

            <button
              type="submit"
              disabled={loading}
              className="w-full py-2.5 px-4 bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white rounded-xl text-xs font-semibold shadow-md shadow-brand-500/25 transition-all flex items-center justify-center gap-2"
            >
              {loading ? <Loader2 className="w-4 h-4 animate-spin" /> : <span>Sign In</span>}
            </button>
          </form>

          <div className="text-center pt-2 border-t border-slate-800 text-xs text-slate-400">
            Don't have an account?{' '}
            <NavLink to="/register" className="text-brand-400 hover:text-brand-300 font-semibold">
              Create One
            </NavLink>
          </div>
        </div>
      </div>
    </div>
  );
}
