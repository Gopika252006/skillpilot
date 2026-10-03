import React, { useState } from 'react';
import {
  Compass,
  Sparkles,
  PlusCircle,
  ExternalLink,
  Cpu,
  Layers,
  CheckCircle2,
  BookmarkPlus
} from 'lucide-react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';

const TECHNOLOGIES = [
  {
    id: 'ai-agents',
    title: 'Autonomous AI Agents & Tool Calling',
    category: 'AI / LLM Architecture',
    description: 'Frameworks and architectures enabling LLMs to plan, interact with APIs, and maintain persistent memory states.',
    relevance: 'High demand for Senior Backend & AI platform roles to automate engineering workflows.',
    tags: ['ai-agents', 'mcp', 'function-calling']
  },
  {
    id: 'slm',
    title: 'Small Language Models (SLMs) on Edge',
    category: 'Local Open AI',
    description: 'Sub-4B parameter open-weight models (Llama 3.2 3B, Qwen 2.5 Coder) optimized for fast laptop inference without GPU clusters.',
    relevance: 'Enables private, cost-free technical intelligence running entirely on the developer\'s machine.',
    tags: ['slm', 'ollama', 'open-weights', 'privacy']
  },
  {
    id: 'mcp',
    title: 'Model Context Protocol (MCP)',
    category: 'Developer Tooling & Protocols',
    description: 'An open standard for securely connecting AI assistants to data repositories, IDEs, and local developer environments.',
    relevance: 'Key standard for building connected developer assistants and local tools.',
    tags: ['mcp', 'protocols', 'agentic-ai']
  },
  {
    id: 'pgvector',
    title: 'Vector Embeddings in PostgreSQL (pgvector)',
    category: 'Databases & Search',
    description: 'Extending standard relational PostgreSQL databases with HNSW and IVFFlat index vector search capabilities.',
    relevance: 'Directly applicable to your Backend Software Engineer target role without needing specialized vector DB infrastructure.',
    tags: ['postgresql', 'embeddings', 'vector-search']
  }
];

export default function Explore() {
  const { addToast } = useToast();
  const [addedIds, setAddedIds] = useState([]);

  const handleAddGoal = async (tech) => {
    try {
      const current = await api.getProfile();
      const updatedGoals = `${current.learning_goals}\n- Explore and build prototype with ${tech.title}`;
      const updatedTech = Array.from(new Set([...current.current_technologies, tech.title]));
      await api.updateProfile({
        learning_goals: updatedGoals,
        current_technologies: updatedTech
      });
      setAddedIds((prev) => [...prev, tech.id]);
      addToast(`Added "${tech.title}" to your learning roadmap!`, 'success');
    } catch (err) {
      addToast('Failed to update learning goals: ' + err.message, 'error');
    }
  };

  return (
    <div className="space-y-6 max-w-5xl mx-auto">
      {/* Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              <Compass className="w-6 h-6 text-brand-400" />
              Technology Discovery
            </h1>
            <span className="text-[10px] uppercase tracking-wider font-extrabold px-2 py-0.5 rounded-full bg-brand-500/20 text-brand-300 border border-brand-500/30">
              Curated Roadmap
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            Carefully curated emerging technologies tailored to your backend interests and career target. Not a generic news feed.
          </p>
        </div>
      </div>

      {/* Grid of technologies */}
      <div className="grid grid-cols-1 md:grid-cols-2 gap-5">
        {TECHNOLOGIES.map((tech) => {
          const isAdded = addedIds.includes(tech.id);
          return (
            <div
              key={tech.id}
              className="p-6 rounded-2xl bg-dark-850 border border-slate-800 hover:border-slate-700 shadow-md flex flex-col justify-between transition-all"
            >
              <div>
                <div className="flex items-center justify-between mb-2">
                  <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded bg-dark-900 border border-slate-800 text-slate-400">
                    {tech.category}
                  </span>
                </div>

                <h3 className="text-base font-bold text-white mb-2">{tech.title}</h3>
                <p className="text-xs text-slate-300 leading-relaxed mb-4">{tech.description}</p>

                <div className="p-3 rounded-xl bg-dark-900 border border-slate-800 text-xs text-slate-400 mb-4">
                  <strong className="text-brand-300">Why it matters for you:</strong> {tech.relevance}
                </div>

                <div className="flex flex-wrap gap-1.5 mb-4">
                  {tech.tags.map((tag) => (
                    <span
                      key={tag}
                      className="text-[10px] font-mono px-2 py-0.5 rounded bg-brand-500/10 text-brand-300 border border-brand-500/20"
                    >
                      #{tag}
                    </span>
                  ))}
                </div>
              </div>

              <div className="pt-3 border-t border-slate-800">
                <button
                  type="button"
                  onClick={() => handleAddGoal(tech)}
                  disabled={isAdded}
                  className={`w-full flex items-center justify-center gap-2 py-2 px-3 rounded-xl text-xs font-semibold transition-all ${
                    isAdded
                      ? 'bg-emerald-500/15 border border-emerald-500/30 text-emerald-400'
                      : 'bg-brand-600 hover:bg-brand-500 text-white shadow-sm'
                  }`}
                >
                  {isAdded ? (
                    <>
                      <CheckCircle2 className="w-3.5 h-3.5" />
                      <span>Added to Your Roadmap</span>
                    </>
                  ) : (
                    <>
                      <BookmarkPlus className="w-3.5 h-3.5" />
                      <span>Add to My Learning Goals</span>
                    </>
                  )}
                </button>
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
