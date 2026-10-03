import React, { useState, useEffect } from 'react';
import {
  Settings,
  Users,
  Terminal,
  Archive,
  BookOpen,
  Cpu,
  CheckCircle2,
  Shield,
  Loader2
} from 'lucide-react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';

export default function Admin() {
  const { addToast } = useToast();
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadStats() {
      setLoading(true);
      try {
        const data = await api.getAdminStats();
        setStats(data);
      } catch (err) {
        addToast('Admin access restricted: ' + err.message, 'error');
      } finally {
        setLoading(false);
      }
    }
    loadStats();
  }, []);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              <Settings className="w-6 h-6 text-brand-400" />
              Admin Portal
            </h1>
            <span className="text-[10px] uppercase tracking-wider font-extrabold px-2 py-0.5 rounded-full bg-amber-500/20 text-amber-300 border border-amber-500/30">
              Restricted
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            System metrics, user counts, and local AI health. User data remains private and strictly isolated.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400 flex flex-col items-center justify-center">
          <Loader2 className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mb-3" />
          <p className="text-xs">Fetching system telemetry...</p>
        </div>
      ) : stats ? (
        <div className="space-y-6">
          {/* Key Metrics Grid */}
          <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
            <div className="p-5 rounded-2xl bg-dark-850 border border-slate-800 space-y-2">
              <div className="flex items-center justify-between text-slate-400 text-xs">
                <span>Registered Users</span>
                <Users className="w-4 h-4 text-brand-400" />
              </div>
              <div className="text-3xl font-extrabold text-white">{stats.total_users}</div>
              <div className="text-[11px] text-emerald-400">{stats.active_users} active</div>
            </div>

            <div className="p-5 rounded-2xl bg-dark-850 border border-slate-800 space-y-2">
              <div className="flex items-center justify-between text-slate-400 text-xs">
                <span>Code Analyses</span>
                <Terminal className="w-4 h-4 text-indigo-400" />
              </div>
              <div className="text-3xl font-extrabold text-white">{stats.total_code_analyses}</div>
              <div className="text-[11px] text-slate-400">Processed through AI</div>
            </div>

            <div className="p-5 rounded-2xl bg-dark-850 border border-slate-800 space-y-2">
              <div className="flex items-center justify-between text-slate-400 text-xs">
                <span>Vault Volume</span>
                <Archive className="w-4 h-4 text-emerald-400" />
              </div>
              <div className="text-3xl font-extrabold text-white">{stats.total_vault_items}</div>
              <div className="text-[11px] text-slate-400">Notes, docs & formulas</div>
            </div>

            <div className="p-5 rounded-2xl bg-dark-850 border border-slate-800 space-y-2">
              <div className="flex items-center justify-between text-slate-400 text-xs">
                <span>Learning Logs</span>
                <BookOpen className="w-4 h-4 text-cyan-400" />
              </div>
              <div className="text-3xl font-extrabold text-white">{stats.total_learning_logs}</div>
              <div className="text-[11px] text-slate-400">External events</div>
            </div>
          </div>

          {/* System Health Status */}
          <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800 space-y-4">
            <h3 className="text-sm font-bold text-white flex items-center gap-2">
              <CheckCircle2 className="w-4 h-4 text-emerald-400" />
              System Status & AI Architecture
            </h3>
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
              <div className="p-3.5 rounded-xl bg-dark-900 border border-slate-800">
                <span className="text-slate-500 block mb-1">Platform Status</span>
                <span className="font-semibold text-emerald-400">{stats.system_health}</span>
              </div>
              <div className="p-3.5 rounded-xl bg-dark-900 border border-slate-800">
                <span className="text-slate-500 block mb-1">AI Subsystem</span>
                <span className="font-semibold text-white">{stats.ai_status}</span>
              </div>
              <div className="p-3.5 rounded-xl bg-dark-900 border border-slate-800">
                <span className="text-slate-500 block mb-1">Active Model</span>
                <span className="font-semibold text-brand-300 font-mono">{stats.active_model}</span>
              </div>
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
