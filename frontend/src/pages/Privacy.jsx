import React, { useState, useEffect } from 'react';
import {
  ShieldCheck,
  Cpu,
  Lock,
  DollarSign,
  RefreshCw,
  Sliders,
  CheckCircle2,
  HardDrive,
  Sparkles,
  Server
} from 'lucide-react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';

export default function Privacy() {
  const { addToast } = useToast();
  const [healthData, setHealthData] = useState(null);
  const [testing, setTesting] = useState(false);

  const fetchStatus = async () => {
    setTesting(true);
    try {
      const data = await api.getHealth();
      setHealthData(data);
      addToast('Open AI runtime diagnostics refreshed.', 'info');
    } catch (err) {
      addToast('Failed to contact local AI health endpoint.', 'error');
    } finally {
      setTesting(false);
    }
  };

  useEffect(() => {
    fetchStatus();
  }, []);

  const aiInfo = healthData?.ai;

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              <ShieldCheck className="w-6 h-6 text-emerald-400" />
              Privacy & Open Innovation Architecture
            </h1>
            <span className="text-[10px] uppercase tracking-wider font-extrabold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              Zero Telemetry
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Why open-weight AI is central to CodePilot: private personal memory, zero recurring API toll, and complete developer autonomy.
          </p>
        </div>

        <button
          onClick={fetchStatus}
          disabled={testing}
          className="flex items-center gap-2 px-4 py-2 bg-dark-850 hover:bg-dark-800 border border-slate-700 text-slate-200 rounded-xl text-xs font-semibold transition-all shrink-0"
        >
          <RefreshCw className={`w-3.5 h-3.5 ${testing ? 'animate-spin' : ''}`} />
          Run Health Diagnostics
        </button>
      </div>

      {/* Live AI Engine Status Box */}
      <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800 shadow-xl space-y-4">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center gap-2">
            <span className="w-2.5 h-2.5 rounded-full bg-emerald-400 animate-pulse"></span>
            <h2 className="text-sm font-bold text-white">Active Inference Runtime</h2>
          </div>
          <span className="text-[11px] font-mono text-emerald-400 font-semibold bg-emerald-500/10 px-2.5 py-0.5 rounded-md border border-emerald-500/20">
            {aiInfo?.status === 'connected' ? 'Ollama Daemon Connected' : 'Local Engine Ready (Offline Resilient)'}
          </span>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-3 gap-4 text-xs">
          <div className="p-3.5 rounded-xl bg-dark-900 border border-slate-800">
            <span className="text-slate-500 block mb-1">Model Architecture</span>
            <div className="font-mono font-semibold text-white">{aiInfo?.configured_model || 'llama3.2:3b'}</div>
          </div>
          <div className="p-3.5 rounded-xl bg-dark-900 border border-slate-800">
            <span className="text-slate-500 block mb-1">Inference Host</span>
            <div className="font-mono font-semibold text-white">{aiInfo?.base_url || 'http://localhost:11434'}</div>
          </div>
          <div className="p-3.5 rounded-xl bg-dark-900 border border-slate-800">
            <span className="text-slate-500 block mb-1">Privacy Guarantee</span>
            <div className="font-semibold text-emerald-400">{aiInfo?.privacy_guarantee || '100% Local / Zero Leakage'}</div>
          </div>
        </div>
      </div>

      {/* 4 Pillars of Open Innovation */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {/* Pillar 1: Privacy */}
        <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800 space-y-3 shadow-md">
          <div className="p-2.5 w-fit rounded-xl bg-emerald-500/10 text-emerald-400">
            <Lock className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white">Your Technical History Stays Yours</h3>
          <p className="text-xs text-slate-300 leading-relaxed">
            Your proprietary code solutions, weaknesses, internal company study notes, and career trajectory remain 100% on your laptop. Closed commercial APIs reserve the right to ingest user telemetry; CodePilot runs on open-weight models that keep your memory private.
          </p>
        </div>

        {/* Pillar 2: Cost Independence */}
        <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800 space-y-3 shadow-md">
          <div className="p-2.5 w-fit rounded-xl bg-indigo-500/10 text-indigo-400">
            <DollarSign className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white">Zero Per-Token Micro-Billing</h3>
          <p className="text-xs text-slate-300 leading-relaxed">
            Consistent learning requires constant interaction: analyzing 10 LeetCode solutions a day, asking dozens of doubt clarifications, and generating weekly synthesis tests. With open weights running on Ollama, there is zero per-message cost or artificial token quota.
          </p>
        </div>

        {/* Pillar 3: Model Replaceability */}
        <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800 space-y-3 shadow-md">
          <div className="p-2.5 w-fit rounded-xl bg-brand-500/10 text-brand-400">
            <Sliders className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white">Swappable Model Adapters</h3>
          <p className="text-xs text-slate-300 leading-relaxed">
            CodePilot uses a provider abstraction layer. Switch between <strong>Llama 3.2 3B</strong>, <strong>Qwen 2.5 Coder 7B</strong>, <strong>Mistral 7B</strong>, or <strong>DeepSeek R1 Distill</strong> without rewriting application logic or losing your personal knowledge memory.
          </p>
        </div>

        {/* Pillar 4: Offline Resilience */}
        <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800 space-y-3 shadow-md">
          <div className="p-2.5 w-fit rounded-xl bg-amber-500/10 text-amber-400">
            <HardDrive className="w-5 h-5" />
          </div>
          <h3 className="text-base font-bold text-white">Airplane & Offline Operation</h3>
          <p className="text-xs text-slate-300 leading-relaxed">
            Learn on trains, flights, or when WiFi drops during campus hackathons. The local inference engine and SQLite database operate smoothly without internet connectivity.
          </p>
        </div>
      </div>
    </div>
  );
}
