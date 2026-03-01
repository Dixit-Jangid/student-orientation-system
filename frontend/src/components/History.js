import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import api from '../services/api';

function History({ user }) {
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
    return <div className="loading">Chargement de l'historique...</div>;
  }

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-content">
          <h1>Historique des Tests</h1>
          <Link to="/dashboard" className="btn btn-secondary">
            Tableau de bord
          </Link>
        </div>
      </nav>

      <div className="container">
        {history.length === 0 ? (
          <div className="card">
            <p style={{ textAlign: 'center', color: '#666' }}>
              Aucun test effectué pour le moment.
            </p>
            <Link to="/dashboard" className="btn btn-primary" style={{ display: 'block', textAlign: 'center', marginTop: '20px' }}>
              Passer un test
            </Link>
          </div>
        ) : (
          <div className="card">
            <h2 style={{ marginBottom: '30px', color: '#667eea' }}>
              Vos tests précédents ({history.length})
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
                        <strong>Filière:</strong> {test.filiere}
                      </p>
                      <p style={{ color: '#666', marginBottom: '5px' }}>
                        <strong>Niveau:</strong> {test.current_level}/5
                      </p>
                      <p style={{ color: '#666', marginBottom: '5px' }}>
                        <strong>Score pratique:</strong> {test.practical_test_score.toFixed(1)}/100
                      </p>
                      <p style={{ color: '#666', marginBottom: '5px' }}>
                        <strong>Confiance:</strong> {(test.confidence * 100).toFixed(1)}%
                      </p>
                      <p style={{ color: '#999', fontSize: '14px' }}>
                        {new Date(test.test_date).toLocaleDateString('fr-FR', {
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

