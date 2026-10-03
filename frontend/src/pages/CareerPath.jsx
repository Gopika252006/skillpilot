import React, { useState, useEffect } from 'react';
import {
  Briefcase,
  CheckCircle2,
  AlertCircle,
  Sparkles,
  ArrowRight,
  TrendingUp,
  FolderGit2,
  Award,
  Layers,
  ChevronRight,
  Loader2
} from 'lucide-react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';

export default function CareerPath() {
  const { addToast } = useToast();
  const [careerData, setCareerData] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadData() {
      setLoading(true);
      try {
        const data = await api.getCareerPath();
        setCareerData(data);
      } catch (err) {
        addToast('Failed to load career intelligence data.', 'error');
      } finally {
        setLoading(false);
      }
    }
    loadData();
  }, []);

  return (
    <div className="space-y-6 max-w-6xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              <Briefcase className="w-6 h-6 text-brand-400" />
              Career & Skill Gap Intelligence
            </h1>
            <span className="text-[10px] uppercase tracking-wider font-extrabold px-2 py-0.5 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30">
              Role Alignment
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Bridging your verified problem-solving and technical memory directly to industry role requirements.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400 flex flex-col items-center justify-center">
          <Loader2 className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mb-3" />
          <p className="text-xs">Analyzing skill gap against target role...</p>
        </div>
      ) : careerData ? (
        <div className="space-y-6">
          {/* Target Role & Readiness Gauge Banner */}
          <div className="p-6 md:p-8 rounded-2xl bg-gradient-to-r from-dark-850 via-dark-800 to-indigo-950/40 border border-slate-800 shadow-xl flex flex-col md:flex-row md:items-center justify-between gap-6">
            <div className="space-y-2">
              <span className="text-xs font-semibold text-brand-400 uppercase tracking-wider">Target Career Direction</span>
              <h2 className="text-2xl font-bold text-white">{careerData.target_role}</h2>
              <p className="text-xs text-slate-300 max-w-2xl leading-relaxed">
                Based on your voluntary code analyses and learning logs, CodePilot calculates your technical benchmark for senior interview readiness.
              </p>
            </div>

            <div className="p-5 rounded-2xl bg-dark-900 border border-slate-800 shrink-0 text-center min-w-[160px]">
              <div className="text-3xl font-extrabold text-white">{careerData.readiness_score}%</div>
              <div className="text-xs text-slate-400 mt-0.5">Role Readiness</div>
              <div className="w-full h-1.5 rounded-full bg-slate-800 mt-2.5 overflow-hidden">
                <div
                  className="h-full rounded-full bg-brand-500"
                  style={{ width: `${careerData.readiness_score}%` }}
                ></div>
              </div>
            </div>
          </div>

          {/* Strong Skills vs Skill Gaps */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Proven Strong Skills */}
            <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800 shadow-lg space-y-4">
              <div className="flex items-center gap-2 pb-2 border-b border-slate-800">
                <CheckCircle2 className="w-4 h-4 text-emerald-400" />
                <h3 className="text-sm font-bold text-white">Proven Strong Skills</h3>
              </div>
              <p className="text-xs text-slate-400">
                Verified through correct solutions, contest performance, and solid Big-O bounds.
              </p>
              <div className="space-y-2">
                {careerData.strong_skills?.map((skill, idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded-xl bg-dark-900 border border-slate-800 flex items-center justify-between text-xs text-slate-200"
                  >
                    <span className="font-semibold text-white">{skill}</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">
                      MATCH
                    </span>
                  </div>
                ))}
              </div>
            </div>

            {/* Gap Skills */}
            <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800 shadow-lg space-y-4">
              <div className="flex items-center gap-2 pb-2 border-b border-slate-800">
                <AlertCircle className="w-4 h-4 text-amber-400" />
                <h3 className="text-sm font-bold text-white">Missing / Next-Level Gaps</h3>
              </div>
              <p className="text-xs text-slate-400">
                High-yield technical requirements for {careerData.target_role} not yet proven in your profile.
              </p>
              <div className="space-y-2">
                {careerData.gap_skills?.map((gap, idx) => (
                  <div
                    key={idx}
                    className="p-3 rounded-xl bg-dark-900 border border-slate-800 flex items-center justify-between text-xs text-slate-200"
                  >
                    <span className="font-semibold text-white">{gap}</span>
                    <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/15 text-amber-400 border border-amber-500/30">
                      GAP
                    </span>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Recommended Next Actions with Rationale */}
          <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800 shadow-lg space-y-4">
            <div className="flex items-center gap-2 pb-2 border-b border-slate-800">
              <TrendingUp className="w-4 h-4 text-brand-400" />
              <h3 className="text-sm font-bold text-white">Prioritized Recommended Actions</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {careerData.recommended_actions?.map((act, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-dark-900 border border-slate-800 space-y-2">
                  <div className="flex items-center justify-between">
                    <span className="font-bold text-sm text-white">{act.skill}</span>
                    <span className="text-[10px] font-bold px-2 py-0.5 rounded bg-brand-500/20 text-brand-300 border border-brand-500/30 uppercase">
                      {act.priority} Priority
                    </span>
                  </div>
                  <p className="text-xs text-slate-400 leading-relaxed">{act.why}</p>
                </div>
              ))}
            </div>
          </div>

          {/* Recommended Projects */}
          <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800 shadow-lg space-y-4">
            <div className="flex items-center gap-2 pb-2 border-b border-slate-800">
              <FolderGit2 className="w-4 h-4 text-indigo-400" />
              <h3 className="text-sm font-bold text-white">High-Value Projects for Your Portfolio</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {careerData.recommended_projects?.map((proj, idx) => (
                <div key={idx} className="p-5 rounded-xl bg-dark-900 border border-slate-800 space-y-3 flex flex-col justify-between">
                  <div>
                    <h4 className="text-sm font-bold text-white mb-1">{proj.title}</h4>
                    <p className="text-xs text-slate-300 leading-relaxed mb-3">{proj.description}</p>
                    <div className="p-3 rounded-lg bg-dark-850 border border-slate-800 text-[11px] text-slate-400">
                      <strong className="text-brand-300">Why this fits:</strong> {proj.why}
                    </div>
                  </div>
                  <div className="flex flex-wrap gap-1.5 pt-2">
                    {proj.skills?.map((sk, sIdx) => (
                      <span key={sIdx} className="text-[10px] font-medium px-2 py-0.5 rounded bg-brand-500/10 text-brand-300 border border-brand-500/20">
                        {sk}
                      </span>
                    ))}
                  </div>
                </div>
              ))}
            </div>
          </div>

          {/* Recommended Certifications */}
          <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800 shadow-lg space-y-4">
            <div className="flex items-center gap-2 pb-2 border-b border-slate-800">
              <Award className="w-4 h-4 text-cyan-400" />
              <h3 className="text-sm font-bold text-white">Strategic Certifications</h3>
            </div>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              {careerData.recommended_certifications?.map((cert, idx) => (
                <div key={idx} className="p-4 rounded-xl bg-dark-900 border border-slate-800 space-y-1.5">
                  <h4 className="text-xs font-bold text-white">{cert.title}</h4>
                  <p className="text-xs text-slate-400 leading-relaxed">{cert.why}</p>
                </div>
              ))}
            </div>
          </div>

          {/* AI Disclaimer */}
          <div className="text-center text-[11px] text-slate-500 italic pt-2">
            * Clearly labeled: AI-generated recommendations based on your personal knowledge profile, not guaranteed career outcome.
          </div>
        </div>
      ) : null}
    </div>
  );
}
