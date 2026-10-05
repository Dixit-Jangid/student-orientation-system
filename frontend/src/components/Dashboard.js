import React from 'react';
import { Link } from 'react-router-dom';

function Dashboard({ user, onLogout }) {
  const filieres = [
    {
      label: "Artificial Intelligence & Data Science",
      value: "Intelligence Artificielle & Sciences des Données",
    },
    {
      label: "Cybersecurity & Network Infrastructure",
      value: "Cybersécurité & Infrastructures Réseaux",
    },
    {
      label: "Digital Development & Information Systems",
      value: "Développement Digital & Systèmes d'Information",
    },
  ];

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-content">
          <h1>UniGuide</h1>
          <div className="navbar-actions">
            <span style={{ marginRight: '20px' }}>Hello, {user.username}!</span>
            <Link to="/history" className="btn btn-secondary">History</Link>
            <Link to="/progress" className="btn btn-secondary">Progress</Link>
            <button onClick={onLogout} className="btn btn-secondary">
              Logout
            </button>
          </div>
        </div>
      </nav>

      <div className="container">
        <div className="card">
          <h2 style={{ marginBottom: '30px', color: '#667eea' }}>
            Choose your specialization path
          </h2>
          <p style={{ marginBottom: '30px', color: '#666' }}>
            Select the path you want to explore. The system will evaluate your skills and
            recommend the specialization that best matches your profile.
          </p>

          <div style={{ display: 'grid', gap: '20px' }}>
            {filieres.map((filiere, index) => (
              <Link
                key={index}
                to={`/test?filiere=${encodeURIComponent(filiere.value)}`}
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
                  <h3 style={{ color: '#667eea', marginBottom: '10px' }}>{filiere.label}</h3>
                  <p style={{ color: '#666' }}>
                    Click to start the specialization assessment
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

