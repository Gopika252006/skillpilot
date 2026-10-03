import React, { useState, useEffect } from 'react';
import { NavLink } from 'react-router-dom';
import {
  Sparkles,
  TrendingUp,
  AlertTriangle,
  CheckCircle2,
  Terminal,
  Calendar,
  ArrowRight,
  BookOpen,
  Award,
  Briefcase,
  Layers,
  ChevronRight,
  Archive,
  RefreshCw,
  Cpu
} from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';

export default function Dashboard() {
  const { user } = useAuth();
  const { addToast } = useToast();
  const [loading, setLoading] = useState(true);
  const [concepts, setConcepts] = useState([]);
  const [recentAnalyses, setRecentAnalyses] = useState([]);
  const [weeklyPlan, setWeeklyPlan] = useState(null);
  const [careerPath, setCareerPath] = useState(null);
  const [revisionItems, setRevisionItems] = useState([]);

  const loadDashboardData = async () => {
    setLoading(true);
    try {
      const [conceptsData, historyData, planData, careerData, revisionsData] = await Promise.all([
        api.getConcepts().catch(() => []),
        api.getCodeHistory(3).catch(() => []),
        api.getCurrentPlan().catch(() => null),
        api.getCareerPath().catch(() => null),
        api.getVaultRevisions().catch(() => [])
      ]);

      setConcepts(conceptsData);
      setRecentAnalyses(historyData);
      setWeeklyPlan(planData);
      setCareerPath(careerData);
      setRevisionItems(revisionsData);
    } catch (err) {
      addToast('Error loading dashboard data.', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadDashboardData();
  }, []);

  const strongConcepts = concepts.filter((c) => c.status === 'STRONG' || c.confidence >= 0.8);
  const weakConcepts = concepts.filter((c) => c.status === 'NEEDS_REVISION' || c.status === 'LEARNING');
  const readinessScore = careerPath?.readiness_score || 75;

  return (
    <div className="space-y-8 max-w-7xl mx-auto">
      {/* Top Banner / Friend Persona Welcome */}
      <div className="relative overflow-hidden rounded-2xl bg-gradient-to-r from-dark-850 via-dark-800 to-indigo-950/40 border border-slate-800 p-6 md:p-8 shadow-xl">
        <div className="relative z-10 flex flex-col md:flex-row md:items-center justify-between gap-6">
          <div className="space-y-2">
            <div className="inline-flex items-center gap-2 px-2.5 py-1 rounded-full bg-brand-500/10 border border-brand-500/30 text-brand-300 text-xs font-semibold">
              <Sparkles className="w-3.5 h-3.5" />
              <span>Personal Technical Intelligence</span>
            </div>
            <h1 className="text-2xl md:text-3xl font-bold tracking-tight text-white">
              Welcome back, {user?.full_name?.split(' ')[0] || 'Friend'}
            </h1>
            <p className="text-sm text-slate-400 max-w-2xl leading-relaxed">
              CodePilot continuously maps your LeetCode problem solving, learning notes, and contest practice into your private technical knowledge memory.
            </p>
          </div>

          <div className="flex items-center gap-3">
            <NavLink
              to="/analyzer"
              className="flex items-center gap-2 px-4 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold shadow-lg shadow-brand-500/25 transition-all hover:scale-[1.02]"
            >
              <Terminal className="w-4 h-4" />
              Analyze New Code
            </NavLink>
            <NavLink
              to="/vault"
              className="flex items-center gap-2 px-4 py-2.5 bg-dark-800 hover:bg-dark-700 border border-slate-700 text-slate-200 rounded-xl text-xs font-medium transition-all"
            >
              <Archive className="w-4 h-4" />
              Knowledge Vault
            </NavLink>
          </div>
        </div>
      </div>

      {/* 3 Core Questions Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Metric 1: What do I know? */}
        <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800/80 shadow-lg relative overflow-hidden flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">What Do I Know?</span>
              <div className="p-2 rounded-xl bg-emerald-500/10 text-emerald-400">
                <CheckCircle2 className="w-4 h-4" />
              </div>
            </div>
            <div className="text-3xl font-extrabold text-white mb-1">
              {strongConcepts.length} <span className="text-sm font-medium text-slate-400">Strong Concepts</span>
            </div>
            <p className="text-xs text-slate-400 mb-4">
              Demonstrated through consistent correct solutions & verified asymptotic complexity bounds.
            </p>
            <div className="flex flex-wrap gap-1.5">
              {strongConcepts.slice(0, 3).map((c) => (
                <span
                  key={c.id}
                  className="px-2.5 py-1 rounded-lg bg-emerald-500/10 border border-emerald-500/20 text-emerald-300 text-[11px] font-medium"
                >
                  {c.name}
                </span>
              ))}
              {strongConcepts.length === 0 && (
                <span className="text-xs text-slate-500 italic">Submit solutions to Code Analyzer to verify strong skills.</span>
              )}
            </div>
          </div>
          <NavLink
            to="/knowledge"
            className="mt-6 flex items-center justify-between text-xs font-semibold text-brand-400 hover:text-brand-300 pt-3 border-t border-slate-800"
          >
            <span>Explore Knowledge Graph</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </NavLink>
        </div>

        {/* Metric 2: What am I improving? */}
        <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800/80 shadow-lg relative overflow-hidden flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">What Am I Improving?</span>
              <div className="p-2 rounded-xl bg-rose-500/10 text-rose-400">
                <AlertTriangle className="w-4 h-4" />
              </div>
            </div>
            <div className="text-3xl font-extrabold text-white mb-1">
              {weakConcepts.length} <span className="text-sm font-medium text-slate-400">Revision Focus</span>
            </div>
            <p className="text-xs text-slate-400 mb-4">
              Identified from repeated boundary edge cases and state recurrence mistakes.
            </p>
            <div className="flex flex-wrap gap-1.5">
              {weakConcepts.slice(0, 3).map((c) => (
                <span
                  key={c.id}
                  className="px-2.5 py-1 rounded-lg bg-rose-500/10 border border-rose-500/20 text-rose-300 text-[11px] font-medium"
                >
                  {c.name}
                </span>
              ))}
            </div>
          </div>
          <NavLink
            to="/plan"
            className="mt-6 flex items-center justify-between text-xs font-semibold text-brand-400 hover:text-brand-300 pt-3 border-t border-slate-800"
          >
            <span>View Adaptive Plan</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </NavLink>
        </div>

        {/* Metric 3: What should I do next? */}
        <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800/80 shadow-lg relative overflow-hidden flex flex-col justify-between">
          <div>
            <div className="flex items-center justify-between mb-4">
              <span className="text-xs font-semibold text-slate-400 uppercase tracking-wider">Target Direction</span>
              <div className="p-2 rounded-xl bg-brand-500/10 text-brand-400">
                <Briefcase className="w-4 h-4" />
              </div>
            </div>
            <div className="text-2xl font-bold text-white mb-1">
              {readinessScore}% <span className="text-sm font-medium text-slate-400">Ready</span>
            </div>
            <p className="text-xs text-slate-400 mb-3">
              Target Role: <strong className="text-slate-200">{careerPath?.target_role || 'Backend Software Engineer'}</strong>
            </p>
            <div className="p-2.5 rounded-xl bg-dark-900 border border-slate-800 text-xs text-slate-300">
              <span className="font-semibold text-brand-400">Recommended Action:</span>{' '}
              {careerPath?.recommended_actions?.[0]?.skill || 'Revise Distributed Caching & Redis'}
            </div>
          </div>
          <NavLink
            to="/career"
            className="mt-6 flex items-center justify-between text-xs font-semibold text-brand-400 hover:text-brand-300 pt-3 border-t border-slate-800"
          >
            <span>Inspect Skill Gaps</span>
            <ChevronRight className="w-3.5 h-3.5" />
          </NavLink>
        </div>
      </div>

      {/* Smart Revision Callout if user has saved items matching weak concepts */}
      {revisionItems.length > 0 && (
        <div className="p-5 rounded-2xl bg-amber-500/10 border border-amber-500/20 flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div className="flex items-start gap-3">
            <div className="p-2 rounded-xl bg-amber-500/20 text-amber-300 shrink-0 mt-0.5">
              <Archive className="w-5 h-5" />
            </div>
            <div>
              <h3 className="text-sm font-bold text-amber-200">
                Smart Revision Alert: Saved Material Available
              </h3>
              <p className="text-xs text-amber-300/80 mt-0.5">
                You have saved notes in Knowledge Vault on <strong>{revisionItems[0].concept}</strong> that directly address your current revision focus.
              </p>
            </div>
          </div>
          <NavLink
            to="/vault"
            className="px-4 py-2 bg-amber-500/20 hover:bg-amber-500/30 text-amber-200 rounded-xl text-xs font-semibold border border-amber-500/40 whitespace-nowrap self-start sm:self-auto transition-colors"
          >
            Review Vault Material
          </NavLink>
        </div>
      )}

      {/* Two Column Layout: Recent Code Analyses & Current Weekly Focus */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-8">
        {/* Left: Recent Code Analyses */}
        <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800/80 shadow-lg">
          <div className="flex items-center justify-between mb-5">
            <div className="flex items-center gap-2.5">
              <div className="p-2 rounded-xl bg-brand-500/10 text-brand-400">
                <Terminal className="w-4 h-4" />
              </div>
              <h2 className="text-base font-bold text-white">Recent Code Analyses</h2>
            </div>
            <NavLink to="/analyzer" className="text-xs text-brand-400 hover:text-brand-300 font-medium">
              View All
            </NavLink>
          </div>

          <div className="space-y-3">
            {recentAnalyses.length === 0 ? (
              <div className="p-6 text-center rounded-xl bg-dark-900 border border-slate-800 text-slate-400 text-xs">
                No solutions analyzed yet. Paste your LeetCode code in Code Analyzer to start building your technical profile.
              </div>
            ) : (
              recentAnalyses.map((a) => (
                <div
                  key={a.id}
                  className="p-4 rounded-xl bg-dark-900 border border-slate-800/80 hover:border-slate-700 transition-all flex items-center justify-between"
                >
                  <div className="min-w-0 pr-3">
                    <p className="text-xs font-semibold text-white truncate">{a.problem_title}</p>
                    <p className="text-[11px] text-slate-400 mt-0.5 truncate">{a.approach_detected}</p>
                    <div className="flex items-center gap-2 mt-2">
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-dark-800 text-slate-300 border border-slate-700">
                        {a.time_complexity}
                      </span>
                      <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-dark-800 text-slate-300 border border-slate-700">
                        {a.space_complexity}
                      </span>
                    </div>
                  </div>
                  <div className="text-right shrink-0">
                    <span className="px-2 py-1 rounded-md text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      Score {a.code_quality_score}/10
                    </span>
                  </div>
                </div>
              ))
            )}
          </div>
        </div>

        {/* Right: Today's Adaptive Plan & Upcoming Weekend Assessment */}
        <div className="space-y-6">
          {/* Weekly Plan Snapshot */}
          <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800/80 shadow-lg">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center gap-2.5">
                <div className="p-2 rounded-xl bg-indigo-500/10 text-indigo-400">
                  <Calendar className="w-4 h-4" />
                </div>
                <div>
                  <h2 className="text-base font-bold text-white">Current Weekly Sprint</h2>
                  <p className="text-xs text-slate-400">{weeklyPlan?.week_title || 'Weekly Learning Mission'}</p>
                </div>
              </div>
              <NavLink to="/plan" className="text-xs text-brand-400 hover:text-brand-300 font-medium">
                Manage
              </NavLink>
            </div>

            <div className="space-y-2 mt-4">
              {weeklyPlan?.tasks?.slice(0, 3).map((task) => (
                <div
                  key={task.id}
                  className="flex items-center justify-between p-3 rounded-xl bg-dark-900 border border-slate-800 text-xs"
                >
                  <div className="flex items-center gap-3 min-w-0">
                    <div
                      className={`w-4 h-4 rounded-md border flex items-center justify-center ${
                        task.is_completed
                          ? 'bg-emerald-500/20 border-emerald-500 text-emerald-400'
                          : 'border-slate-700'
                      }`}
                    >
                      {task.is_completed && <CheckCircle2 className="w-3 h-3" />}
                    </div>
                    <span className={`truncate ${task.is_completed ? 'line-through text-slate-500' : 'text-slate-200'}`}>
                      {task.title}
                    </span>
                  </div>
                  <span className="text-[10px] text-slate-500 font-mono shrink-0 ml-2">
                    {task.estimated_minutes}m
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Assessment & Placement Sprint Card */}
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
            <div className="p-5 rounded-2xl bg-dark-850 border border-slate-800 flex flex-col justify-between">
              <div>
                <div className="p-2 w-fit rounded-xl bg-amber-500/10 text-amber-400 mb-3">
                  <Award className="w-4 h-4" />
                </div>
                <h3 className="text-sm font-bold text-white">Weekend Assessment</h3>
                <p className="text-xs text-slate-400 mt-1">
                  Adaptive 5-question test based on this week's practice.
                </p>
              </div>
              <NavLink
                to="/assessment"
                className="mt-4 inline-flex items-center gap-1.5 text-xs font-semibold text-brand-400 hover:text-brand-300"
              >
                <span>Take Test</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </NavLink>
            </div>

            <div className="p-5 rounded-2xl bg-dark-850 border border-slate-800 flex flex-col justify-between">
              <div>
                <div className="p-2 w-fit rounded-xl bg-emerald-500/10 text-emerald-400 mb-3">
                  <Layers className="w-4 h-4" />
                </div>
                <h3 className="text-sm font-bold text-white">Aptitude Sprint</h3>
                <p className="text-xs text-slate-400 mt-1">
                  5 daily quick questions (Quant, Logic, Verbal).
                </p>
              </div>
              <NavLink
                to="/aptitude"
                className="mt-4 inline-flex items-center gap-1.5 text-xs font-semibold text-brand-400 hover:text-brand-300"
              >
                <span>Daily 5 Qs</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </NavLink>
            </div>
          </div>
        </div>
      </div>
    </div>
  );
}
