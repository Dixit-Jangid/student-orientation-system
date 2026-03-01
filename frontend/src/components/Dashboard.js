import React from 'react';
import { Link } from 'react-router-dom';

function Dashboard({ user, onLogout }) {
  const filieres = [
    "Intelligence Artificielle & Sciences des Données",
    "Cybersécurité & Infrastructures Réseaux",
    "Développement Digital & Systèmes d'Information",
  ];

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-content">
          <h1>Système de Prédiction de Spécialisation</h1>
          <div className="navbar-actions">
            <span style={{ marginRight: '20px' }}>Bonjour, {user.username}!</span>
            <Link to="/history" className="btn btn-secondary">Historique</Link>
            <Link to="/progress" className="btn btn-secondary">Progression</Link>
            <button onClick={onLogout} className="btn btn-secondary">
              Déconnexion
            </button>
          </div>
        </div>
      </nav>

      <div className="container">
        <div className="card">
          <h2 style={{ marginBottom: '30px', color: '#667eea' }}>
            Choisissez votre filière
          </h2>
          <p style={{ marginBottom: '30px', color: '#666' }}>
            Sélectionnez votre filière pour commencer le test de spécialisation.
            Le système analysera vos compétences et vous recommandera la spécialisation
            la plus adaptée à votre profil.
          </p>

          <div style={{ display: 'grid', gap: '20px' }}>
            {filieres.map((filiere, index) => (
              <Link
                key={index}
                to={`/test?filiere=${encodeURIComponent(filiere)}`}
                style={{ textDecoration: 'none' }}
                onClick={(e) => {
                  if (!user) {
                    e.preventDefault();
                    window.location.href = '/login';
                  }
                }}
              >
                <div
                  className="card"
                  style={{
                    cursor: 'pointer',
                    transition: 'transform 0.2s',
                    border: '2px solid #667eea',
                  }}
                  onMouseEnter={(e) => (e.currentTarget.style.transform = 'translateY(-5px)')}
                  onMouseLeave={(e) => (e.currentTarget.style.transform = 'translateY(0)')}
                >
                  <h3 style={{ color: '#667eea', marginBottom: '10px' }}>{filiere}</h3>
                  <p style={{ color: '#666' }}>
                    Cliquez pour commencer le test de spécialisation
                  </p>
                </div>
              </Link>
            ))}
          </div>
        </div>
      </div>
    </div>
  );
}

export default Dashboard;

