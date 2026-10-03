import React, { createContext, useContext, useState, useEffect } from 'react';
import { api } from '../services/api';

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function loadUser() {
      const token = localStorage.getItem('codepilot_token');
      if (token) {
        try {
          const userData = await api.getMe();
          setUser(userData);
        } catch (err) {
          console.error('Failed to load user profile on startup:', err);
          localStorage.removeItem('codepilot_token');
          localStorage.removeItem('codepilot_user');
          setUser(null);
        }
      }
      setLoading(false);
    }
    loadUser();
  }, []);

  const login = async (email, password) => {
    const data = await api.login({ email, password });
    localStorage.setItem('codepilot_token', data.access_token);
    const userData = await api.getMe();
    setUser(userData);
    return userData;
  };

  const register = async (email, password, fullName, role = 'USER') => {
    const data = await api.register({ email, password, full_name: fullName, role });
    localStorage.setItem('codepilot_token', data.access_token);
    const userData = await api.getMe();
    setUser(userData);
    return userData;
  };

  const logout = async () => {
    try {
      await api.logout();
    } catch (e) {
      // ignore
    }
    localStorage.removeItem('codepilot_token');
    localStorage.removeItem('codepilot_user');
    setUser(null);
  };

  const loginDemo = async (role = 'USER') => {
    if (role === 'ADMIN') {
      return login('admin@codepilot.dev', 'Admin1234!');
    }
    return login('demo@codepilot.dev', 'Demo1234!');
  };

  return (
    <AuthContext.Provider value={{ user, setUser, loading, login, register, logout, loginDemo }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const context = useContext(AuthContext);
  if (!context) throw new Error('useAuth must be used within AuthProvider');
  return context;
}
