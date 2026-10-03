import React, { useState, useEffect } from 'react';
import {
  Award,
  CheckCircle2,
  AlertCircle,
  HelpCircle,
  ArrowRight,
  Sparkles,
  TrendingUp,
  RefreshCw,
  Loader2
} from 'lucide-react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';

export default function Assessment() {
  const { addToast } = useToast();
  const [assessment, setAssessment] = useState(null);
  const [loading, setLoading] = useState(true);
  const [selectedAnswers, setSelectedAnswers] = useState({});
  const [submitting, setSubmitting] = useState(false);

  const fetchAssessment = async () => {
    setLoading(true);
    try {
      const data = await api.getCurrentAssessment();
      setAssessment(data);
      if (data.user_answers) {
        setSelectedAnswers(data.user_answers);
      }
    } catch (err) {
      addToast('Failed to load weekend assessment.', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchAssessment();
  }, []);

  const handleSelectOption = (questionId, optionIndex) => {
    if (assessment?.status === 'COMPLETED') return;
    setSelectedAnswers((prev) => ({
      ...prev,
      [String(questionId)]: optionIndex
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!assessment) return;

    const unanswered = assessment.questions.some(
      (q, idx) => selectedAnswers[String(q.id || idx)] === undefined
    );

    if (unanswered) {
      if (!window.confirm('Some questions are unanswered. Do you want to submit anyway?')) return;
    }

    setSubmitting(true);
    try {
      const result = await api.submitAssessment(assessment.id, selectedAnswers);
      setAssessment(result);
      addToast(`Assessment completed! Score: ${result.score}%. Knowledge Memory updated.`, 'success');
    } catch (err) {
      addToast('Failed to submit assessment: ' + err.message, 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const isCompleted = assessment?.status === 'COMPLETED';

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              <Award className="w-6 h-6 text-brand-400" />
              Weekend Adaptive Assessment
            </h1>
            <span
              className={`text-[10px] uppercase tracking-wider font-extrabold px-2 py-0.5 rounded-full border ${
                isCompleted
                  ? 'bg-emerald-500/20 text-emerald-300 border-emerald-500/30'
                  : 'bg-amber-500/20 text-amber-300 border-amber-500/30'
              }`}
            >
              {isCompleted ? 'Completed' : 'Pending Test'}
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Measures mastery over this week's practice concepts. Verified results feed into Personal Technical Memory to adapt next week's plan.
          </p>
        </div>
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400 flex flex-col items-center justify-center">
          <Loader2 className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mb-3" />
          <p className="text-xs">Preparing adaptive assessment...</p>
        </div>
      ) : assessment ? (
        <div className="space-y-6">
          {/* Assessment Score / Result Banner if completed */}
          {isCompleted && (
            <div className="p-6 rounded-2xl bg-dark-850 border border-slate-800 shadow-xl space-y-4 animate-fade-in">
              <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 border-b border-slate-800 pb-4">
                <div>
                  <span className="text-xs font-semibold text-emerald-400 uppercase tracking-wider">Outcome Verified</span>
                  <h2 className="text-2xl font-extrabold text-white mt-0.5">
                    Score: {assessment.score}%
                  </h2>
                  <p className="text-xs text-slate-300 mt-1">{assessment.feedback_summary}</p>
                </div>

                <div className="p-3 bg-emerald-500/10 border border-emerald-500/20 rounded-xl text-xs text-emerald-300 flex items-center gap-2">
                  <CheckCircle2 className="w-5 h-5 text-emerald-400 shrink-0" />
                  <span>Personal Technical Memory Updated with verified test evidence</span>
                </div>
              </div>

              {/* Strong vs Weak breakdown */}
              <div className="grid grid-cols-1 sm:grid-cols-2 gap-4">
                <div className="p-4 rounded-xl bg-dark-900 border border-slate-800 space-y-2">
                  <span className="text-xs font-bold text-emerald-400 flex items-center gap-1.5">
                    <CheckCircle2 className="w-3.5 h-3.5" />
                    Verified Strengths
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {assessment.strong_areas?.map((item, idx) => (
                      <span key={idx} className="px-2 py-0.5 rounded bg-emerald-500/15 text-emerald-300 text-xs">
                        {item}
                      </span>
                    ))}
                  </div>
                </div>

                <div className="p-4 rounded-xl bg-dark-900 border border-slate-800 space-y-2">
                  <span className="text-xs font-bold text-rose-400 flex items-center gap-1.5">
                    <AlertCircle className="w-3.5 h-3.5" />
                    Concepts Requiring Revision
                  </span>
                  <div className="flex flex-wrap gap-1.5">
                    {assessment.weak_areas?.map((item, idx) => (
                      <span key={idx} className="px-2 py-0.5 rounded bg-rose-500/15 text-rose-300 text-xs">
                        {item}
                      </span>
                    ))}
                  </div>
                </div>
              </div>

              {/* Next week recommendations */}
              {assessment.next_week_recommendations?.length > 0 && (
                <div className="p-4 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-xs space-y-1.5">
                  <span className="font-bold text-indigo-300">Adaptive Recommendations for Next Week:</span>
                  <ul className="list-disc pl-5 text-indigo-200/90 space-y-1">
                    {assessment.next_week_recommendations.map((rec, idx) => (
                      <li key={idx}>{rec}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          )}

          {/* Questions Form */}
          <form onSubmit={handleSubmit} className="space-y-5">
            {assessment.questions?.map((q, qIndex) => {
              const qId = String(q.id || qIndex);
              const selectedOpt = selectedAnswers[qId];
              const isAnswered = selectedOpt !== undefined;

              return (
                <div key={qId} className="p-6 rounded-2xl bg-dark-850 border border-slate-800 space-y-4 shadow-lg">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold uppercase tracking-wider text-brand-400">
                      Question {qIndex + 1}
                    </span>
                    <span className="text-[10px] font-medium px-2 py-0.5 rounded bg-dark-900 text-slate-400 border border-slate-800">
                      {q.topic}
                    </span>
                  </div>

                  <h3 className="text-sm sm:text-base font-semibold text-white leading-relaxed">{q.question}</h3>

                  {/* Options List */}
                  <div className="space-y-2 pt-1">
                    {q.options?.map((option, optIdx) => {
                      const isSelected = Number(selectedOpt) === optIdx;
                      const isCorrect = isCompleted && optIdx === q.correct_option;
                      const isWrongSelected = isCompleted && isSelected && !isCorrect;

                      return (
                        <div
                          key={optIdx}
                          onClick={() => handleSelectOption(qId, optIdx)}
                          className={`p-3.5 rounded-xl border text-xs sm:text-sm transition-all cursor-pointer flex items-center justify-between ${
                            isCorrect
                              ? 'bg-emerald-500/15 border-emerald-500/50 text-emerald-200 font-medium'
                              : isWrongSelected
                              ? 'bg-rose-500/15 border-rose-500/50 text-rose-200 line-through'
                              : isSelected
                              ? 'bg-brand-600/20 border-brand-500/60 text-white font-medium'
                              : 'bg-dark-900 border-slate-800/90 hover:border-slate-700 text-slate-300'
                          }`}
                        >
                          <div className="flex items-center gap-3">
                            <span className="w-5 h-5 rounded-full border flex items-center justify-center text-[10px] font-mono shrink-0">
                              {String.fromCharCode(65 + optIdx)}
                            </span>
                            <span>{option}</span>
                          </div>
                          {isCorrect && <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />}
                          {isWrongSelected && <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />}
                        </div>
                      );
                    })}
                  </div>

                  {/* Explanation if completed */}
                  {isCompleted && q.explanation && (
                    <div className="p-3 rounded-xl bg-dark-900 border border-slate-800/80 text-xs text-slate-400 leading-relaxed">
                      <strong className="text-slate-300">Explanation:</strong> {q.explanation}
                    </div>
                  )}
                </div>
              );
            })}

            {!isCompleted && (
              <div className="flex justify-end pt-2">
                <button
                  type="submit"
                  disabled={submitting}
                  className="flex items-center gap-2 px-8 py-3 bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white rounded-xl text-sm font-semibold shadow-lg shadow-brand-500/25 transition-all hover:scale-[1.02]"
                >
                  {submitting ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Evaluating Answers...
                    </>
                  ) : (
                    <>
                      <span>Submit Weekend Assessment</span>
                      <ArrowRight className="w-4 h-4" />
                    </>
                  )}
                </button>
              </div>
            )}
          </form>
        </div>
      ) : null}
    </div>
  );
}
