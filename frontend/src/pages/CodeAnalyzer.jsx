import React, { useState } from 'react';
import {
  Terminal,
  Play,
  Sparkles,
  CheckCircle2,
  AlertTriangle,
  Lightbulb,
  Clock,
  HardDrive,
  Code2,
  ChevronDown,
  ChevronUp,
  Cpu,
  BookmarkPlus,
  Loader2
} from 'lucide-react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';

const PRESETS = [
  {
    name: 'Binary Search (Rotated Array)',
    lang: 'python',
    title: 'Search in Rotated Sorted Array',
    statement: 'Given an integer array nums sorted in ascending order and rotated at an unknown pivot index, search for target in O(log n) runtime.',
    code: `def search(nums: list[int], target: int) -> int:
    low, high = 0, len(nums) - 1
    while low <= high:
        mid = (low + high) // 2
        if nums[mid] == target:
            return mid
        # Check if left half is sorted
        if nums[low] <= nums[mid]:
            if nums[low] <= target < nums[mid]:
                high = mid - 1
            else:
                low = mid + 1
        else:
            if nums[mid] < target <= nums[high]:
                low = mid + 1
            else:
                high = mid - 1
    return -1`
  },
  {
    name: 'Sliding Window (Longest Substring)',
    lang: 'python',
    title: 'Longest Substring Without Repeating Characters',
    statement: 'Find the length of the longest substring without repeating characters.',
    code: `def lengthOfLongestSubstring(s: str) -> int:
    char_map = {}
    left = 0
    max_len = 0
    for right, char in enumerate(s):
        if char in char_map and char_map[char] >= left:
            left = char_map[char] + 1
        char_map[char] = right
        max_len = max(max_len, right - left + 1)
    return max_len`
  },
  {
    name: 'Dynamic Programming (Coin Change)',
    lang: 'python',
    title: 'Coin Change Minimum Coins',
    statement: 'Return the fewest number of coins that you need to make up that amount.',
    code: `def coinChange(coins: list[int], amount: int) -> int:
    # DP array initialized to sentinel
    dp = [amount + 1] * (amount + 1)
    dp[0] = 0
    for coin in coins:
        for x in range(coin, amount + 1):
            dp[x] = min(dp[x], dp[x - coin] + 1)
    return dp[amount] if dp[amount] != amount + 1 else -1`
  }
];

export default function CodeAnalyzer() {
  const { addToast } = useToast();
  const [problemTitle, setProblemTitle] = useState(PRESETS[0].title);
  const [problemStatement, setProblemStatement] = useState(PRESETS[0].statement);
  const [language, setLanguage] = useState(PRESETS[0].lang);
  const [userCode, setUserCode] = useState(PRESETS[0].code);

  const [loading, setLoading] = useState(false);
  const [result, setResult] = useState(null);

  // Progressive hints toggle states
  const [showHint1, setShowHint1] = useState(false);
  const [showHint2, setShowHint2] = useState(false);
  const [showDeeper, setShowDeeper] = useState(false);
  const [showOptimized, setShowOptimized] = useState(false);

  const handlePreset = (preset) => {
    setProblemTitle(preset.title);
    setProblemStatement(preset.statement);
    setLanguage(preset.lang);
    setUserCode(preset.code);
    setResult(null);
  };

  const handleAnalyze = async (e) => {
    e.preventDefault();
    if (!userCode.trim()) {
      addToast('Please enter your code to analyze.', 'error');
      return;
    }
    setLoading(true);
    setResult(null);
    setShowHint1(false);
    setShowHint2(false);
    setShowDeeper(false);
    setShowOptimized(false);

    try {
      const data = await api.analyzeCode({
        problem_title: problemTitle,
        problem_statement: problemStatement,
        language,
        user_code: userCode
      });
      setResult(data);
      addToast('Analysis complete! Personal Technical Memory updated with practice evidence.', 'success');
    } catch (err) {
      addToast(err.message || 'Analysis failed. Please verify connection.', 'error');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Header */}
      <div className="flex flex-col md:flex-row md:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              <Terminal className="w-6 h-6 text-brand-400" />
              Code Analyzer
            </h1>
            <span className="text-[10px] uppercase tracking-wider font-extrabold px-2 py-0.5 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30">
              Hero Feature
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Open-weight AI analyzes your complexity, extracts algorithmic concepts, detects boundary bugs, and feeds verified evidence into your Personal Knowledge Memory.
          </p>
        </div>

        {/* Quick sample load pills */}
        <div className="flex items-center gap-1.5 flex-wrap">
          <span className="text-[11px] text-slate-500 font-medium mr-1">Load Demo:</span>
          {PRESETS.map((p) => (
            <button
              key={p.name}
              type="button"
              onClick={() => handlePreset(p)}
              className="px-2.5 py-1 text-[11px] font-medium rounded-lg bg-dark-850 hover:bg-dark-800 text-slate-300 border border-slate-700 transition-colors"
            >
              {p.name.split(' ')[0]}
            </button>
          ))}
        </div>
      </div>

      {/* Main Grid: Code Submission Left, Analysis Right */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-6">
        {/* Editor Form (7 cols) */}
        <div className="lg:col-span-7 space-y-4">
          <form onSubmit={handleAnalyze} className="p-5 rounded-2xl bg-dark-850 border border-slate-800 space-y-4 shadow-xl">
            {/* Title and Language */}
            <div className="grid grid-cols-1 sm:grid-cols-3 gap-3">
              <div className="sm:col-span-2">
                <label className="block text-xs font-semibold text-slate-300 mb-1">Problem Title</label>
                <input
                  type="text"
                  value={problemTitle}
                  onChange={(e) => setProblemTitle(e.target.value)}
                  placeholder="e.g. Search in Rotated Sorted Array"
                  className="w-full px-3.5 py-2 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">Language</label>
                <select
                  value={language}
                  onChange={(e) => setLanguage(e.target.value)}
                  className="w-full px-3.5 py-2 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white focus:outline-none focus:border-brand-500"
                >
                  <option value="python">Python</option>
                  <option value="java">Java</option>
                  <option value="cpp">C++</option>
                  <option value="javascript">JavaScript</option>
                </select>
              </div>
            </div>

            {/* Problem Statement */}
            <div>
              <label className="block text-xs font-semibold text-slate-300 mb-1">Problem Statement (Optional)</label>
              <textarea
                rows={2}
                value={problemStatement}
                onChange={(e) => setProblemStatement(e.target.value)}
                placeholder="Paste the problem description or constraints..."
                className="w-full px-3.5 py-2 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
              />
            </div>

            {/* Code Input */}
            <div>
              <div className="flex items-center justify-between mb-1">
                <label className="text-xs font-semibold text-slate-300">Your Code Solution</label>
                <span className="text-[10px] text-slate-500 font-mono">Lines: {userCode.split('\n').length}</span>
              </div>
              <textarea
                rows={14}
                value={userCode}
                onChange={(e) => setUserCode(e.target.value)}
                placeholder="Paste your solution here..."
                className="w-full p-4 bg-dark-950 border border-slate-800 rounded-xl code-font text-xs text-slate-200 placeholder-slate-600 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 leading-relaxed"
                required
              />
            </div>

            {/* Submit Action */}
            <div className="flex items-center justify-between pt-2">
              <span className="text-[11px] text-slate-400 flex items-center gap-1.5">
                <Cpu className="w-3.5 h-3.5 text-emerald-400" />
                Local Open-Weight Model (Ollama / Local Inference)
              </span>
              <button
                type="submit"
                disabled={loading}
                className="flex items-center gap-2 px-6 py-2.5 bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white rounded-xl text-xs font-semibold shadow-lg shadow-brand-500/25 transition-all hover:scale-[1.02]"
              >
                {loading ? (
                  <>
                    <Loader2 className="w-4 h-4 animate-spin" />
                    <span>Analyzing Invariants & Complexity...</span>
                  </>
                ) : (
                  <>
                    <Play className="w-4 h-4 fill-current" />
                    <span>Analyze Code</span>
                  </>
                )}
              </button>
            </div>
          </form>
        </div>

        {/* Analysis Results View (5 cols) */}
        <div className="lg:col-span-5 space-y-4">
          {!result && !loading && (
            <div className="p-8 rounded-2xl bg-dark-850 border border-slate-800 text-center flex flex-col items-center justify-center min-h-[460px]">
              <div className="p-4 rounded-2xl bg-brand-500/10 text-brand-400 mb-3">
                <Code2 className="w-8 h-8" />
              </div>
              <h3 className="text-base font-bold text-white mb-1">Ready for Analysis</h3>
              <p className="text-xs text-slate-400 max-w-xs text-center leading-relaxed">
                Click <strong>Analyze Code</strong> to detect algorithmic approach, time/space complexity, progressive hints, and update your personal knowledge profile.
              </p>
            </div>
          )}

          {loading && (
            <div className="p-8 rounded-2xl bg-dark-850 border border-slate-800 text-center flex flex-col items-center justify-center min-h-[460px] animate-pulse">
              <div className="w-10 h-10 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mb-4"></div>
              <p className="text-sm font-semibold text-white">Extracting Algorithmic Evidence...</p>
              <p className="text-xs text-slate-400 mt-1">Verifying Big-O bounds and boundary conditions</p>
            </div>
          )}

          {result && (
            <div className="space-y-4 animate-fade-in">
              {/* Core metrics panel */}
              <div className="p-5 rounded-2xl bg-dark-850 border border-slate-800 space-y-4 shadow-xl">
                <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                  <div>
                    <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Approach Detected</span>
                    <h3 className="text-sm font-bold text-white mt-0.5">{result.approach_detected}</h3>
                  </div>
                  <div className="text-right">
                    <span className="text-[10px] font-semibold text-slate-400 uppercase tracking-wider">Quality</span>
                    <div className="text-base font-extrabold text-emerald-400">
                      {result.code_quality_score}/10
                    </div>
                  </div>
                </div>

                {/* Big-O Complexity */}
                <div className="grid grid-cols-2 gap-3">
                  <div className="p-3 rounded-xl bg-dark-900 border border-slate-800">
                    <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
                      <Clock className="w-3.5 h-3.5 text-indigo-400" />
                      <span>Time Complexity</span>
                    </div>
                    <div className="text-sm font-mono font-bold text-indigo-300">{result.time_complexity}</div>
                  </div>

                  <div className="p-3 rounded-xl bg-dark-900 border border-slate-800">
                    <div className="flex items-center gap-1.5 text-xs text-slate-400 mb-1">
                      <HardDrive className="w-3.5 h-3.5 text-cyan-400" />
                      <span>Space Complexity</span>
                    </div>
                    <div className="text-sm font-mono font-bold text-cyan-300">{result.space_complexity}</div>
                  </div>
                </div>

                {/* Concepts detected */}
                <div>
                  <span className="text-xs font-semibold text-slate-400 block mb-1.5">Concepts Demonstrated</span>
                  <div className="flex flex-wrap gap-1.5">
                    {result.concepts_detected.map((c) => (
                      <span
                        key={c}
                        className="px-2.5 py-1 rounded-lg text-[11px] font-semibold bg-brand-500/10 text-brand-300 border border-brand-500/25"
                      >
                        {c}
                      </span>
                    ))}
                  </div>
                </div>

                {/* Memory update confirmation badge */}
                <div className="p-3 rounded-xl bg-emerald-500/10 border border-emerald-500/25 text-emerald-300 text-xs flex items-start gap-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0 mt-0.5" />
                  <div>
                    <span className="font-semibold">Personal Technical Memory Updated:</span> Practice count and confidence score recorded.
                  </div>
                </div>

                {/* Boundary / Improvement warnings */}
                {result.improvements?.length > 0 && (
                  <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs space-y-1">
                    <div className="flex items-center gap-1.5 font-bold text-amber-300">
                      <AlertTriangle className="w-3.5 h-3.5 text-amber-400" />
                      <span>Boundary Check & Caveats</span>
                    </div>
                    {result.improvements.map((imp, idx) => (
                      <p key={idx} className="text-amber-200/90 pl-5 text-[11px] leading-relaxed">
                        • {imp}
                      </p>
                    ))}
                  </div>
                )}
              </div>

              {/* Progressive Learning Hints (Does NOT immediately dump optimal code) */}
              <div className="p-5 rounded-2xl bg-dark-850 border border-slate-800 space-y-3">
                <div className="flex items-center gap-2 pb-2 border-b border-slate-800">
                  <Lightbulb className="w-4 h-4 text-amber-400" />
                  <h4 className="text-xs font-bold uppercase tracking-wider text-slate-200">
                    Progressive Learning Hints
                  </h4>
                </div>

                {/* Hint 1 */}
                <div className="rounded-xl border border-slate-800 bg-dark-900 overflow-hidden">
                  <button
                    type="button"
                    onClick={() => setShowHint1(!showHint1)}
                    className="w-full px-3.5 py-2.5 text-left text-xs font-semibold text-slate-300 flex items-center justify-between hover:text-white"
                  >
                    <span>Hint 1: Structural Direction</span>
                    {showHint1 ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                  </button>
                  {showHint1 && (
                    <div className="px-3.5 pb-3 pt-1 text-xs text-slate-300 leading-relaxed border-t border-slate-800/80 bg-dark-950/50">
                      {result.hint_1}
                    </div>
                  )}
                </div>

                {/* Hint 2 */}
                <div className="rounded-xl border border-slate-800 bg-dark-900 overflow-hidden">
                  <button
                    type="button"
                    onClick={() => setShowHint2(!showHint2)}
                    className="w-full px-3.5 py-2.5 text-left text-xs font-semibold text-slate-300 flex items-center justify-between hover:text-white"
                  >
                    <span>Hint 2: Algorithmic Invariant</span>
                    {showHint2 ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                  </button>
                  {showHint2 && (
                    <div className="px-3.5 pb-3 pt-1 text-xs text-slate-300 leading-relaxed border-t border-slate-800/80 bg-dark-950/50">
                      {result.hint_2}
                    </div>
                  )}
                </div>

                {/* Deeper Explanation */}
                <div className="rounded-xl border border-slate-800 bg-dark-900 overflow-hidden">
                  <button
                    type="button"
                    onClick={() => setShowDeeper(!showDeeper)}
                    className="w-full px-3.5 py-2.5 text-left text-xs font-semibold text-slate-300 flex items-center justify-between hover:text-white"
                  >
                    <span>Deeper Complexity Breakdown</span>
                    {showDeeper ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                  </button>
                  {showDeeper && (
                    <div className="px-3.5 pb-3 pt-1 text-xs text-slate-300 leading-relaxed border-t border-slate-800/80 bg-dark-950/50">
                      {result.deeper_explanation}
                    </div>
                  )}
                </div>

                {/* Optional Optimized Approach */}
                {result.optimized_approach && (
                  <div className="rounded-xl border border-slate-800 bg-dark-900 overflow-hidden">
                    <button
                      type="button"
                      onClick={() => setShowOptimized(!showOptimized)}
                      className="w-full px-3.5 py-2.5 text-left text-xs font-semibold text-brand-400 flex items-center justify-between hover:text-brand-300"
                    >
                      <span>Reveal Optimal Approach</span>
                      {showOptimized ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
                    </button>
                    {showOptimized && (
                      <div className="px-3.5 pb-3 pt-1 text-xs text-slate-200 leading-relaxed border-t border-slate-800/80 bg-dark-950/80">
                        {result.optimized_approach}
                      </div>
                    )}
                  </div>
                )}
              </div>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}
