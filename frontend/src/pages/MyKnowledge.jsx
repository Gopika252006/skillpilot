import React, { useState, useEffect } from 'react';
import {
  Network,
  PlusCircle,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  BookOpen,
  Filter,
  Layers,
  Clock,
  Award,
  ChevronRight,
  TrendingUp,
  X,
  Loader2
} from 'lucide-react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';

export default function MyKnowledge() {
  const { addToast } = useToast();
  const [concepts, setConcepts] = useState([]);
  const [graphData, setGraphData] = useState(null);
  const [logs, setLogs] = useState([]);
  const [activeCategory, setActiveCategory] = useState('ALL');
  const [loading, setLoading] = useState(true);

  // "I Learned This" modal state
  const [learnModalOpen, setLearnModalOpen] = useState(false);
  const [learnTopic, setLearnTopic] = useState('');
  const [learnNotes, setLearnNotes] = useState('');
  const [learnSource, setLearnSource] = useState('Self Study');
  const [learnSaving, setLearnSaving] = useState(false);

  const loadData = async () => {
    setLoading(true);
    try {
      const [conceptsRes, graphRes, logsRes] = await Promise.all([
        api.getConcepts(),
        api.getKnowledgeGraph(),
        api.getLearningLogs()
      ]);
      setConcepts(conceptsRes);
      setGraphData(graphRes);
      setLogs(logsRes);
    } catch (err) {
      addToast('Failed to load knowledge memory.', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadData();
  }, []);

  const handleSaveLearning = async (e) => {
    e.preventDefault();
    if (!learnTopic.trim() || !learnNotes.trim()) return;
    setLearnSaving(true);
    try {
      const res = await api.recordLearningLog({
        topic: learnTopic,
        notes: learnNotes,
        source: learnSource,
        time_spent_mins: 20
      });
      addToast(`Recorded learning! Extracted concepts: ${res.extracted_concepts?.join(', ')}`, 'success');
      setLearnTopic('');
      setLearnNotes('');
      setLearnModalOpen(false);
      loadData();
    } catch (err) {
      addToast('Failed to save learning: ' + err.message, 'error');
    } finally {
      setLearnSaving(false);
    }
  };

  const categories = ['ALL', 'DSA', 'System Design', 'Backend', 'Core CS'];
  const filteredConcepts =
    activeCategory === 'ALL'
      ? concepts
      : concepts.filter((c) => c.category?.toLowerCase() === activeCategory.toLowerCase());

  const getStatusBadge = (status) => {
    switch (status) {
      case 'STRONG':
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-emerald-500/15 text-emerald-400 border border-emerald-500/30">STRONG</span>;
      case 'PRACTICED':
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-cyan-500/15 text-cyan-400 border border-cyan-500/30">PRACTICED</span>;
      case 'LEARNING':
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-amber-500/15 text-amber-400 border border-amber-500/30">LEARNING</span>;
      case 'NEEDS_REVISION':
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-rose-500/15 text-rose-400 border border-rose-500/30">NEEDS REVISION</span>;
      default:
        return <span className="px-2 py-0.5 rounded text-[10px] font-bold bg-slate-800 text-slate-400">NOT STARTED</span>;
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              <Network className="w-6 h-6 text-brand-400" />
              Personal Technical Memory
            </h1>
            <span className="text-[10px] uppercase tracking-wider font-extrabold px-2 py-0.5 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30">
              Core Differentiator
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Evidence-based mastery tracking. Concepts evolve only through verified practice, code analyses, and assessment outcomes.
          </p>
        </div>

        <button
          onClick={() => setLearnModalOpen(true)}
          className="flex items-center gap-2 px-4 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold shadow-lg shadow-brand-500/20 transition-all hover:scale-[1.02] shrink-0"
        >
          <PlusCircle className="w-4 h-4" />
          + I Learned This
        </button>
      </div>

      {/* Memory Summary Stats */}
      {graphData?.stats && (
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
          <div className="p-4 rounded-xl bg-dark-850 border border-slate-800">
            <span className="text-xs text-slate-400">Total Tracked</span>
            <div className="text-2xl font-bold text-white mt-1">{graphData.stats.total_concepts}</div>
          </div>
          <div className="p-4 rounded-xl bg-dark-850 border border-slate-800">
            <span className="text-xs text-emerald-400">Strong Mastery</span>
            <div className="text-2xl font-bold text-emerald-400 mt-1">{graphData.stats.strong}</div>
          </div>
          <div className="p-4 rounded-xl bg-dark-850 border border-slate-800">
            <span className="text-xs text-rose-400">Needs Revision</span>
            <div className="text-2xl font-bold text-rose-400 mt-1">{graphData.stats.needs_revision}</div>
          </div>
          <div className="p-4 rounded-xl bg-dark-850 border border-slate-800">
            <span className="text-xs text-indigo-400">Avg Confidence</span>
            <div className="text-2xl font-bold text-indigo-400 mt-1">
              {Math.round(graphData.stats.average_confidence * 100)}%
            </div>
          </div>
        </div>
      )}

      {/* Visual Hierarchy Diagram Panel */}
      <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800 space-y-4 shadow-xl">
        <div className="flex items-center justify-between border-b border-slate-800 pb-3">
          <div className="flex items-center gap-2">
            <Layers className="w-4 h-4 text-brand-400" />
            <h2 className="text-sm font-bold text-white">Visual Knowledge Hierarchy</h2>
          </div>
          <span className="text-[11px] text-slate-400">Prerequisite & Invariant Mapping</span>
        </div>

        <div className="p-4 rounded-xl bg-dark-900 border border-slate-800/80 font-mono text-xs text-slate-300 overflow-x-auto leading-relaxed">
          <div className="text-brand-400 font-bold mb-1">DSA & Algorithmic Foundations</div>
          <div>├── Arrays & Strings</div>
          <div>│   ├── Binary Search <span className="text-emerald-400 text-[10px] ml-2">[STRONG 88%]</span></div>
          <div>│   └── Sliding Window & Two Pointers <span className="text-emerald-400 text-[10px] ml-2">[STRONG 82%]</span></div>
          <div>├── Dynamic Programming <span className="text-rose-400 text-[10px] ml-2">[NEEDS REVISION 54%]</span></div>
          <div>│   ├── State Invariant Recurrence</div>
          <div>│   └── 2D Memoization Boundaries</div>
          <div>└── Graph Theory <span className="text-cyan-400 text-[10px] ml-2">[PRACTICED 70%]</span></div>
          <div>    ├── Breadth-First Search (Queue Invariants)</div>
          <div>    └── Depth-First Search (Backtracking)</div>
          <div className="text-indigo-400 font-bold mt-3 mb-1">Backend Architecture & Systems</div>
          <div>├── Distributed Caching & Redis <span className="text-amber-400 text-[10px] ml-2">[LEARNING 52%]</span></div>
          <div>├── Event Streaming (Kafka) <span className="text-amber-400 text-[10px] ml-2">[LEARNING 42%]</span></div>
          <div>└── System Scalability & Partitioning <span className="text-amber-400 text-[10px] ml-2">[LEARNING 50%]</span></div>
        </div>
      </div>

      {/* Category Filter Pills */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1">
        {categories.map((cat) => (
          <button
            key={cat}
            onClick={() => setActiveCategory(cat)}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-medium whitespace-nowrap transition-all ${
              activeCategory === cat
                ? 'bg-brand-600 text-white shadow-sm'
                : 'bg-dark-850 text-slate-400 hover:text-slate-200 border border-slate-800'
            }`}
          >
            {cat}
          </button>
        ))}
      </div>

      {/* Concepts Grid */}
      {loading ? (
        <div className="p-12 text-center text-slate-400 flex flex-col items-center justify-center">
          <Loader2 className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mb-3" />
          <p className="text-xs">Loading Knowledge Profile...</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {filteredConcepts.map((concept) => (
            <div
              key={concept.id}
              className="p-5 rounded-2xl bg-dark-850 border border-slate-800 hover:border-slate-700 shadow-md flex flex-col justify-between transition-all"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[11px] font-semibold text-slate-400">{concept.category}</span>
                  {getStatusBadge(concept.status)}
                </div>

                <h3 className="text-base font-bold text-white mb-2">{concept.name}</h3>

                {/* Confidence Bar */}
                <div className="space-y-1 mb-4">
                  <div className="flex items-center justify-between text-[11px]">
                    <span className="text-slate-400">Confidence</span>
                    <span className="font-mono text-slate-200">{Math.round(concept.confidence * 100)}%</span>
                  </div>
                  <div className="w-full h-1.5 rounded-full bg-dark-950 overflow-hidden">
                    <div
                      className={`h-full rounded-full transition-all ${
                        concept.confidence >= 0.8
                          ? 'bg-emerald-500'
                          : concept.confidence >= 0.6
                          ? 'bg-cyan-500'
                          : concept.confidence >= 0.4
                          ? 'bg-amber-500'
                          : 'bg-rose-500'
                      }`}
                      style={{ width: `${Math.round(concept.confidence * 100)}%` }}
                    ></div>
                  </div>
                </div>

                {/* Practice count & success rate */}
                <div className="flex items-center justify-between text-xs text-slate-400 pt-2 border-t border-slate-800/80 mb-3">
                  <span>Practiced: <strong className="text-slate-200">{concept.practice_count}x</strong></span>
                  <span>Success: <strong className="text-slate-200">{Math.round((concept.success_rate || 0.7) * 100)}%</strong></span>
                </div>

                {/* Repeated Mistakes Alert */}
                {concept.repeated_mistakes?.length > 0 && (
                  <div className="p-3 rounded-xl bg-rose-500/10 border border-rose-500/20 text-xs space-y-1 mt-2">
                    <div className="flex items-center gap-1.5 font-bold text-rose-300">
                      <AlertTriangle className="w-3.5 h-3.5 text-rose-400 shrink-0" />
                      <span>Recurring Blind Spot:</span>
                    </div>
                    {concept.repeated_mistakes.map((m, idx) => (
                      <p key={idx} className="text-rose-200/90 text-[11px] pl-4">
                        • {m}
                      </p>
                    ))}
                  </div>
                )}
              </div>
            </div>
          ))}
        </div>
      )}

      {/* "I Learned This" Modal */}
      {learnModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-lg bg-dark-850 border border-slate-800 rounded-2xl shadow-2xl p-6">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-brand-400" />
                  "I Learned This" — Capture External Study
                </h3>
                <p className="text-xs text-slate-400">AI will extract concepts and update your memory profile</p>
              </div>
              <button
                onClick={() => setLearnModalOpen(false)}
                className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleSaveLearning} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">What did you learn today?</label>
                <input
                  type="text"
                  placeholder="e.g. How Kafka consumer groups handle partition rebalancing"
                  value={learnTopic}
                  onChange={(e) => setLearnTopic(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Key Takeaways & Notes</label>
                <textarea
                  rows={4}
                  placeholder="Cooperative sticky assignors avoid stopping the world during rebalances. Heartbeat timeouts must be tuned against heavy poll batch durations..."
                  value={learnNotes}
                  onChange={(e) => setLearnNotes(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Source</label>
                <select
                  value={learnSource}
                  onChange={(e) => setLearnSource(e.target.value)}
                  className="w-full px-3.5 py-2 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-brand-500"
                >
                  <option value="LeetCode / Contest">LeetCode / Contest</option>
                  <option value="Official Documentation">Official Documentation</option>
                  <option value="System Design Book / Blog">System Design Book / Blog</option>
                  <option value="YouTube / Tech Talk">YouTube / Tech Talk</option>
                  <option value="Self Study">Self Study</option>
                </select>
              </div>

              <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => setLearnModalOpen(false)}
                  className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-white"
                >
                  Cancel
                </button>
                <button
                  type="submit"
                  disabled={learnSaving}
                  className="flex items-center gap-2 px-5 py-2 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold shadow-md shadow-brand-500/25"
                >
                  {learnSaving ? <Loader2 className="w-3.5 h-3.5 animate-spin" /> : <Sparkles className="w-3.5 h-3.5" />}
                  Save Learning & Update Memory
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  );
}
