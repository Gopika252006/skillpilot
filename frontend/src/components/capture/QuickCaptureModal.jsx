import React, { useState } from 'react';
import {
  X, FileText, Upload, Image as ImageIcon, Calculator, Code2, Link as LinkIcon, Sparkles, Loader2
} from 'lucide-react';
import { api } from '../../services/api';
import { useToast } from '../../context/ToastContext';

export default function QuickCaptureModal({ isOpen, onClose, onItemSaved }) {
  const { addToast } = useToast();
  const [activeTab, setActiveTab] = useState('note');
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [topic, setTopic] = useState('General');
  const [folder, setFolder] = useState('Personal Reference');
  const [tags, setTags] = useState('');
  const [file, setFile] = useState(null);
  const [saving, setSaving] = useState(false);

  if (!isOpen) return null;

  const resetForm = () => {
    setTitle('');
    setContent('');
    setTags('');
    setFile(null);
    setTopic('General');
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setSaving(true);
    try {
      if (activeTab === 'file' || activeTab === 'image') {
        if (!file) {
          addToast('Please select a file to upload.', 'error');
          setSaving(false);
          return;
        }
        const formData = new FormData();
        formData.append('file', file);
        formData.append('topic', topic);
        formData.append('folder', folder);
        const saved = await api.uploadVaultFile(formData);
        addToast(`Uploaded and indexed ${saved.title}!`, 'success');
        if (onItemSaved) onItemSaved(saved);
      } else {
        if (!title.trim() || !content.trim()) {
          addToast('Please provide both title and content.', 'error');
          setSaving(false);
          return;
        }
        const tagList = tags.split(',').map((t) => t.trim()).filter(Boolean);
        const itemData = {
          content_type: activeTab,
          title,
          content,
          topic,
          folder,
          tags: tagList,
        };
        const saved = await api.createVaultItem(itemData);
        addToast(`Saved to Knowledge Vault: "${saved.title}"`, 'success');
        if (onItemSaved) onItemSaved(saved);
      }
      resetForm();
      onClose();
    } catch (err) {
      addToast(err.message || 'Failed to save to Knowledge Vault.', 'error');
    } finally {
      setSaving(false);
    }
  };

  const tabs = [
    { id: 'note', label: 'Quick Note', icon: FileText },
    { id: 'code', label: 'Code Snippet', icon: Code2 },
    { id: 'formula', label: 'Formula', icon: Calculator },
    { id: 'link', label: 'Link', icon: LinkIcon },
    { id: 'file', label: 'Upload Doc (PDF/TXT)', icon: Upload },
    { id: 'image', label: 'Upload Diagram', icon: ImageIcon },
  ];

  return (
    <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/80 backdrop-blur-sm animate-fade-in">
      <div className="relative w-full max-w-2xl bg-dark-850 border border-slate-800 rounded-2xl shadow-2xl overflow-hidden">
        {/* Header */}
        <div className="flex items-center justify-between px-6 py-4 border-b border-slate-800 bg-dark-900/60">
          <div className="flex items-center gap-2.5">
            <div className="p-2 rounded-lg bg-brand-500/10 text-brand-400">
              <Sparkles className="w-5 h-5" />
            </div>
            <div>
              <h2 className="text-base font-semibold text-white">Quick Capture to Knowledge Vault</h2>
              <p className="text-xs text-slate-400">Save anything you studied outside CodePilot in seconds</p>
            </div>
          </div>
          <button
            onClick={onClose}
            className="p-1.5 text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
          >
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Tab selection */}
        <div className="flex border-b border-slate-800/80 px-6 overflow-x-auto gap-2 bg-dark-900/30 py-2.5">
          {tabs.map((tab) => {
            const Icon = tab.icon;
            const isSelected = activeTab === tab.id;
            return (
              <button
                key={tab.id}
                type="button"
                onClick={() => setActiveTab(tab.id)}
                className={`flex items-center gap-2 px-3 py-1.5 rounded-lg text-xs font-medium whitespace-nowrap transition-all ${
                  isSelected
                    ? 'bg-brand-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-slate-200 hover:bg-slate-800/60'
                }`}
              >
                <Icon className="w-3.5 h-3.5" />
                {tab.label}
              </button>
            );
          })}
        </div>

        {/* Capture Form */}
        <form onSubmit={handleSubmit} className="p-6 space-y-4">
          {activeTab !== 'file' && activeTab !== 'image' ? (
            <>
              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">Title</label>
                <input
                  type="text"
                  placeholder={
                    activeTab === 'formula'
                      ? 'e.g. Master Theorem Complexity Recurrence'
                      : activeTab === 'code'
                      ? 'e.g. Monotonic Deque Sliding Window Max'
                      : activeTab === 'link'
                      ? 'e.g. Kafka Consumer Lag Architecture Docs'
                      : 'e.g. JWT Token Invalidation with Redis Bloom Filter'
                  }
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  className="w-full px-3.5 py-2.5 bg-dark-900 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-colors"
                  required
                />
              </div>

              <div>
                <label className="block text-xs font-medium text-slate-300 mb-1">
                  {activeTab === 'code'
                    ? 'Code'
                    : activeTab === 'formula'
                    ? 'Mathematical Notation / Recurrence'
                    : activeTab === 'link'
                    ? 'URL & Overview'
                    : 'Content / Notes'}
                </label>
                <textarea
                  rows={activeTab === 'code' ? 7 : 4}
                  placeholder={
                    activeTab === 'formula'
                      ? 'T(n) = 2*T(n/2) + O(n)\nFormula: Theta(n log n)'
                      : activeTab === 'code'
                      ? 'def sliding_window(arr, k):\n    ...'
                      : activeTab === 'link'
                      ? 'https://example.com/system-design\nKey takeaways: Write-through cache minimizes stale reads.'
                      : 'Write or paste your technical takeaways here...'
                  }
                  value={content}
                  onChange={(e) => setContent(e.target.value)}
                  className={`w-full px-3.5 py-2.5 bg-dark-900 border border-slate-800 rounded-xl text-sm text-white placeholder-slate-500 focus:outline-none focus:border-brand-500 focus:ring-1 focus:ring-brand-500 transition-colors ${
                    activeTab === 'code' || activeTab === 'formula' ? 'code-font text-xs' : ''
                  }`}
                  required
                />
              </div>
            </>
          ) : (
            <div>
              <label className="block text-xs font-medium text-slate-300 mb-1">
                {activeTab === 'file' ? 'Upload Document (PDF, TXT, MD)' : 'Upload Diagram / Screenshot'}
              </label>
              <div className="relative border-2 border-dashed border-slate-700 hover:border-brand-500/60 rounded-xl p-6 text-center transition-colors bg-dark-900/40">
                <input
                  type="file"
                  accept={activeTab === 'file' ? '.pdf,.txt,.md' : '.png,.jpg,.jpeg,.webp'}
                  onChange={(e) => setFile(e.target.files[0] || null)}
                  className="absolute inset-0 w-full h-full opacity-0 cursor-pointer"
                  required
                />
                <div className="flex flex-col items-center justify-center gap-2">
                  <div className="p-3 bg-brand-500/10 text-brand-400 rounded-xl">
                    <Upload className="w-6 h-6" />
                  </div>
                  {file ? (
                    <div>
                      <p className="text-sm font-medium text-emerald-400">{file.name}</p>
                      <p className="text-xs text-slate-400">{(file.size / 1024).toFixed(1)} KB selected</p>
                    </div>
                  ) : (
                    <div>
                      <p className="text-sm font-medium text-slate-200">
                        Drop your {activeTab === 'file' ? 'PDF or Markdown notes' : 'technical diagram/screenshot'} here
                      </p>
                      <p className="text-xs text-slate-500 mt-1">AI will automatically index text and extract technical concepts</p>
                    </div>
                  )}
                </div>
              </div>
            </div>
          )}

          {/* Categorization & Metadata */}
          <div className="grid grid-cols-1 sm:grid-cols-3 gap-3 pt-1">
            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Folder</label>
              <select
                value={folder}
                onChange={(e) => setFolder(e.target.value)}
                className="w-full px-3 py-2 bg-dark-900 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-brand-500"
              >
                <option value="DSA">DSA</option>
                <option value="Backend">Backend</option>
                <option value="System Design">System Design</option>
                <option value="AI & ML">AI & ML</option>
                <option value="College">College</option>
                <option value="Interview Prep">Interview Prep</option>
                <option value="Personal Reference">Personal Reference</option>
              </select>
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Topic</label>
              <input
                type="text"
                placeholder="e.g. Distributed Systems"
                value={topic}
                onChange={(e) => setTopic(e.target.value)}
                className="w-full px-3 py-2 bg-dark-900 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-brand-500"
              />
            </div>

            <div>
              <label className="block text-xs font-medium text-slate-400 mb-1">Tags (comma-separated)</label>
              <input
                type="text"
                placeholder="e.g. jwt, auth, security"
                value={tags}
                onChange={(e) => setTags(e.target.value)}
                className="w-full px-3 py-2 bg-dark-900 border border-slate-800 rounded-lg text-xs text-slate-200 focus:outline-none focus:border-brand-500"
              />
            </div>
          </div>

          {/* Action buttons */}
          <div className="flex items-center justify-end gap-3 pt-3 border-t border-slate-800">
            <button
              type="button"
              onClick={onClose}
              className="px-4 py-2 text-xs font-medium text-slate-400 hover:text-white rounded-lg hover:bg-slate-800 transition-colors"
            >
              Cancel
            </button>
            <button
              type="submit"
              disabled={saving}
              className="flex items-center gap-2 px-5 py-2 bg-brand-600 hover:bg-brand-500 disabled:opacity-50 text-white rounded-lg text-xs font-medium shadow-md transition-all shadow-brand-500/20"
            >
              {saving ? (
                <>
                  <Loader2 className="w-3.5 h-3.5 animate-spin" />
                  Saving & Indexing...
                </>
              ) : (
                <>
                  <Sparkles className="w-3.5 h-3.5" />
                  Save to Vault
                </>
              )}
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}
