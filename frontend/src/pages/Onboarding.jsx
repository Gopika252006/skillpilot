import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Sparkles, ArrowRight, CheckCircle2, Loader2 } from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';

const ROLES = [
  'Backend Software Engineer',
  'Software Engineer',
  'Full Stack Developer',
  'AI/ML Engineer',
  'Data Engineer',
  'Cloud / DevOps Engineer'
];

const INTERESTS = [
  'DSA',
  'System Design',
  'OOP',
  'DBMS',
  'OS',
  'Computer Networks',
  'Java',
  'Python',
  'AI/ML',
  'Cloud',
  'DevOps',
  'Web Development',
  'Cybersecurity'
];

export default function Onboarding() {
  const { setUser } = useAuth();
  const { addToast } = useToast();
  const navigate = useNavigate();

  const [step, setStep] = useState(1);
  const [targetRole, setTargetRole] = useState(ROLES[0]);
  const [selectedInterests, setSelectedInterests] = useState(['DSA', 'System Design', 'Backend']);
  const [experienceLevel, setExperienceLevel] = useState('Intermediate');
  const [goals, setGoals] = useState('Targeting Tier-1 product companies. Build mastery over advanced dynamic programming, distributed systems, and Kafka pipelines.');
  const [weeklyHours, setWeeklyHours] = useState(7);
  const [saving, setSaving] = useState(false);

  const toggleInterest = (interest) => {
    setSelectedInterests((prev) =>
      prev.includes(interest) ? prev.filter((i) => i !== interest) : [...prev, interest]
    );
  };

  const handleFinish = async () => {
    setSaving(true);
    try {
      await api.updateProfile({
        target_role: targetRole,
        interests: selectedInterests,
        experience_level: experienceLevel,
        learning_goals: goals,
        weekly_hours: Number(weeklyHours),
        onboarding_completed: true
      });
      const updatedUser = await api.getMe();
      setUser(updatedUser);
      addToast('Profile initialized! Personal Technical Memory is ready.', 'success');
      navigate('/');
    } catch (err) {
      addToast('Failed to save onboarding: ' + err.message, 'error');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="min-h-screen bg-dark-900 flex items-center justify-center p-4">
      <div className="w-full max-w-2xl bg-dark-850 border border-slate-800 rounded-2xl shadow-2xl p-6 md:p-8 space-y-6">
        {/* Progress indicator */}
        <div className="flex items-center justify-between border-b border-slate-800 pb-4">
          <div className="flex items-center gap-2">
            <div className="w-8 h-8 rounded-xl bg-brand-500/10 text-brand-400 flex items-center justify-center font-bold text-xs">
              {step}/3
            </div>
            <div>
              <h2 className="text-sm font-bold text-white">Personalizing Your CodePilot</h2>
              <p className="text-[11px] text-slate-400">Step {step} of 3</p>
            </div>
          </div>
        </div>

        {/* Step 1: Target Role & Level */}
        {step === 1 && (
          <div className="space-y-5 animate-fade-in">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-2">
                What is your target engineering role?
              </label>
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-2.5">
                {ROLES.map((r) => (
                  <button
                    key={r}
                    type="button"
                    onClick={() => setTargetRole(r)}
                    className={`p-3 rounded-xl border text-left text-xs font-medium transition-all ${
                      targetRole === r
                        ? 'bg-brand-600/20 border-brand-500 text-white font-semibold shadow-sm'
                        : 'bg-dark-900 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-200'
                    }`}
                  >
                    {r}
                  </button>
                ))}
              </div>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-2">
                Your current proficiency level:
              </label>
              <div className="grid grid-cols-3 gap-2.5">
                {['Beginner', 'Intermediate', 'Advanced'].map((lvl) => (
                  <button
                    key={lvl}
                    type="button"
                    onClick={() => setExperienceLevel(lvl)}
                    className={`p-2.5 rounded-xl border text-center text-xs font-medium transition-all ${
                      experienceLevel === lvl
                        ? 'bg-brand-600/20 border-brand-500 text-white font-semibold'
                        : 'bg-dark-900 border-slate-800 text-slate-400 hover:text-slate-200'
                    }`}
                  >
                    {lvl}
                  </button>
                ))}
              </div>
            </div>

            <div className="flex justify-end pt-3">
              <button
                type="button"
                onClick={() => setStep(2)}
                className="flex items-center gap-2 px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold shadow-md shadow-brand-500/25 transition-all"
              >
                <span>Next: Technical Interests</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}

        {/* Step 2: Interests Selection */}
        {step === 2 && (
          <div className="space-y-5 animate-fade-in">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Select your core technical disciplines & interests:
              </label>
              <p className="text-xs text-slate-500 mb-3">CodePilot uses these to calibrate your weekly recommendations.</p>
              <div className="flex flex-wrap gap-2">
                {INTERESTS.map((interest) => {
                  const selected = selectedInterests.includes(interest);
                  return (
                    <button
                      key={interest}
                      type="button"
                      onClick={() => toggleInterest(interest)}
                      className={`px-3.5 py-2 rounded-xl border text-xs font-medium transition-all ${
                        selected
                          ? 'bg-brand-600/20 border-brand-500 text-brand-300 shadow-sm'
                          : 'bg-dark-900 border-slate-800 text-slate-400 hover:border-slate-700 hover:text-slate-200'
                      }`}
                    >
                      {interest}
                    </button>
                  );
                })}
              </div>
            </div>

            <div className="flex items-center justify-between pt-3">
              <button
                type="button"
                onClick={() => setStep(1)}
                className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-white"
              >
                Back
              </button>
              <button
                type="button"
                onClick={() => setStep(3)}
                className="flex items-center gap-2 px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold shadow-md shadow-brand-500/25 transition-all"
              >
                <span>Next: Goals & Commitment</span>
                <ArrowRight className="w-3.5 h-3.5" />
              </button>
            </div>
          </div>
        )}

        {/* Step 3: Goals & Time Commitment */}
        {step === 3 && (
          <div className="space-y-5 animate-fade-in">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                What are your current learning & career goals?
              </label>
              <textarea
                rows={3}
                value={goals}
                onChange={(e) => setGoals(e.target.value)}
                className="w-full p-3.5 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">
                Available weekly learning hours:
              </label>
              <div className="flex items-center gap-3">
                <input
                  type="range"
                  min="3"
                  max="25"
                  value={weeklyHours}
                  onChange={(e) => setWeeklyHours(e.target.value)}
                  className="flex-1 accent-brand-500"
                />
                <span className="text-xs font-bold text-brand-400 min-w-[70px] text-right font-mono">
                  {weeklyHours} hrs/week
                </span>
              </div>
              <p className="text-[11px] text-slate-500 mt-1">
                Target: ~15 to 25 minutes of focused problem solving per day.
              </p>
            </div>

            <div className="flex items-center justify-between pt-3">
              <button
                type="button"
                onClick={() => setStep(2)}
                className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-white"
              >
                Back
              </button>
              <button
                type="button"
                onClick={handleFinish}
                disabled={saving}
                className="flex items-center gap-2 px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold shadow-lg shadow-brand-500/25 transition-all hover:scale-105"
              >
                {saving ? (
                  <>
                    <Loader2 className="w-3.5 h-3.5 animate-spin" />
                    <span>Initializing Knowledge Brain...</span>
                  </>
                ) : (
                  <>
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    <span>Complete & Enter Dashboard</span>
                  </>
                )}
              </button>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
