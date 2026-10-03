import React, { useState, useEffect } from 'react';
import {
  Archive,
  Search,
  Plus,
  FileText,
  Upload,
  Code2,
  Calculator,
  Link as LinkIcon,
  Star,
  Sparkles,
  MessageSquare,
  Trash2,
  Filter,
  Layers,
  HelpCircle,
  ExternalLink,
  BookOpen,
  Folder,
  Send,
  Loader2,
  X
} from 'lucide-react';
import { api } from '../services/api';
import { useToast } from '../context/ToastContext';
import QuickCaptureModal from '../components/capture/QuickCaptureModal';

export default function KnowledgeVault() {
  const { addToast } = useToast();
  const [items, setItems] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedType, setSelectedType] = useState('all');
  const [selectedFolder, setSelectedFolder] = useState('all');
  const [showFavoritesOnly, setShowFavoritesOnly] = useState(false);

  const [captureOpen, setCaptureOpen] = useState(false);

  // "Ask This" modal state
  const [askingItem, setAskingItem] = useState(null);
  const [askQuestion, setAskQuestion] = useState('');
  const [askLoading, setAskLoading] = useState(false);
  const [askResult, setAskResult] = useState(null);

  // AI Study action modal state
  const [actionItem, setActionItem] = useState(null);
  const [actionType, setActionType] = useState('summarize');
  const [actionLoading, setActionLoading] = useState(false);
  const [actionResult, setActionResult] = useState(null);

  const fetchItems = async () => {
    setLoading(true);
    try {
      const params = {};
      if (selectedType !== 'all') params.contentType = selectedType;
      if (selectedFolder !== 'all') params.folder = selectedFolder;
      if (showFavoritesOnly) params.isFavorite = true;
      if (search.trim()) params.search = search.trim();

      const data = await api.getVaultItems(params);
      setItems(data);
    } catch (err) {
      addToast('Failed to load Knowledge Vault items.', 'error');
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchItems();
  }, [selectedType, selectedFolder, showFavoritesOnly]);

  const handleSearchSubmit = (e) => {
    e.preventDefault();
    fetchItems();
  };

  const handleToggleFavorite = async (item) => {
    try {
      const updated = await api.updateVaultItem(item.id, { is_favorite: !item.is_favorite });
      setItems((prev) => prev.map((i) => (i.id === item.id ? { ...i, is_favorite: updated.is_favorite } : i)));
    } catch (err) {
      addToast('Failed to update favorite status.', 'error');
    }
  };

  const handleDeleteItem = async (itemId) => {
    if (!window.confirm('Are you sure you want to remove this item from your Knowledge Vault?')) return;
    try {
      await api.deleteVaultItem(itemId);
      setItems((prev) => prev.filter((i) => i.id !== itemId));
      addToast('Item removed from Knowledge Vault.', 'info');
    } catch (err) {
      addToast('Failed to delete item.', 'error');
    }
  };

  const handleAskSubmit = async (e) => {
    e.preventDefault();
    if (!askQuestion.trim() || !askingItem) return;
    setAskLoading(true);
    setAskResult(null);
    try {
      const resp = await api.askVaultItem(askingItem.id, askQuestion);
      setAskResult(resp);
    } catch (err) {
      addToast('Error querying document: ' + err.message, 'error');
    } finally {
      setAskLoading(false);
    }
  };

  const handleRunAction = async (item, action) => {
    setActionItem(item);
    setActionType(action);
    setActionLoading(true);
    setActionResult(null);
    try {
      const res = await api.runVaultAction(action, item.content);
      setActionResult(res.result);
    } catch (err) {
      addToast('AI action failed: ' + err.message, 'error');
    } finally {
      setActionLoading(false);
    }
  };

  const typeTabs = [
    { id: 'all', label: 'All Items' },
    { id: 'note', label: 'Notes', icon: FileText },
    { id: 'document', label: 'Documents', icon: Upload },
    { id: 'formula', label: 'Formulas', icon: Calculator },
    { id: 'code', label: 'Code Snippets', icon: Code2 },
    { id: 'link', label: 'Links', icon: LinkIcon },
  ];

  return (
    <div className="space-y-6 max-w-7xl mx-auto">
      {/* Top Header */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 pb-2 border-b border-slate-800">
        <div>
          <div className="flex items-center gap-2">
            <h1 className="text-2xl font-bold tracking-tight text-white flex items-center gap-2">
              <Archive className="w-6 h-6 text-brand-400" />
              Knowledge Vault
            </h1>
            <span className="text-[10px] uppercase tracking-wider font-extrabold px-2 py-0.5 rounded-full bg-emerald-500/20 text-emerald-300 border border-emerald-500/30">
              Personal Second Brain
            </span>
          </div>
          <p className="text-xs text-slate-400 mt-1">
            "Whenever you learn outside CodePilot, capture it here." Never lose notes, formulas, PDFs, or reusable patterns again.
          </p>
        </div>

        <button
          onClick={() => setCaptureOpen(true)}
          className="flex items-center gap-2 px-4 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold shadow-lg shadow-brand-500/20 transition-all hover:scale-[1.02] shrink-0"
        >
          <Plus className="w-4 h-4" />
          + Add to Knowledge Vault
        </button>
      </div>

      {/* Search & Filter Toolbar */}
      <div className="flex flex-col md:flex-row items-stretch md:items-center justify-between gap-3 bg-dark-850 p-3 rounded-2xl border border-slate-800">
        <form onSubmit={handleSearchSubmit} className="flex-1 relative">
          <Search className="w-4 h-4 text-slate-500 absolute left-3.5 top-1/2 -translate-y-1/2" />
          <input
            type="text"
            placeholder="Search notes, formulas, concepts, or documents (keyword & semantic search)..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
            className="w-full pl-9 pr-4 py-2 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
          />
        </form>

        <div className="flex items-center gap-2 overflow-x-auto">
          {/* Folder selector */}
          <select
            value={selectedFolder}
            onChange={(e) => setSelectedFolder(e.target.value)}
            className="px-3 py-2 bg-dark-900 border border-slate-800 rounded-xl text-xs text-slate-300 focus:outline-none focus:border-brand-500"
          >
            <option value="all">All Folders</option>
            <option value="DSA">DSA</option>
            <option value="Backend">Backend</option>
            <option value="System Design">System Design</option>
            <option value="College">College</option>
            <option value="Personal Reference">Personal Reference</option>
          </select>

          {/* Favorite toggle button */}
          <button
            onClick={() => setShowFavoritesOnly(!showFavoritesOnly)}
            className={`flex items-center gap-1.5 px-3 py-2 rounded-xl text-xs font-medium border transition-colors ${
              showFavoritesOnly
                ? 'bg-amber-500/20 border-amber-500/40 text-amber-300'
                : 'bg-dark-900 border-slate-800 text-slate-400 hover:text-slate-200'
            }`}
          >
            <Star className={`w-3.5 h-3.5 ${showFavoritesOnly ? 'fill-current' : ''}`} />
            <span>Favorites</span>
          </button>
        </div>
      </div>

      {/* Content Type Filter Pills */}
      <div className="flex items-center gap-2 overflow-x-auto pb-1">
        {typeTabs.map((tab) => (
          <button
            key={tab.id}
            onClick={() => setSelectedType(tab.id)}
            className={`px-3.5 py-1.5 rounded-xl text-xs font-medium whitespace-nowrap transition-all ${
              selectedType === tab.id
                ? 'bg-brand-600 text-white shadow-sm'
                : 'bg-dark-850 text-slate-400 hover:text-slate-200 hover:bg-dark-800 border border-slate-800/80'
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      {/* Items Grid */}
      {loading ? (
        <div className="p-12 text-center text-slate-400 flex flex-col items-center justify-center">
          <div className="w-8 h-8 border-2 border-brand-500 border-t-transparent rounded-full animate-spin mb-3"></div>
          <p className="text-xs">Loading Knowledge Vault items...</p>
        </div>
      ) : items.length === 0 ? (
        <div className="p-12 text-center rounded-2xl bg-dark-850 border border-slate-800">
          <Archive className="w-10 h-10 text-slate-600 mx-auto mb-3" />
          <h3 className="text-base font-bold text-white mb-1">Knowledge Vault is Empty</h3>
          <p className="text-xs text-slate-400 max-w-sm mx-auto mb-4">
            Save notes, formulas, code snippets, or upload documents to start building your personal technical second brain.
          </p>
          <button
            onClick={() => setCaptureOpen(true)}
            className="px-4 py-2 bg-brand-600 hover:bg-brand-500 text-white text-xs font-semibold rounded-xl"
          >
            + Quick Capture Something
          </button>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-5">
          {items.map((item) => (
            <div
              key={item.id}
              className="p-5 rounded-2xl bg-dark-850 border border-slate-800 hover:border-slate-700 shadow-md flex flex-col justify-between transition-all group"
            >
              <div>
                {/* Card Top: Type badge & favorite button */}
                <div className="flex items-center justify-between mb-3">
                  <div className="flex items-center gap-2">
                    <span className="text-[10px] font-bold uppercase tracking-wider px-2 py-0.5 rounded-md bg-dark-900 border border-slate-800 text-slate-300">
                      {item.content_type}
                    </span>
                    <span className="text-[11px] text-slate-400 flex items-center gap-1">
                      <Folder className="w-3 h-3 text-slate-500" />
                      {item.folder}
                    </span>
                  </div>
                  <div className="flex items-center gap-1">
                    <button
                      onClick={() => handleToggleFavorite(item)}
                      className={`p-1 rounded-md transition-colors ${
                        item.is_favorite ? 'text-amber-400' : 'text-slate-600 hover:text-slate-400'
                      }`}
                    >
                      <Star className={`w-3.5 h-3.5 ${item.is_favorite ? 'fill-current' : ''}`} />
                    </button>
                    <button
                      onClick={() => handleDeleteItem(item.id)}
                      className="p-1 text-slate-600 hover:text-rose-400 rounded-md transition-colors"
                      title="Delete item"
                    >
                      <Trash2 className="w-3.5 h-3.5" />
                    </button>
                  </div>
                </div>

                {/* Title */}
                <h3 className="text-sm font-bold text-white group-hover:text-brand-300 transition-colors line-clamp-1 mb-2">
                  {item.title}
                </h3>

                {/* Content preview */}
                <div
                  className={`text-xs text-slate-300 leading-relaxed mb-4 line-clamp-4 bg-dark-900/60 p-3 rounded-xl border border-slate-800/80 ${
                    item.content_type === 'code' || item.content_type === 'formula' ? 'code-font text-[11px]' : ''
                  }`}
                >
                  {item.content}
                </div>

                {/* Extracted Concepts / Tags */}
                <div className="flex flex-wrap gap-1 mb-4">
                  {item.extracted_concepts?.slice(0, 3).map((concept) => (
                    <span
                      key={concept}
                      className="text-[10px] font-medium px-2 py-0.5 rounded bg-brand-500/10 text-brand-300 border border-brand-500/20"
                    >
                      {concept}
                    </span>
                  ))}
                </div>
              </div>

              {/* Bottom Actions: "Ask This" & "AI Study" */}
              <div className="pt-3 border-t border-slate-800/80 flex items-center justify-between text-xs">
                <button
                  onClick={() => {
                    setAskingItem(item);
                    setAskQuestion('');
                    setAskResult(null);
                  }}
                  className="flex items-center gap-1.5 text-slate-400 hover:text-white font-medium"
                >
                  <MessageSquare className="w-3.5 h-3.5 text-brand-400" />
                  <span>Ask This</span>
                </button>

                <div className="flex items-center gap-2">
                  <button
                    onClick={() => handleRunAction(item, 'summarize')}
                    className="text-[11px] text-slate-400 hover:text-indigo-300 font-medium px-2 py-1 rounded bg-dark-900 hover:bg-dark-800 border border-slate-800"
                  >
                    Summarize
                  </button>
                  <button
                    onClick={() => handleRunAction(item, 'explain')}
                    className="text-[11px] text-slate-400 hover:text-indigo-300 font-medium px-2 py-1 rounded bg-dark-900 hover:bg-dark-800 border border-slate-800"
                  >
                    Explain
                  </button>
                </div>
              </div>
            </div>
          ))}
        </div>
      )}

      {/* "Ask This" Document Modal */}
      {askingItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-xl bg-dark-850 border border-slate-800 rounded-2xl shadow-2xl p-6">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <Sparkles className="w-4 h-4 text-brand-400" />
                  Ask This Document
                </h3>
                <p className="text-xs text-slate-400 truncate max-w-md">Target: {askingItem.title}</p>
              </div>
              <button
                onClick={() => setAskingItem(null)}
                className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            <form onSubmit={handleAskSubmit} className="space-y-4">
              <div>
                <label className="block text-xs font-semibold text-slate-300 mb-1">
                  Ask a question specifically answered by this material
                </label>
                <div className="flex gap-2">
                  <input
                    type="text"
                    placeholder="e.g. How does this implement token revocation?"
                    value={askQuestion}
                    onChange={(e) => setAskQuestion(e.target.value)}
                    className="flex-1 px-3.5 py-2.5 bg-dark-900 border border-slate-800 rounded-xl text-xs text-white placeholder-slate-500 focus:outline-none focus:border-brand-500"
                    required
                  />
                  <button
                    type="submit"
                    disabled={askLoading}
                    className="px-4 py-2.5 bg-brand-600 hover:bg-brand-500 text-white rounded-xl text-xs font-semibold disabled:opacity-50 shrink-0"
                  >
                    {askLoading ? <Loader2 className="w-4 h-4 animate-spin" /> : <Send className="w-4 h-4" />}
                  </button>
                </div>
              </div>
            </form>

            {/* Answer Display */}
            {askResult && (
              <div className="mt-4 p-4 rounded-xl bg-dark-900 border border-slate-800 text-xs text-slate-200 space-y-2 animate-fade-in">
                <div className="font-bold text-brand-300 flex items-center gap-1.5">
                  <Sparkles className="w-3.5 h-3.5" />
                  Grounded Answer:
                </div>
                <div className="leading-relaxed whitespace-pre-wrap">{askResult.answer}</div>
                {askResult.key_quotes?.length > 0 && (
                  <div className="pt-2 border-t border-slate-800/80 mt-2 text-[11px] text-slate-400">
                    <span className="font-semibold text-slate-300">Key Excerpts Found:</span>
                    <ul className="list-disc pl-4 mt-1 space-y-0.5">
                      {askResult.key_quotes.map((quote, qIdx) => (
                        <li key={qIdx} className="italic">
                          "{quote}"
                        </li>
                      ))}
                    </ul>
                  </div>
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* AI Study Action Modal */}
      {actionItem && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
          <div className="relative w-full max-w-xl bg-dark-850 border border-slate-800 rounded-2xl shadow-2xl p-6">
            <div className="flex items-center justify-between pb-3 border-b border-slate-800 mb-4">
              <div>
                <h3 className="text-base font-bold text-white capitalize">{actionType} Material</h3>
                <p className="text-xs text-slate-400 truncate max-w-md">{actionItem.title}</p>
              </div>
              <button
                onClick={() => setActionItem(null)}
                className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800"
              >
                <X className="w-5 h-5" />
              </button>
            </div>

            {actionLoading ? (
              <div className="p-8 text-center text-slate-400 flex flex-col items-center justify-center">
                <Loader2 className="w-6 h-6 animate-spin text-brand-500 mb-2" />
                <p className="text-xs">AI analyzing and synthesizing content...</p>
              </div>
            ) : (
              <div className="p-4 rounded-xl bg-dark-900 border border-slate-800 text-xs text-slate-200 leading-relaxed max-h-96 overflow-y-auto whitespace-pre-wrap">
                {typeof actionResult === 'string' ? (
                  actionResult
                ) : Array.isArray(actionResult) ? (
                  <div className="space-y-3">
                    {actionResult.map((card, idx) => (
                      <div key={idx} className="p-3 bg-dark-850 rounded-lg border border-slate-800 space-y-1">
                        <div className="font-semibold text-brand-300">Q: {card.front}</div>
                        <div className="text-slate-300">A: {card.back}</div>
                      </div>
                    ))}
                  </div>
                ) : (
                  'Done.'
                )}
              </div>
            )}
          </div>
        </div>
      )}

      {/* Quick capture modal */}
      <QuickCaptureModal
        isOpen={captureOpen}
        onClose={() => setCaptureOpen(false)}
        onItemSaved={() => fetchItems()}
      />
    </div>
  );
}
