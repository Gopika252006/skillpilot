import React, { useState, useEffect } from 'react';
import {
  CalendarCheck,
  CheckCircle2,
  Clock,
  Sparkles,
  RefreshCw,
  Target,
  ArrowRight,
  BookOpen,
  Loader2
} from 'lucide-react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';

export default function LearningPlan() {
  const { addToast } = useToast();
  const [plan, setPlan] = useState(null);
  const [loading, setLoading] = useState(true);
  const [regenerating, setRegenerating] = useState(false);

  const fetchPlan = async () => {
    setLoading(true);
    try {
      const data = await api.getCurrentPlan();
      setPlan(data);
    } catch (err) {
      addToast('Failed to load weekly plan.', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPlan();
  }, []);

  const handleToggle = async (taskId) => {
    try {
      const updated = await api.toggleTask(taskId);
      setPlan((prev) => ({
        ...prev,
        tasks: prev.tasks.map((t) => (t.id === taskId ? { ...t, is_completed: updated.is_completed } : t))
      }));
      addToast(updated.is_completed ? 'Task completed! Keep up the momentum.' : 'Task marked pending.', 'info');
    } catch (err) {
      addToast('Error updating task: ' + err.message, 'error');
    }
  };

  const handleRegenerate = async () => {
    setRegenerating(true);
    try {
      const newPlan = await api.generatePlan();
      setPlan(newPlan);
      addToast('New adaptive plan generated based on your latest knowledge gaps!', 'success');
    } catch (err) {
      addToast('Failed to regenerate plan.', 'error');
    } finally {
      setRegenerating(false);
    }
  };

  const completedCount = plan?.tasks?.filter((t) => t.is_completed).length || 0;
  const totalCount = plan?.tasks?.length || 7;
  const progressPercent = Math.round((completedCount / totalCount) * 100);

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              <CalendarCheck className="w-6 h-6 text-brand-400" />
              Weekly Learning Plan
            </h1>
            <span className="text-[10px] uppercase tracking-wider font-extrabold px-2 py-0.5 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30">
              15-20 Min / Day
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Monday-style adaptive mission designed for consistent developers. Zero fluff, targeted strictly at your knowledge gaps.
          </p>
        </div>

        <button
          onClick={handleRegenerate}
          disabled={regenerating}
          className="flex items-center gap-2 px-4 py-2.5 bg-dark-850 hover:bg-dark-800 border border-slate-700 text-slate-200 rounded-xl text-xs font-semibold transition-all hover:scale-[1.01] shrink-0"
        >
          {regenerating ? <Loader2 className="w-4 h-4 animate-spin text-brand-400" /> : <RefreshCw className="w-4 h-4" />}
          Regenerate Adaptive Plan
        </button>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400 flex flex-col items-center justify-center">
          <Loader2 className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mb-3" />
          <p className="text-xs">Generating your adaptive weekly sprint...</p>
        </div>
      ) : plan ? (
        <div className="space-y-6">
          {/* Plan Mission Banner */}
          <div className="p-6 rounded-2xl bg-gradient-to-r from-dark-850 via-dark-800 to-indigo-950/30 border border-slate-800 shadow-xl space-y-4">
            <div className="flex flex-col md:flex-row md:items-center justify-between gap-4">
              <div>
                <span className="text-xs font-semibold text-brand-400 uppercase tracking-wider">Weekly Focus</span>
                <h2 className="text-xl font-bold text-white mt-0.5">{plan.week_title}</h2>
                <p className="text-xs text-slate-300 mt-1 max-w-2xl leading-relaxed">{plan.rationale}</p>
              </div>

              {/* Progress dial */}
              <div className="p-4 rounded-xl bg-dark-900 border border-slate-800 shrink-0 text-center min-w-[140px]">
                <div className="text-2xl font-extrabold text-white">{completedCount}/{totalCount}</div>
                <div className="text-[11px] text-slate-400 mt-0.5">Tasks Completed</div>
                <div className="w-full h-1.5 rounded-full bg-slate-800 mt-2 overflow-hidden">
                  <div
                    className="h-full rounded-full bg-emerald-500 transition-all duration-500"
                    style={{ width: `${progressPercent}%` }}
                  ></div>
                </div>
              </div>
            </div>
          </div>

          {/* Daily Tasks List */}
          <div className="space-y-3">
            {plan.tasks?.map((task) => (
              <div
                key={task.id}
                onClick={() => handleToggle(task.id)}
                className={`p-4 rounded-2xl border transition-all cursor-pointer flex items-center justify-between gap-4 group ${
                  task.is_completed
                    ? 'bg-dark-900/60 border-slate-850 opacity-75'
                    : 'bg-dark-850 border-slate-800 hover:border-slate-700 shadow-md'
                }`}
              >
                <div className="flex items-start gap-3.5 min-w-0">
                  <button
                    type="button"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleToggle(task.id);
                    }}
                    className={`w-5 h-5 rounded-lg border flex items-center justify-center mt-0.5 transition-colors ${
                      task.is_completed
                        ? 'bg-emerald-500 border-emerald-500 text-white'
                        : 'border-slate-600 hover:border-brand-500'
                    }`}
                  >
                    {task.is_completed && <CheckCircle2 className="w-3.5 h-3.5" />}
                  </button>

                  <div className="space-y-1 min-w-0">
                    <div className="flex items-center gap-2">
                      <span className="text-[11px] font-bold uppercase tracking-wider text-brand-400">
                        {task.day_of_week}
                      </span>
                      {task.target_concept && (
                        <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-dark-900 text-slate-400 border border-slate-800">
                          {task.target_concept}
                        </span>
                      )}
                    </div>
                    <h3
                      className={`text-sm font-semibold transition-colors ${
                        task.is_completed ? 'line-through text-slate-500' : 'text-white group-hover:text-brand-300'
                      }`}
                    >
                      {task.title}
                    </h3>
                    {task.description && (
                      <p className="text-xs text-slate-400 leading-relaxed">{task.description}</p>
                    )}
                  </div>
                </div>

                <div className="flex items-center gap-1 text-xs text-slate-500 font-mono shrink-0">
                  <Clock className="w-3.5 h-3.5" />
                  <span>{task.estimated_minutes} min</span>
                </div>
              </div>
            ))}
          </div>
        </div>
      ) : null}
    </div>
  );
}
