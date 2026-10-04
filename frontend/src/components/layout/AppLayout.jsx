import React, { useState } from 'react';
import { Outlet, Navigate } from 'react-router-dom';
import Sidebar from './Sidebar';
import Header from './Header';
import QuickCaptureModal from '../capture/QuickCaptureModal';
import { useAuth } from '../../context/AuthContext';

export default function AppLayout() {
  const { user, loading } = useAuth();
  const [captureOpen, setCaptureOpen] = useState(false);

  if (loading) {
    return (
      <div className="min-h-screen bg-dark-900 flex items-center justify-center text-slate-400">
        <div className="flex flex-col items-center gap-3">
          <div className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin"></div>
          <p className="text-xs font-mono">Initializing SkillPilot Personal Technical Memory...</p>
        </div>
      </div>
    );
  }

  if (!user) {
    return <Navigate to="/login" replace />;
  }

  return (
    <div className="flex min-h-screen bg-dark-900 text-slate-100 font-sans">
      <Sidebar onOpenCapture={() => setCaptureOpen(true)} />
      <div className="flex-1 flex flex-col min-w-0">
        <Header />
        <main className="flex-1 p-6 md:p-8 overflow-y-auto">
          <Outlet />
        </main>
      </div>

      {/* Global Quick Capture Modal accessible anywhere */}
      <QuickCaptureModal
        isOpen={captureOpen}
        onClose={() => setCaptureOpen(false)}
        onItemSaved={() => {
          // Trigger optional refresh
        }}
      />
    </div>
  );
}
