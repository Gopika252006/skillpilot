import React, { useState, useEffect } from 'react';
import {
  Layers,
  CheckCircle2,
  AlertCircle,
  Clock,
  ArrowRight,
  TrendingUp,
  RotateCcw,
  Sparkles,
  Loader2
} from 'lucide-react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';

export default function Aptitude() {
  const { addToast } = useToast();
  const [questions, setQuestions] = useState([]);
  const [currentIndex, setCurrentIndex] = useState(0);
  const [selectedOption, setSelectedOption] = useState(null);
  const [answered, setAnswered] = useState(false);
  const [result, setResult] = useState(null);
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);

  const fetchSprint = async () => {
    setLoading(true);
    try {
      const [qData, sData] = await Promise.all([
        api.getAptitudeSprint(),
        api.getAptitudeStats()
      ]);
      setQuestions(qData);
      setStats(sData);
    } catch (err) {
      addToast('Failed to load daily aptitude sprint.', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchSprint();
  }, []);

  const handleOptionSelect = (idx) => {
    if (answered) return;
    setSelectedOption(idx);
  };

  const handleVerify = async () => {
    if (selectedOption === null) {
      addToast('Please select an option first.', 'error');
      return;
    }
    setSubmitting(true);
    try {
      const res = await api.submitAptitudeAttempt(currentIndex, selectedOption, 35);
      setResult(res);
      setAnswered(true);
      if (res.is_correct) {
        addToast('Correct! Great analytical reasoning.', 'success');
      } else {
        addToast('Incorrect. Check the explanation below.', 'error');
      }
      const updatedStats = await api.getAptitudeStats();
      setStats(updatedStats);
    } catch (err) {
      addToast('Error verifying answer: ' + err.message, 'error');
    } finally {
      setSubmitting(false);
    }
  };

  const handleNext = () => {
    if (currentIndex < questions.length - 1) {
      setCurrentIndex((prev) => prev + 1);
      setSelectedOption(null);
      setAnswered(false);
      setResult(null);
    }
  };

  const currentQ = questions[currentIndex];

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              <Layers className="w-6 h-6 text-brand-400" />
              Aptitude Sprint
            </h1>
            <span className="text-[10px] uppercase tracking-wider font-extrabold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              5 Daily Placement Qs
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Maintain placement & online test sharpness without bloated prep. Daily micro-sprints for Quant, Logic, and Verbal reasoning.
          </p>
        </div>

        {/* Stats Pill */}
        {stats && (
          <div className="flex items-center gap-4 px-4 py-2 bg-dark-850 rounded-xl border border-slate-800 shrink-0 text-xs">
            <div>
              <span className="text-slate-500">Solved:</span>{' '}
              <strong className="text-white">{stats.total_attempts}</strong>
            </div>
            <div>
              <span className="text-slate-500">Accuracy:</span>{' '}
              <strong className="text-emerald-400">{stats.accuracy}%</strong>
            </div>
          </div>
        )}
      </div>

      {loading ? (
        <div className="p-12 text-center text-slate-400 flex flex-col items-center justify-center">
          <Loader2 className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mb-3" />
          <p className="text-xs">Loading aptitude questions...</p>
        </div>
      ) : currentQ ? (
        <div className="space-y-5">
          {/* Question Card */}
          <div className="p-6 md:p-8 rounded-2xl bg-dark-850 border border-slate-800 shadow-xl space-y-6">
            <div className="flex items-center justify-between">
              <div className="flex items-center gap-2">
                <span className="text-xs font-bold uppercase tracking-wider text-brand-400">
                  Question {currentIndex + 1} of {questions.length}
                </span>
                <span className="text-[11px] font-semibold px-2.5 py-0.5 rounded bg-dark-900 text-slate-300 border border-slate-800">
                  {currentQ.category}
                </span>
              </div>
            </div>

            <h3 className="text-sm sm:text-base font-semibold text-white leading-relaxed">{currentQ.question}</h3>

            {/* Options */}
            <div className="space-y-3 pt-2">
              {currentQ.options?.map((opt, idx) => {
                const isSelected = selectedOption === idx;
                const isCorrect = answered && idx === result?.correct_option;
                const isWrong = answered && isSelected && !result?.is_correct;

                return (
                  <div
                    key={idx}
                    onClick={() => handleOptionSelect(idx)}
                    className={`p-4 rounded-xl border text-xs sm:text-sm transition-all cursor-pointer flex items-center justify-between ${
                      isCorrect
                        ? 'bg-emerald-500/15 border-emerald-500 text-emerald-200 font-medium'
                        : isWrong
                        ? 'bg-rose-500/15 border-rose-500 text-rose-200 line-through'
                        : isSelected
                        ? 'bg-brand-600/20 border-brand-500 text-white font-medium'
                        : 'bg-dark-900 border-slate-800 hover:border-slate-700 text-slate-300'
                    }`}
                  >
                    <div className="flex items-center gap-3">
                      <span className="w-6 h-6 rounded-full border flex items-center justify-center text-xs font-mono shrink-0">
                        {String.fromCharCode(65 + idx)}
                      </span>
                      <span>{opt}</span>
                    </div>
                    {isCorrect && <CheckCircle2 className="w-4 h-4 text-emerald-400 shrink-0" />}
                    {isWrong && <AlertCircle className="w-4 h-4 text-rose-400 shrink-0" />}
                  </div>
                );
              })}
            </div>

            {/* Explanation box */}
            {answered && result && (
              <div className="p-4 rounded-xl bg-dark-900 border border-slate-800 space-y-1.5 text-xs animate-fade-in">
                <span className="font-bold text-brand-300 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5" />
                  Solution & Logical Step:
                </span>
                <p className="text-slate-300 leading-relaxed">{result.explanation}</p>
              </div>
            )}

            {/* Actions */}
            <div className="flex items-center justify-between pt-4 border-t border-slate-800">
              <span className="text-xs text-slate-500">
                Placement tests evaluate both speed & accuracy.
              </span>

              {!answered ? (
                <button
                  onClick={handleVerify}
                  disabled={submitting || selectedOption === null}
                  className="px-6 py-2.5 bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white rounded-xl text-xs font-semibold shadow-md transition-all"
                >
                  {submitting ? 'Checking...' : 'Check Answer'}
                </button>
              ) : currentIndex < questions.length - 1 ? (
                <button
                  onClick={handleNext}
                  className="flex items-center gap-1.5 px-6 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold shadow-md transition-all"
                >
                  <span>Next Question</span>
                  <ArrowRight className="w-4 h-4" />
                </button>
              ) : (
                <span className="text-xs font-semibold text-emerald-400 flex items-center gap-1">
                  <CheckCircle2 className="w-4 h-4" />
                  Daily Sprint Completed!
                </span>
              )}
            </div>
          </div>
        </div>
      ) : null}
    </div>
  );
}
