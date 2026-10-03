import React from 'react';
import { NavLink } from 'react-router-dom';
import {
  LayoutDashboard,
  Terminal,
  Archive,
  Network,
  MessageSquareCode,
  CalendarCheck,
  Award,
  Compass,
  Briefcase,
  Layers,
  Sparkles,
  ShieldCheck,
  Settings,
  PlusCircle,
  HelpCircle,
  UserCheck
} from 'lucide-react';
import { useAuth } from '../../context/AuthContext';

export default function Sidebar({ onOpenCapture }) {
  const { user } = useAuth();
  const isAdmin = user?.role === 'ADMIN';

  const navItems = [
    { to: '/', label: 'Dashboard', icon: LayoutDashboard },
    { to: '/analyzer', label: 'Code Analyzer', icon: Terminal, badge: 'Hero' },
    { to: '/vault', label: 'Knowledge Vault', icon: Archive, badge: 'Brain' },
    { to: '/knowledge', label: 'My Knowledge', icon: Network },
    { to: '/chat', label: 'Ask My AI', icon: MessageSquareCode },
    { to: '/plan', label: 'Weekly Plan', icon: CalendarCheck },
    { to: '/assessment', label: 'Assessments', icon: Award },
    { to: '/career', label: 'Career Path', icon: Briefcase },
    { to: '/aptitude', label: 'Aptitude Sprint', icon: Layers },
    { to: '/interview', label: 'Adaptive Interview', icon: UserCheck },
    { to: '/explore', label: 'Explore Tech', icon: Compass },
    { to: '/privacy', label: 'Privacy & Open AI', icon: ShieldCheck },
  ];

  if (isAdmin) {
    navItems.push({ to: '/admin', label: 'Admin Portal', icon: Settings, badge: 'Admin' });
  }

  return (
    <aside className="w-64 bg-dark-950 border-r border-slate-800/80 flex flex-col shrink-0 h-screen sticky top-0">
      {/* Brand logo & tagline */}
      <div className="p-5 border-b border-slate-800/80">
        <div className="flex items-center gap-2.5">
          <div className="w-9 h-9 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 flex items-center justify-center shadow-lg shadow-brand-500/20 text-white font-bold">
            <Sparkles className="w-5 h-5" />
          </div>
          <div>
            <h1 className="text-base font-bold tracking-tight text-white flex items-center gap-1.5">
              CodePilot
            </h1>
            <p className="text-[10px] text-slate-400 font-medium">An AI that knows what you know</p>
          </div>
        </div>

        {/* Quick Capture Button */}
        <button
          onClick={onOpenCapture}
          className="w-full mt-4 flex items-center justify-center gap-2 py-2 px-3 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold shadow-md shadow-brand-500/20 transition-all hover:scale-[1.01]"
        >
          <PlusCircle className="w-4 h-4" />
          + Quick Capture
        </button>
      </div>

      {/* Nav links */}
      <nav className="flex-1 px-3 py-4 space-y-1 overflow-y-auto">
        <div className="text-[10px] font-semibold uppercase tracking-wider text-slate-500 px-3 pb-1.5">
          Workspace
        </div>
        {navItems.map((item) => {
          const Icon = item.icon;
          return (
            <NavLink
              key={item.to}
              to={item.to}
              end={item.to === '/'}
              className={({ isActive }) =>
                `flex items-center justify-between px-3 py-2 rounded-xl text-xs font-medium transition-all ${
                  isActive
                    ? 'bg-brand-600/15 text-brand-400 border border-brand-500/30'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-850/60'
                }`
              }
            >
              <div className="flex items-center gap-2.5">
                <Icon className="w-4 h-4 shrink-0" />
                <span>{item.label}</span>
              </div>
              {item.badge && (
                <span
                  className={`text-[9px] px-1.5 py-0.5 rounded font-bold uppercase tracking-wider ${
                    item.badge === 'Hero'
                      ? 'bg-brand-500/20 text-brand-300 border border-brand-500/30'
                      : item.badge === 'Brain'
                      ? 'bg-emerald-500/20 text-emerald-300 border border-emerald-500/30'
                      : 'bg-amber-500/20 text-amber-300 border border-amber-500/30'
                  }`}
                >
                  {item.badge}
                </span>
              )}
            </NavLink>
          );
        })}
      </nav>

      {/* User profile drawer */}
      <div className="p-3 border-t border-slate-800/80 bg-dark-900/60">
        <div className="flex items-center justify-between p-2 rounded-xl bg-dark-850 border border-slate-800">
          <div className="flex items-center gap-2.5 min-w-0">
            <div className="w-7 h-7 rounded-lg bg-indigo-600/30 border border-indigo-500/40 text-indigo-300 flex items-center justify-center font-bold text-xs shrink-0">
              {user?.full_name ? user.full_name[0].toUpperCase() : 'U'}
            </div>
            <div className="min-w-0">
              <p className="text-xs font-semibold text-white truncate">{user?.full_name || 'Developer'}</p>
              <p className="text-[10px] text-slate-400 truncate">{user?.role || 'USER'}</p>
            </div>
          </div>
          <NavLink
            to="/profile"
            className="p-1 text-slate-400 hover:text-white rounded-md hover:bg-slate-800 transition-colors"
            title="Profile & Settings"
          >
            <Settings className="w-3.5 h-3.5" />
          </NavLink>
        </div>
      </div>
    </aside>
  );
}
