import React, { useState, useEffect } from 'react';
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom';
import Login from './components/Login';
import Register from './components/Register';
import Dashboard from './components/Dashboard';
import UserDashboard from './components/UserDashboard';
import AdminDashboard from './components/AdminDashboard';
import Test from './components/Test';
import Results from './components/Results';
import History from './components/History';
import Progress from './components/Progress';
import api from './services/api';

function App() {
  const [user, setUser] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = localStorage.getItem('token');
    if (token) {
      api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
      fetchUser();
    } else {
      setLoading(false);
    }
  }, []);

  const fetchUser = async () => {
    try {
      const response = await api.get('/api/user/me');
      setUser(response.data);
    } catch (error) {
      localStorage.removeItem('token');
      delete api.defaults.headers.common['Authorization'];
      setUser(null);
    } finally {
      setLoading(false);
    }
  };

  const handleLogin = (token, redirectInfo) => {
    localStorage.setItem('token', token);
    api.defaults.headers.common['Authorization'] = `Bearer ${token}`;
    fetchUser();
    
    // Redirect based on role and test history
    if (redirectInfo && redirectInfo.redirect_to) {
      setTimeout(() => {
        // Use navigate instead of window.location for better React Router integration
        if (redirectInfo.redirect_to === '/admin') {
          window.location.href = '/admin';
        } else {
          window.location.href = redirectInfo.redirect_to;
        }
      }, 100);
    }
  };

  const handleLogout = () => {
    localStorage.removeItem('token');
    delete api.defaults.headers.common['Authorization'];
    setUser(null);
  };

  if (loading) {
    return <div className="loading">Loading...</div>;
  }

  return (
    <Router>
      <div className="App">
        <Routes>
          <Route
            path="/login"
            element={user ? (user.is_admin ? <Navigate to="/admin" /> : <Navigate to="/dashboard" />) : <Login onLogin={handleLogin} />}
          />
          <Route
            path="/register"
            element={user ? (user.is_admin ? <Navigate to="/admin" /> : <Navigate to="/dashboard" />) : <Register onLogin={handleLogin} />}
          />
          <Route
            path="/dashboard"
            element={user ? <UserDashboard user={user} onLogout={handleLogout} /> : <Navigate to="/login" />}
          />
          <Route
            path="/admin"
            element={user && user.is_admin ? <AdminDashboard user={user} onLogout={handleLogout} /> : <Navigate to="/login" />}
          />
          <Route
            path="/select-filiere"
            element={user ? <Dashboard user={user} onLogout={handleLogout} /> : <Navigate to="/login" />}
          />
          <Route
            path="/test"
            element={user ? <Test user={user} /> : <Navigate to="/login" />}
          />
          <Route
            path="/results/:testId"
            element={user ? <Results user={user} /> : <Navigate to="/login" />}
          />
          <Route
            path="/history"
            element={user ? <History user={user} /> : <Navigate to="/login" />}
          />
          <Route
            path="/progress"
            element={user ? <Progress user={user} /> : <Navigate to="/login" />}
          />
          <Route path="/" element={<Navigate to="/login" />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;

