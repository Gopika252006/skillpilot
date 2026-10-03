import React, { useState, useEffect } from 'react';
import {
  User,
  Settings,
  Briefcase,
  Calendar,
  Sparkles,
  Save,
  CheckCircle2,
  Loader2
} from 'lucide-react';
import { api } from '../services/api';
import { useAuth } from '../context/AuthContext';
import { useToast } from '../context/ToastContext';

export default function Profile() {
  const { user, setUser } = useAuth();
  const { addToast } = useToast();
  const [profile, setProfile] = useState(null);
  const [loading, setLoading] = useState(true);
  const [saving, setSaving] = useState(false);

  const [targetRole, setTargetRole] = useState('');
  const [experienceLevel, setExperienceLevel] = useState('Intermediate');
  const [learningGoals, setLearningGoals] = useState('');
  const [weeklyHours, setWeeklyHours] = useState(7);

  useEffect(() => {
    async function load() {
      setLoading(true);
      try {
        const data = await api.getProfile();
        setProfile(data);
        setTargetRole(data.target_role || 'Backend Software Engineer');
        setExperienceLevel(data.experience_level || 'Intermediate');
        setLearningGoals(data.learning_goals || '');
        setWeeklyHours(data.weekly_hours || 7);
      } catch (err) {
        addToast('Failed to load profile data.', 'error');
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  const handleSave = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      const updated = await api.updateProfile({
        target_role: targetRole,
        experience_level: experienceLevel,
        learning_goals: learningGoals,
        weekly_hours: Number(weeklyHours)
      });
      setProfile(updated);
      const me = await api.getMe();
      setUser(me);
      addToast('Profile updated successfully!', 'success');
    } catch (err) {
      addToast('Error updating profile: ' + err.message, 'error');
    } finally {
      setSaving(false);
    }
  };

  return (
    <div className="space-y-6 max-w-3xl mx-auto">
      {/* Header */}
      <div className="pb-2 border-b border-slate-800">
        <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
          <Settings className="w-6 h-6 text-brand-400" />
          Developer Profile & Settings
        </h1>
        <p className="text-xs text-slate-400 mt-1">
          Manage your personal learning parameters, career target, and account details.
        </p>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400 flex flex-col items-center justify-center">
          <Loader2 className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mb-3" />
          <p className="text-xs">Loading profile settings...</p>
        </div>
      ) : (
        <form onSubmit={handleSave} className="p-6 md:p-8 rounded-2xl bg-dark-850 border border-slate-800 space-y-6 shadow-xl">
          {/* User info box */}
          <div className="flex items-center gap-4 p-4 rounded-xl bg-dark-900 border border-slate-800">
            <div className="w-12 h-12 rounded-xl bg-gradient-to-tr from-brand-600 to-indigo-500 text-white flex items-center justify-center font-bold text-lg">
              {user?.full_name ? user.full_name[0].toUpperCase() : 'U'}
            </div>
            <div>
              <h3 className="text-sm font-bold text-white">{user?.full_name}</h3>
              <p className="text-xs text-slate-400">{user?.email}</p>
              <span className="inline-block mt-1 text-[10px] font-mono px-2 py-0.5 rounded bg-dark-850 border border-slate-700 text-brand-300">
                Role: {user?.role}
              </span>
            </div>
          </div>

          <div className="space-y-4">
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Target Engineering Role</label>
              <input
                type="text"
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                required
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Experience Level</label>
              <select
                value={experienceLevel}
                onChange={(e) => setExperienceLevel(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-brand-500"
              >
                <option value="Beginner">Beginner</option>
                <option value="Intermediate">Intermediate</option>
                <option value="Advanced">Advanced</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Learning Goals</label>
              <textarea
                rows={3}
                value={learningGoals}
                onChange={(e) => setLearningGoals(e.target.value)}
                className="w-full p-3.5 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
              />
            </div>

            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Weekly Learning Hours</label>
              <input
                type="number"
                min="1"
                max="40"
                value={weeklyHours}
                onChange={(e) => setWeeklyHours(e.target.value)}
                className="w-full px-3.5 py-2.5 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-brand-500"
              />
            </div>
          </div>

          <div className="flex justify-end pt-4 border-t border-slate-800">
            <button
              type="submit"
              disabled={saving}
              className="flex items-center gap-2 px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold shadow-md shadow-brand-500/25 transition-all"
            >
              {saving ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Save className="w-3.5 h-3.5" />}
              <span>Save Changes</span>
            </button>
          </div>
        </form>
      )}
    </div>
  );
}
