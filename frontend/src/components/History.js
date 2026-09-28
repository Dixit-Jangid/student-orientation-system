import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

function History({ user }) {
  const pathLabels = {
    "Intelligence Artificielle & Sciences des Données": "Artificial Intelligence & Data Science",
    "Cybersécurité & Infrastructures Réseaux": "Cybersecurity & Network Infrastructure",
    "Développement Digital & Systèmes d'Information": "Digital Development & Information Systems",
  };
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchHistory();
  }, []);

  const fetchHistory = async () => {
    try {
      const response = await api.get('/api/history');
      setHistory(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching history:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading history...</div>;
  }

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-content">
          <h1>Test History</h1>
          <Link to="/dashboard" className="btn btn-secondary">
            Dashboard
          </Link>
        </div>
      </nav>

      <div className="container">
        {history.length === 0 ? (
          <div className="card">
            <p style={{ textAlign: 'center', color: '#666' }}>
              No tests completed yet.
            </p>
            <Link to="/dashboard" className="btn btn-primary" style={{ display: 'block', textAlign: 'center', marginTop: '20px' }}>
              Take an assessment
            </Link>
          </div>
        ) : (
          <div className="card">
            <h2 style={{ marginBottom: '30px', color: '#667eea' }}>
              Previous assessments ({history.length})
            </h2>
            <div style={{ display: 'grid', gap: '15px' }}>
              {history.map((test) => (
                <div
                  key={test.id}
                  style={{
                    padding: '20px',
                    background: '#f8f9fa',
                    borderRadius: '8px',
                    borderLeft: '4px solid #667eea',
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start' }}>
                    <div>
                      <h3 style={{ color: '#667eea', marginBottom: '10px' }}>
                        {test.predicted_specialization}
                      </h3>
                      <p style={{ color: '#666', marginBottom: '5px' }}>
                        <strong>Path:</strong> {pathLabels[test.filiere] || test.filiere}
                      </p>
                      <p style={{ color: '#666', marginBottom: '5px' }}>
                        <strong>Level:</strong> {test.current_level}/5
                      </p>
                      <p style={{ color: '#666', marginBottom: '5px' }}>
                        <strong>Practical score:</strong> {test.practical_test_score.toFixed(1)}/100
                      </p>
                      <p style={{ color: '#666', marginBottom: '5px' }}>
                        <strong>Confidence:</strong> {(test.confidence * 100).toFixed(1)}%
                      </p>
                      <p style={{ color: '#999', fontSize: '14px' }}>
                        {new Date(test.test_date).toLocaleDateString('en-US', {
                          year: 'numeric',
                          month: 'long',
                          day: 'numeric',
                          hour: '2-digit',
                          minute: '2-digit',
                        })}
                      </p>
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default History;

