import { useEffect, useState } from 'react';
import api from '../services/api';
import { AuthContext } from './authContext.js';

export default function AuthProvider({ children }) {
  const [user, setUser] = useState(null);
  const [token, setToken] = useState(() => localStorage.getItem('token'));
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    if (!token) return;
    api
      .get('/users/profile')
      .then((res) => setUser(res.data))
      .catch(() => {
        // Backend may not be available yet; keep the token and allow the app shell to work.
        setUser(null);
      });
  }, [token]);

  const login = async (credentials) => {
    setLoading(true);
    try {
      const { data } = await api.post('/login', credentials);
      if (data.token) {
        setToken(data.token);
        localStorage.setItem('token', data.token);
      }
      if (data.user) {
        setUser(data.user);
      }
      setLoading(false);
      return data;
    } catch (error) {
      setLoading(false);
      console.error("Login error:", error.response?.data || error.message);
      throw error;
    }
  };

  const register = async (payload) => {
    setLoading(true);
    try {
      const { data } = await api.post('/register', payload);
      setLoading(false);
      return data;
    } catch (error) {
      setLoading(false);
      console.error("Register error:", error.response?.data || error.message);
      throw error;
    }
  };

  const logout = () => {
    setUser(null);
    setToken(null);
    localStorage.removeItem('token');
  };

  return (
    <AuthContext.Provider
      value={{
        user,
        token,
        loading,
        login,
        register,
        logout,
        isAuthenticated: !!token,
      }}
    >
      {children}
    </AuthContext.Provider>
  );
}

