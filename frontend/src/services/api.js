const BASE_URL = '/api';

async function request(endpoint, options = {}) {
  const token = localStorage.getItem('codepilot_token');
  const headers = {
    ...options.headers,
  };

  if (token) {
    headers['Authorization'] = `Bearer ${token}`;
  }

  // Do not set Content-Type for FormData
  if (!(options.body instanceof FormData) && !headers['Content-Type']) {
    headers['Content-Type'] = 'application/json';
  }

  const response = await fetch(`${BASE_URL}${endpoint}`, {
    ...options,
    headers,
  });

  if (response.status === 401) {
    // If unauthorized, clear token and redirect to login if not already there
    if (!window.location.pathname.includes('/login') && !window.location.pathname.includes('/register')) {
      localStorage.removeItem('codepilot_token');
      localStorage.removeItem('codepilot_user');
      window.location.href = '/login';
    }
  }

  let data;
  try {
    data = await response.json();
  } catch (err) {
    data = null;
  }

  if (!response.ok) {
    const errorMsg = data?.detail || response.statusText || 'An unexpected error occurred.';
    throw new Error(errorMsg);
  }

  return data;
}

export const api = {
  // Health
  getHealth: () => request('/health', { method: 'GET' }),

  // Auth
  login: (credentials) => request('/auth/login', { method: 'POST', body: JSON.stringify(credentials) }),
  register: (userData) => request('/auth/register', { method: 'POST', body: JSON.stringify(userData) }),
  getMe: () => request('/auth/me', { method: 'GET' }),
  logout: () => request('/auth/logout', { method: 'POST' }),

  // Profile & Onboarding
  getProfile: () => request('/profile', { method: 'GET' }),
  updateProfile: (profile) => request('/profile', { method: 'PUT', body: JSON.stringify(profile) }),

  // Code Analyzer (Hero Feature)
  analyzeCode: (submission) => request('/code/analyze', { method: 'POST', body: JSON.stringify(submission) }),
  getCodeHistory: (limit = 20) => request(`/code/history?limit=${limit}`, { method: 'GET' }),

  // Knowledge Memory & Graph
  getConcepts: () => request('/knowledge/concepts', { method: 'GET' }),
  getKnowledgeGraph: () => request('/knowledge/graph', { method: 'GET' }),
  recordLearningLog: (log) => request('/knowledge/log', { method: 'POST', body: JSON.stringify(log) }),
  getLearningLogs: () => request('/knowledge/logs', { method: 'GET' }),

  // Knowledge Vault (Second Brain)
  getVaultItems: (params = {}) => {
    const query = new URLSearchParams();
    if (params.contentType) query.append('content_type', params.contentType);
    if (params.folder) query.append('folder', params.folder);
    if (params.topic) query.append('topic', params.topic);
    if (params.isFavorite !== undefined) query.append('is_favorite', params.isFavorite);
    if (params.search) query.append('search', params.search);
    return request(`/vault/items?${query.toString()}`, { method: 'GET' });
  },
  createVaultItem: (item) => request('/vault/items', { method: 'POST', body: JSON.stringify(item) }),
  uploadVaultFile: (formData) => request('/vault/upload', { method: 'POST', body: formData }),
  updateVaultItem: (id, updates) => request(`/vault/items/${id}`, { method: 'PUT', body: JSON.stringify(updates) }),
  deleteVaultItem: (id) => request(`/vault/items/${id}`, { method: 'DELETE' }),
  askVaultItem: (id, question) => request(`/vault/items/${id}/ask`, { method: 'POST', body: JSON.stringify({ item_id: id, question }) }),
  runVaultAction: (action, content) => request('/vault/action', { method: 'POST', body: JSON.stringify({ action, content }) }),
  getVaultRevisions: () => request('/vault/revisions', { method: 'GET' }),

  // Ask My AI Chat
  sendChatMessage: (message, activeCode = null, currentTopic = null) =>
    request('/chat/message', { method: 'POST', body: JSON.stringify({ message, active_code: activeCode, current_topic: currentTopic }) }),
  getChatHistory: () => request('/chat/history', { method: 'GET' }),

  // Weekly Plan
  getCurrentPlan: () => request('/plan/current', { method: 'GET' }),
  generatePlan: () => request('/plan/generate', { method: 'POST' }),
  toggleTask: (taskId) => request(`/plan/tasks/${taskId}/toggle`, { method: 'POST' }),

  // Weekend Assessment
  getCurrentAssessment: () => request('/assessment/current', { method: 'GET' }),
  submitAssessment: (id, answers) => request(`/assessment/${id}/submit`, { method: 'POST', body: JSON.stringify({ answers }) }),

  // Career Path
  getCareerPath: () => request('/career/path', { method: 'GET' }),

  // Aptitude
  getAptitudeSprint: () => request('/aptitude/sprint', { method: 'GET' }),
  submitAptitudeAttempt: (questionIndex, selectedOption, timeTakenSeconds) =>
    request('/aptitude/attempt', {
      method: 'POST',
      body: JSON.stringify({ question_index: questionIndex, selected_option: selectedOption, time_taken_seconds: timeTakenSeconds })
    }),
  getAptitudeStats: () => request('/aptitude/stats', { method: 'GET' }),

  // Interview
  startInterview: (topic) => request('/interview/start', { method: 'POST', body: JSON.stringify({ topic }) }),
  submitInterviewAnswer: (sessionId, questionNumber, userAnswer) =>
    request('/interview/answer', {
      method: 'POST',
      body: JSON.stringify({ session_id: sessionId, question_number: questionNumber, user_answer: userAnswer })
    }),
  getInterviewSession: (sessionId) => request(`/interview/sessions/${sessionId}`, { method: 'GET' }),

  // Admin
  getAdminStats: () => request('/admin/stats', { method: 'GET' }),
};
