import React, { useState, useEffect } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';
import { RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, ResponsiveContainer, Legend, Tooltip } from 'recharts';

function UserDashboard({ user, onLogout }) {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const navigate = useNavigate();

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      const response = await api.get('/api/dashboard/user');
      setDashboardData(response.data);
      
      // Redirect to test if no test completed
      if (!response.data.has_test) {
        navigate('/test');
      }
    } catch (error) {
      console.error('Error fetching dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Chargement du tableau de bord...</div>;
  }

  if (!dashboardData || !dashboardData.has_test) {
    return (
      <div className="container">
        <div className="card">
          <h2>Bienvenue, {user.username}!</h2>
          <p>Passez un test pour voir votre tableau de bord personnalisé.</p>
          <Link to="/test" className="btn btn-primary">
            Passer un test
          </Link>
        </div>
      </div>
    );
  }

  // Prepare radar chart data
  const radarData = Object.entries(dashboardData.skill_scores || {}).map(([skill, score]) => ({
    skill: skill.substring(0, 10), // Truncate for display
    score: score,
    fullMark: 100
  }));

  return (
    <div style={{ 
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
      backgroundAttachment: 'fixed'
    }}>
      <nav className="navbar">
        <div className="navbar-content">
          <h1>Tableau de Bord - {user.username}</h1>
          <div className="navbar-actions">
            <Link to="/history" className="btn btn-secondary">Historique</Link>
            <Link to="/progress" className="btn btn-secondary">Progression</Link>
            <Link to="/select-filiere" className="btn btn-primary">Nouveau test</Link>
            <button onClick={onLogout} className="btn btn-secondary">Déconnexion</button>
          </div>
        </div>
      </nav>

      <div className="container" style={{ paddingTop: '20px' }}>
        {/* Improvement Message */}
        <div className="card" style={{ 
          marginBottom: '32px',
          boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
          animation: 'fadeIn 0.5s ease'
        }}>
          <div style={{
            padding: '20px',
            borderRadius: '12px',
            background: dashboardData.improvement_message.includes('amélioré') 
              ? 'linear-gradient(135deg, #68d391 0%, #48bb78 100%)'
              : 'linear-gradient(135deg, #fc8181 0%, #f56565 100%)',
            color: 'white',
            fontWeight: 600,
            fontSize: '1.1rem',
            textAlign: 'center'
          }}>
            {dashboardData.improvement_message}
          </div>
        </div>

        {/* Main Prediction Card */}
        <div className="card" style={{ 
          marginBottom: '40px',
          boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
          background: 'linear-gradient(135deg, rgba(255,255,255,0.95) 0%, rgba(255,255,255,0.98) 100%)',
          animation: 'scaleIn 0.5s ease'
        }}>
          <h2 className="text-gradient" style={{ 
            marginBottom: '24px',
            fontSize: '1.8rem',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            🎯 Votre Spécialisation Recommandée
          </h2>
          
          <div style={{ 
            textAlign: 'center',
            padding: '40px 20px',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            borderRadius: '20px',
            color: 'white',
            marginBottom: '32px',
            boxShadow: '0 8px 25px rgba(102, 126, 234, 0.4)',
            animation: 'pulse 2s ease-in-out infinite'
          }}>
            <h1 style={{ 
              fontSize: '3.5rem', 
              margin: '24px 0',
              fontWeight: 800,
              textShadow: '0 4px 10px rgba(0,0,0,0.2)'
            }}>
              {dashboardData.predicted_specialization}
            </h1>
          </div>
          
          <div style={{ margin: '32px 0' }}>
            <div style={{ 
              display: 'flex', 
              justifyContent: 'space-between', 
              alignItems: 'center',
              marginBottom: '12px'
            }}>
              <p style={{ fontWeight: 700, fontSize: '1.125rem', color: '#4a5568' }}>
                Confiance: {(dashboardData.confidence * 100).toFixed(1)}%
              </p>
              <div style={{
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                padding: '6px 16px',
                borderRadius: '20px',
                fontSize: '0.9rem',
                fontWeight: 600
              }}>
                {dashboardData.confidence >= 0.8 ? 'Très élevée' : 
                 dashboardData.confidence >= 0.6 ? 'Élevée' : 
                 dashboardData.confidence >= 0.4 ? 'Moyenne' : 'Faible'}
              </div>
            </div>
            <div style={{
              width: '100%',
              height: '30px',
              background: '#e2e8f0',
              borderRadius: '15px',
              overflow: 'hidden',
              boxShadow: 'inset 0 2px 4px rgba(0,0,0,0.1)'
            }}>
              <div
                style={{
                  width: `${dashboardData.confidence * 100}%`,
                  height: '100%',
                  background: 'linear-gradient(90deg, #667eea 0%, #764ba2 100%)',
                  borderRadius: '15px',
                  display: 'flex',
                  alignItems: 'center',
                  justifyContent: 'center',
                  color: 'white',
                  fontWeight: 700,
                  fontSize: '0.9rem',
                  transition: 'width 1s ease',
                  boxShadow: '0 2px 8px rgba(102, 126, 234, 0.4)'
                }}
              >
                {(dashboardData.confidence * 100).toFixed(1)}%
              </div>
            </div>
          </div>

          <div style={{ 
            marginTop: '32px', 
            display: 'grid',
            gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))',
            gap: '20px'
          }}>
            <div style={{ 
              padding: '20px', 
              background: 'linear-gradient(135deg, #667eea15 0%, #764ba215 100%)',
              borderRadius: '16px',
              border: '2px solid #667eea40',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '1.5rem', marginBottom: '8px' }}>🎓</div>
              <div style={{ fontSize: '0.9rem', color: '#718096', marginBottom: '8px' }}>Filière</div>
              <div style={{ fontSize: '1.3rem', fontWeight: 700, color: '#667eea' }}>
                {dashboardData.current_filiere}
              </div>
            </div>
            <div style={{ 
              padding: '20px', 
              background: 'linear-gradient(135deg, #f093fb15 0%, #4facfe15 100%)',
              borderRadius: '16px',
              border: '2px solid #f093fb40',
              textAlign: 'center'
            }}>
              <div style={{ fontSize: '1.5rem', marginBottom: '8px' }}>⭐</div>
              <div style={{ fontSize: '0.9rem', color: '#718096', marginBottom: '8px' }}>Niveau</div>
              <div style={{ fontSize: '1.3rem', fontWeight: 700, color: '#f093fb' }}>
                {dashboardData.level_name} ({dashboardData.current_level}/5)
              </div>
            </div>
          </div>
        </div>

        {/* Top 3 Alternatives */}
        {dashboardData.top_3_specializations && dashboardData.top_3_specializations.length > 1 && (
          <div className="card" style={{ 
            marginBottom: '40px',
            boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
            animation: 'fadeIn 0.5s ease'
          }}>
            <h2 className="text-gradient" style={{ 
              marginBottom: '24px',
              fontSize: '1.8rem',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}>
              🏆 Top 3 Spécialisations Alternatives
            </h2>
            <div style={{ display: 'grid', gap: '20px' }}>
              {dashboardData.top_3_specializations.slice(0, 3).map((spec, index) => (
                <div
                  key={index}
                  style={{
                    padding: '24px',
                    background: index === 0 
                      ? 'linear-gradient(135deg, #667eea15 0%, #764ba215 100%)'
                      : index === 1
                      ? 'linear-gradient(135deg, #764ba215 0%, #f093fb15 100%)'
                      : 'linear-gradient(135deg, #f093fb15 0%, #4facfe15 100%)',
                    borderRadius: '16px',
                    border: `3px solid ${index === 0 ? '#667eea' : index === 1 ? '#764ba2' : '#f093fb'}`,
                    transition: 'all 0.3s ease',
                    cursor: 'pointer',
                    boxShadow: '0 4px 15px rgba(0,0,0,0.1)'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateY(-5px)';
                    e.currentTarget.style.boxShadow = '0 8px 25px rgba(0,0,0,0.15)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateY(0)';
                    e.currentTarget.style.boxShadow = '0 4px 15px rgba(0,0,0,0.1)';
                  }}
                >
                  <div style={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
                    <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                      <div style={{ 
                        fontSize: '2.5rem',
                        width: '60px',
                        height: '60px',
                        display: 'flex',
                        alignItems: 'center',
                        justifyContent: 'center',
                        background: index === 0 
                          ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                          : index === 1
                          ? 'linear-gradient(135deg, #764ba2 0%, #f093fb 100%)'
                          : 'linear-gradient(135deg, #f093fb 0%, #4facfe 100%)',
                        borderRadius: '12px',
                        color: 'white',
                        fontWeight: 800
                      }}>
                        {index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉'}
                      </div>
                      <div>
                        <strong style={{ fontSize: '1.25rem', color: '#1a202c', display: 'block', marginBottom: '4px' }}>
                          {spec.specialization}
                        </strong>
                        <div style={{ fontSize: '0.9rem', color: '#718096' }}>
                          Alternative #{index + 1}
                        </div>
                      </div>
                    </div>
                    <div style={{ 
                      padding: '12px 24px',
                      background: index === 0 
                        ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                        : index === 1
                        ? 'linear-gradient(135deg, #764ba2 0%, #f093fb 100%)'
                        : 'linear-gradient(135deg, #f093fb 0%, #4facfe 100%)',
                      borderRadius: '20px',
                      color: 'white',
                      fontWeight: 700, 
                      fontSize: '1.5rem',
                      boxShadow: '0 4px 15px rgba(0,0,0,0.2)'
                    }}>
                      {(spec.confidence * 100).toFixed(1)}%
                    </div>
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* Skill Radar Chart */}
        {radarData.length > 0 && (
          <div className="card" style={{ 
            marginBottom: '40px',
            boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
            animation: 'fadeIn 0.5s ease'
          }}>
            <h2 className="text-gradient" style={{ 
              marginBottom: '24px',
              fontSize: '1.8rem',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}>
              📊 Compétences (Radar)
            </h2>
            <ResponsiveContainer width="100%" height={500}>
              <RadarChart data={radarData}>
                <defs>
                  <linearGradient id="radarGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="0%" stopColor="#667eea" stopOpacity={0.8}/>
                    <stop offset="100%" stopColor="#764ba2" stopOpacity={0.3}/>
                  </linearGradient>
                </defs>
                <PolarGrid stroke="#e2e8f0" strokeWidth={2} />
                <PolarAngleAxis 
                  dataKey="skill" 
                  tick={{ fill: '#4a5568', fontSize: 13, fontWeight: 600 }}
                />
                <PolarRadiusAxis 
                  angle={90} 
                  domain={[0, 100]} 
                  tick={{ fill: '#718096', fontSize: 11 }}
                  label={{ value: 'Score (0-100)', angle: -90, position: 'insideStart' }}
                />
                <Radar
                  name="Score"
                  dataKey="score"
                  stroke="#667eea"
                  fill="url(#radarGradient)"
                  strokeWidth={3}
                  dot={{ fill: '#667eea', r: 5 }}
                  activeDot={{ r: 8, fill: '#764ba2' }}
                />
                <Legend 
                  wrapperStyle={{ paddingTop: '20px' }}
                  iconType="circle"
                />
                <Tooltip 
                  contentStyle={{
                    backgroundColor: 'rgba(255, 255, 255, 0.95)',
                    border: '1px solid #e2e8f0',
                    borderRadius: '12px',
                    boxShadow: '0 4px 15px rgba(0, 0, 0, 0.15)',
                    padding: '12px'
                  }}
                  formatter={(value) => [`${value}/100`, 'Score']}
                />
              </RadarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Scores Summary */}
        <div className="card" style={{ 
          marginBottom: '40px',
          boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
          animation: 'fadeIn 0.5s ease'
        }}>
          <h2 className="text-gradient" style={{ 
            marginBottom: '24px',
            fontSize: '1.8rem',
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            📈 Scores Détaillés
          </h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', gap: '24px' }}>
            <div className="stat-card" style={{ 
              background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
              color: 'white',
              transform: 'translateY(0)',
              transition: 'transform 0.3s ease',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-5px)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div>
                  <h4 style={{ color: 'rgba(255,255,255,0.9)', fontSize: '0.9rem', fontWeight: 600, marginBottom: '8px' }}>TEST PRATIQUE</h4>
                  <p style={{ fontSize: '3rem', fontWeight: 800, margin: 0 }}>
                    {dashboardData.practical_score?.toFixed(1) || 0}
                  </p>
                  <p style={{ fontSize: '1rem', opacity: 0.8, margin: 0 }}>/100</p>
                </div>
                <div style={{ fontSize: '3rem', opacity: 0.3 }}>💼</div>
              </div>
            </div>
            <div className="stat-card" style={{ 
              background: 'linear-gradient(135deg, #f093fb 0%, #4facfe 100%)',
              color: 'white',
              transform: 'translateY(0)',
              transition: 'transform 0.3s ease',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-5px)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div>
                  <h4 style={{ color: 'rgba(255,255,255,0.9)', fontSize: '0.9rem', fontWeight: 600, marginBottom: '8px' }}>RAISONNEMENT LOGIQUE</h4>
                  <p style={{ fontSize: '3rem', fontWeight: 800, margin: 0 }}>
                    {dashboardData.logical_score?.toFixed(1) || 0}
                  </p>
                  <p style={{ fontSize: '1rem', opacity: 0.8, margin: 0 }}>/100</p>
                </div>
                <div style={{ fontSize: '3rem', opacity: 0.3 }}>🧠</div>
              </div>
            </div>
            <div className="stat-card" style={{ 
              background: 'linear-gradient(135deg, #f6ad55 0%, #fc8181 100%)',
              color: 'white',
              transform: 'translateY(0)',
              transition: 'transform 0.3s ease',
              cursor: 'pointer'
            }}
            onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-5px)'}
            onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
              <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
                <div>
                  <h4 style={{ color: 'rgba(255,255,255,0.9)', fontSize: '0.9rem', fontWeight: 600, marginBottom: '8px' }}>RÉSOLUTION PROBLÈMES</h4>
                  <p style={{ fontSize: '3rem', fontWeight: 800, margin: 0 }}>
                    {dashboardData.problem_solving_score?.toFixed(1) || 0}
                  </p>
                  <p style={{ fontSize: '1rem', opacity: 0.8, margin: 0 }}>/100</p>
                </div>
                <div style={{ fontSize: '3rem', opacity: 0.3 }}>🔧</div>
              </div>
            </div>
          </div>
        </div>

        {/* Test History */}
        {dashboardData.test_history && dashboardData.test_history.length > 0 && (
          <div className="card" style={{ 
            marginBottom: '40px',
            boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
            animation: 'fadeIn 0.5s ease'
          }}>
            <h2 className="text-gradient" style={{ 
              marginBottom: '24px',
              fontSize: '1.8rem',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}>
              📋 Historique des Tests
            </h2>
            <div style={{ display: 'grid', gap: '16px' }}>
              {dashboardData.test_history.slice(0, 5).map((test, index) => (
                <div
                  key={test.id}
                  style={{
                    padding: '20px',
                    background: 'linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%)',
                    borderRadius: '12px',
                    display: 'flex',
                    justifyContent: 'space-between',
                    alignItems: 'center',
                    border: '2px solid #e2e8f0',
                    transition: 'all 0.3s ease',
                    cursor: 'pointer'
                  }}
                  onMouseEnter={(e) => {
                    e.currentTarget.style.transform = 'translateX(5px)';
                    e.currentTarget.style.borderColor = '#667eea';
                    e.currentTarget.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.2)';
                  }}
                  onMouseLeave={(e) => {
                    e.currentTarget.style.transform = 'translateX(0)';
                    e.currentTarget.style.borderColor = '#e2e8f0';
                    e.currentTarget.style.boxShadow = 'none';
                  }}
                >
                  <div style={{ display: 'flex', alignItems: 'center', gap: '16px' }}>
                    <div style={{
                      width: '50px',
                      height: '50px',
                      borderRadius: '12px',
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      display: 'flex',
                      alignItems: 'center',
                      justifyContent: 'center',
                      color: 'white',
                      fontWeight: 800,
                      fontSize: '1.2rem'
                    }}>
                      #{index + 1}
                    </div>
                    <div>
                      <strong style={{ fontSize: '1.1rem', color: '#1a202c', display: 'block', marginBottom: '4px' }}>
                        {test.specialization}
                      </strong>
                      <p style={{ margin: 0, color: '#718096', fontSize: '0.9rem' }}>
                        {new Date(test.date).toLocaleDateString('fr-FR', { 
                          year: 'numeric', 
                          month: 'long', 
                          day: 'numeric' 
                        })}
                      </p>
                    </div>
                  </div>
                  <div style={{ textAlign: 'right' }}>
                    <div style={{ 
                      padding: '8px 16px',
                      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                      borderRadius: '20px',
                      color: 'white',
                      fontWeight: 700,
                      fontSize: '1rem',
                      marginBottom: '8px',
                      display: 'inline-block'
                    }}>
                      Niveau {test.level}/5
                    </div>
                    <p style={{ fontSize: '0.9rem', color: '#718096', margin: 0 }}>
                      Score: {test.score.toFixed(1)}/100
                    </p>
                  </div>
                </div>
              ))}
            </div>
            {dashboardData.test_history.length > 5 && (
              <Link 
                to="/history" 
                className="btn btn-primary" 
                style={{ 
                  marginTop: '24px', 
                  display: 'block', 
                  textAlign: 'center',
                  background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                  border: 'none',
                  padding: '14px 28px',
                  fontSize: '1rem',
                  fontWeight: 600
                }}
              >
                Voir tout l'historique ({dashboardData.test_history.length} tests) →
              </Link>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default UserDashboard;

