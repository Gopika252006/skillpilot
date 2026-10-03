import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { AuthProvider } from './context/AuthContext';
import { ToastProvider } from './context/ToastContext';

// Layout
import AppLayout from './components/layout/AppLayout';

// Pages
import Login from './pages/Login';
import Register from './pages/Register';
import Onboarding from './pages/Onboarding';
import Dashboard from './pages/Dashboard';
import CodeAnalyzer from './pages/CodeAnalyzer';
import KnowledgeVault from './pages/KnowledgeVault';
import MyKnowledge from './pages/MyKnowledge';
import AskMyAI from './pages/AskMyAI';
import LearningPlan from './pages/LearningPlan';
import Assessment from './pages/Assessment';
import CareerPath from './pages/CareerPath';
import Aptitude from './pages/Aptitude';
import Interview from './pages/Interview';
import Explore from './pages/Explore';
import Privacy from './pages/Privacy';
import Admin from './pages/Admin';
import Profile from './pages/Profile';

export default function App() {
  return (
    <BrowserRouter>
      <ToastProvider>
        <AuthProvider>
          <Routes>
            {/* Public routes */}
            <Route path="/login" element={<Login />} />
            <Route path="/register" element={<Register />} />
            <Route path="/onboarding" element={<Onboarding />} />

            {/* Protected app routes */}
            <Route element={<AppLayout />}>
              <Route path="/" element={<Dashboard />} />
              <Route path="/analyzer" element={<CodeAnalyzer />} />
              <Route path="/vault" element={<KnowledgeVault />} />
              <Route path="/knowledge" element={<MyKnowledge />} />
              <Route path="/chat" element={<AskMyAI />} />
              <Route path="/plan" element={<LearningPlan />} />
              <Route path="/assessment" element={<Assessment />} />
              <Route path="/career" element={<CareerPath />} />
              <Route path="/aptitude" element={<Aptitude />} />
              <Route path="/interview" element={<Interview />} />
              <Route path="/explore" element={<Explore />} />
              <Route path="/privacy" element={<Privacy />} />
              <Route path="/admin" element={<Admin />} />
              <Route path="/profile" element={<Profile />} />
            </Route>

            {/* Fallback */}
            <Route path="*" element={<Navigate to="/" replace />} />
          </Routes>
        </AuthProvider>
      </ToastProvider>
    </BrowserRouter>
  );
}
