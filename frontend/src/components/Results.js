import React from 'react';
import { useParams, useLocation, Link } from 'react-router-dom';

function Results({ user }) {
  const { testId } = useParams();
  const location = useLocation();
  const prediction = location.state?.prediction;

  if (!prediction) {
    return (
      <div className="container">
        <div className="error">Results are not available.</div>
        <Link to="/dashboard" className="btn btn-primary">
          Back to dashboard
        </Link>
      </div>
    );
  }

  const { predicted_specialization, confidence, top_3_specializations, recommendations } = prediction;
  const confidencePercent = (confidence * 100).toFixed(1);

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-content">
          <h1>Assessment Results</h1>
          <Link to="/dashboard" className="btn btn-secondary">
            Dashboard
          </Link>
        </div>
      </nav>

      <div className="container">
        <div className="card results-card">
          <h2>Your Recommended Specialization</h2>
          <h1 style={{ fontSize: '2.5em', color: '#667eea', margin: '20px 0' }}>
            {predicted_specialization}
          </h1>

          <div style={{ margin: '30px 0' }}>
            <p style={{ marginBottom: '10px', fontWeight: 'bold' }}>Confidence: {confidencePercent}%</p>
            <div className="confidence-bar">
              <div
                className="confidence-fill"
                style={{ width: `${confidencePercent}%` }}
              >
                {confidencePercent}%
              </div>
            </div>
          </div>

          {recommendations?.improvement_message && (
            <div className="success" style={{ margin: '20px 0', textAlign: 'left' }}>
              <strong>Message:</strong> {recommendations.improvement_message}
            </div>
          )}
        </div>

          {/* Top 3 Alternatives */}
          {top_3_specializations && top_3_specializations.length > 1 && (
            <div className="card">
              <h3 style={{ color: '#667eea', marginBottom: '20px' }}>Top 3 Alternatives</h3>
              <div style={{ display: 'grid', gap: '15px' }}>
                {top_3_specializations.slice(0, 3).map((spec, index) => (
                  <div
                    key={index}
                    style={{
                      padding: '15px',
                      background: '#f8f9fa',
                      borderRadius: '5px',
                      borderLeft: `4px solid ${index === 0 ? '#667eea' : '#ccc'}`
                    }}
                  >
                    <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                      <div>
                        <strong>{index + 1}. {spec.specialization}</strong>
                      </div>
                      <div style={{ fontWeight: 'bold', color: '#667eea' }}>
                        {(spec.confidence * 100).toFixed(1)}%
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          )}

          {recommendations && (
          <>
            <div className="card">
              <h3 style={{ color: '#667eea', marginBottom: '20px' }}>
                Personalized Recommendations
              </h3>

              {recommendations.skill_recommendations && recommendations.skill_recommendations.length > 0 && (
                <div style={{ marginBottom: '30px' }}>
                  <h4 style={{ marginBottom: '15px' }}>Skills to improve:</h4>
                  {recommendations.skill_recommendations.map((rec, index) => (
                    <div key={index} style={{ marginBottom: '20px', padding: '15px', background: '#f8f9fa', borderRadius: '5px' }}>
                      <strong>{rec.skill}</strong>
                      <p style={{ marginTop: '5px', color: '#666' }}>
                        Current level: {rec.current_level.toFixed(1)}/3.0
                      </p>
                      {rec.resources && rec.resources.length > 0 && (
                        <div style={{ marginTop: '10px' }}>
                          <strong>Resources:</strong>
                          <ul style={{ marginLeft: '20px', marginTop: '5px' }}>
                            {rec.resources.map((resource, rIdx) => (
                              <li key={rIdx}>{resource}</li>
                            ))}
                          </ul>
                        </div>
                      )}
                    </div>
                  ))}
                </div>
              )}

              {recommendations.topics_to_study && recommendations.topics_to_study.length > 0 && (
                <div style={{ marginBottom: '30px' }}>
                  <h4 style={{ marginBottom: '15px' }}>Topics to study:</h4>
                  <ul style={{ marginLeft: '20px' }}>
                    {recommendations.topics_to_study.map((topic, index) => (
                      <li key={index} style={{ marginBottom: '5px' }}>{topic}</li>
                    ))}
                  </ul>
                </div>
              )}

              {recommendations.next_steps && recommendations.next_steps.length > 0 && (
                <div>
                  <h4 style={{ marginBottom: '15px' }}>Next steps:</h4>
                  <ul style={{ marginLeft: '20px' }}>
                    {recommendations.next_steps.map((step, index) => (
                      <li key={index} style={{ marginBottom: '5px' }}>{step}</li>
                    ))}
                  </ul>
                </div>
              )}
            </div>
          </>
        )}

        <div style={{ display: 'flex', gap: '10px', justifyContent: 'center', marginTop: '20px' }}>
          <Link to="/dashboard" className="btn btn-primary">
            View dashboard
          </Link>
          <Link to="/select-filiere" className="btn btn-primary">
            New assessment
          </Link>
          <Link to="/history" className="btn btn-secondary">
            View history
          </Link>
        </div>
      </div>
    </div>
  );
}

export default Results;

