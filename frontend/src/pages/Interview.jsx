import React, { useState } from 'react';
import {
  UserCheck,
  Sparkles,
  Send,
  MessageSquare,
  Award,
  CheckCircle2,
  ChevronRight,
  Loader2
} from 'lucide-react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';

export default function Interview() {
  const { addToast } = useToast();
  const [session, setSession] = useState(null);
  const [currentQuestion, setCurrentQuestion] = useState(null);
  const [userAnswer, setUserAnswer] = useState('');
  const [feedbackHistory, setFeedbackHistory] = useState([]);
  const [starting, setStarting] = useState(false);
  const [submitting, setSubmitting] = useState(false);
  const [completed, setCompleted] = useState(false);

  const handleStart = async () => {
    setStarting(true);
    setCompleted(false);
    setFeedbackHistory([]);
    try {
      const data = await api.startInterview('DSA & Backend Architecture');
      setSession(data);
      setCurrentQuestion(data.first_question);
      addToast('Interview session started! Answer thoroughly to demonstrate depth.', 'info');
    } catch (err) {
      addToast('Failed to start interview: ' + err.message, 'error');
    } finally {
      setStarting(false);
    }
  };

  const handleAnswerSubmit = async (e) => {
    e.preventDefault();
    if (!userAnswer.trim() || !session || !currentQuestion) return;

    setSubmitting(true);
    try {
      const res = await api.submitInterviewAnswer(
        session.session_id,
        currentQuestion.question_number,
        userAnswer
      );

      setFeedbackHistory((prev) => [
        ...prev,
        {
          qNum: currentQuestion.question_number,
          question: currentQuestion.question,
          answer: userAnswer,
          score: res.score,
          feedback: res.feedback,
          followUp: res.follow_up_question
        }
      ]);

      setUserAnswer('');

      if (res.is_completed) {
        setCompleted(true);
        addToast('Interview session completed! Review your feedback below.', 'success');
      } else if (res.next_question) {
        setCurrentQuestion({
          question_number: res.question_number + 1,
          question: res.next_question
        });
      }
    } catch (err) {
      addToast('Failed to evaluate answer: ' + err.message, 'error');
    } finally {
      setSubmitting(false);
    }
  };

  return (
    <div className="space-y-6 max-w-4xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              <UserCheck className="w-6 h-6 text-brand-400" />
              Adaptive Interview Practice
            </h1>
            <span className="text-[10px] uppercase tracking-wider font-extrabold px-2 py-0.5 rounded-full bg-indigo-500/20 text-indigo-300 border border-indigo-500/30">
              Verbal Reasoning Validation
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            "Can you explain what you claim to know?" Validates technical reasoning, depth, and handling of architectural trade-offs.
          </p>
        </div>
      </div>

      {!session ? (
        <div className="p-8 md:p-12 rounded-2xl bg-dark-850 border border-slate-800 text-center flex flex-col items-center justify-center space-y-4 shadow-xl">
          <div className="w-14 h-14 rounded-2xl bg-brand-500/10 border border-brand-500/20 text-brand-400 flex items-center justify-center mb-2">
            <UserCheck className="w-7 h-7" />
          </div>
          <h2 className="text-xl font-bold text-white">Start Adaptive Technical Interview</h2>
          <p className="text-xs text-slate-400 max-w-md leading-relaxed">
            The AI interviewer will ask 3 targeted questions tailored to your <strong>Backend Software Engineer</strong> profile and recent weak concepts.
          </p>
          <button
            onClick={handleStart}
            disabled={starting}
            className="flex items-center gap-2 px-6 py-3 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold shadow-lg shadow-brand-500/25 transition-all hover:scale-105"
          >
            {starting ? <Loader2 className="w-4 h-4 animate-spin" /> : <Sparkles className="w-4 h-4" />}
            <span>Begin Mock Session</span>
          </button>
        </div>
      ) : (
        <div className="space-y-6">
          {/* Question / Interview Flow */}
          {!completed && currentQuestion && (
            <form onSubmit={handleAnswerSubmit} className="p-6 md:p-8 rounded-2xl bg-dark-850 border border-slate-800 space-y-5 shadow-xl">
              <div className="flex items-center justify-between border-b border-slate-800 pb-3">
                <span className="text-xs font-bold uppercase tracking-wider text-brand-400">
                  Question {currentQuestion.question_number} of 3
                </span>
                <span className="text-[11px] text-slate-400 font-medium">Topic: {session.topic}</span>
              </div>

              <div className="p-4 rounded-xl bg-dark-900 border border-slate-800/80">
                <h3 className="text-sm sm:text-base font-semibold text-white leading-relaxed">
                  "{currentQuestion.question}"
                </h3>
              </div>

              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1.5">
                  Your Answer (Explain your reasoning, Big-O trade-offs, and design choices):
                </label>
                <textarea
                  rows={6}
                  value={userAnswer}
                  onChange={(e) => setUserAnswer(e.target.value)}
                  placeholder="In a B+ Tree, leaf nodes form a contiguous doubly-linked list which optimizes range queries..."
                  className="w-full p-4 bg-dark-950 border border-slate-800 rounded-xl text-xs sm:text-sm text-slate-200 placeholder-slate-600 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 leading-relaxed"
                  required
                />
              </div>

              <div className="flex justify-end pt-2">
                <button
                  type="submit"
                  disabled={submitting || !userAnswer.trim()}
                  className="flex items-center gap-2 px-6 py-2.5 bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white rounded-xl text-xs font-semibold shadow-md shadow-brand-500/25 transition-all"
                >
                  {submitting ? (
                    <>
                      <Loader2 className="w-4 h-4 animate-spin" />
                      Evaluating Technical Depth...
                    </>
                  ) : (
                    <>
                      <span>Submit Answer & Get Feedback</span>
                      <Send className="w-3.5 h-3.5" />
                    </>
                  )}
                </button>
              </div>
            </form>
          )}

          {/* Completed Outcome */}
          {completed && (
            <div className="p-6 md:p-8 rounded-2xl bg-dark-850 border border-slate-800 space-y-4 shadow-xl animate-fade-in">
              <div className="flex items-center gap-2 text-emerald-400">
                <CheckCircle2 className="w-6 h-6" />
                <h2 className="text-xl font-bold text-white">Interview Session Completed</h2>
              </div>
              <p className="text-xs text-slate-300">
                Your technical explanations were evaluated for correctness, clarity, and trade-off depth.
              </p>
              <button
                onClick={handleStart}
                className="mt-2 px-5 py-2 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold transition-all"
              >
                Start Another Session
              </button>
            </div>
          )}

          {/* Feedback & History of Exchanges */}
          {feedbackHistory.length > 0 && (
            <div className="space-y-4 pt-4 border-t border-slate-800">
              <h3 className="text-sm font-bold uppercase tracking-wider text-slate-400">
                Evaluation & Follow-up History
              </h3>
              {feedbackHistory.map((item, idx) => (
                <div key={idx} className="p-5 rounded-2xl bg-dark-850 border border-slate-800 space-y-3 shadow-md">
                  <div className="flex items-center justify-between">
                    <span className="text-xs font-bold text-brand-400">Question {item.qNum}</span>
                    <span className="px-2.5 py-0.5 rounded-full text-[10px] font-bold bg-emerald-500/10 text-emerald-400 border border-emerald-500/20">
                      Score: {item.score}/10
                    </span>
                  </div>

                  <p className="text-xs font-semibold text-white">"{item.question}"</p>

                  <div className="p-3 rounded-xl bg-dark-900 border border-slate-800/80 text-xs text-slate-300">
                    <strong className="text-slate-400">Your Answer:</strong> {item.answer}
                  </div>

                  <div className="p-3 rounded-xl bg-indigo-500/10 border border-indigo-500/20 text-xs text-indigo-200 leading-relaxed">
                    <strong className="text-indigo-300">AI Evaluation:</strong> {item.feedback}
                  </div>

                  {item.followUp && (
                    <div className="p-3 rounded-xl bg-amber-500/10 border border-amber-500/20 text-xs text-amber-200">
                      <strong className="text-amber-300">Suggested Follow-up:</strong> {item.followUp}
                    </div>
                  )}
                </div>
              ))}
            </div>
          )}
        </div>
      )}
    </div>
  );
}
