import React from 'react';
import { NavLink, useNavigate } from 'react-router-dom';
import { Shield, LogOut, Cpu, Sparkles } from 'lucide-react';
import { useAuth } from '../../context/AuthContext';
import { useToast } from '../../context/ToastContext';

export default function Header() {
  const { user, logout } = useAuth();
  const { addToast } = useToast();
  const navigate = useNavigate();

  const handleLogout = async () => {
    await logout();
    addToast('Logged out securely.', 'info');
    navigate('/login');
  };

  return (
    <header className="h-14 border-b border-slate-800/80 bg-dark-900/80 backdrop-blur-md px-6 flex items-center justify-between shrink-0 sticky top-0 z-30">
      <div className="flex items-center gap-3">
        <span className="text-xs font-medium text-slate-400">SkillPilot</span>
      </div>

      <div className="flex items-center gap-3">
        {/* Local Open-Weight AI badge */}
        <NavLink
          to="/privacy"
          className="flex items-center gap-2 px-2.5 py-1 rounded-full bg-emerald-500/10 border border-emerald-500/20 text-emerald-400 text-[11px] font-medium hover:bg-emerald-500/15 transition-colors"
          title="Open-Weight AI runs 100% locally. Zero telemetry."
        >
          <span className="w-1.5 h-1.5 rounded-full bg-emerald-400 animate-pulse"></span>
          <Cpu className="w-3 h-3" />
          <span>Local Open AI Engine</span>
        </NavLink>

        {/* Logout */}
        <button
          onClick={handleLogout}
          className="flex items-center gap-1.5 px-3 py-1 text-xs font-medium text-slate-400 hover:text-rose-400 hover:bg-rose-500/10 rounded-lg transition-colors"
          title="Sign out"
        >
          <LogOut className="w-3.5 h-3.5" />
          <span>Logout</span>
        </button>
      </div>
    </header>
  );
}
