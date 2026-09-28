import React, { useState } from 'react';
import { Link, useNavigate } from 'react-router-dom';
import api from '../services/api';

function Login({ onLogin }) {
  const [formData, setFormData] = useState({ username: '', password: '' });
  const [error, setError] = useState('');
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError('');

    try {
      console.log('[LOGIN] Attempting login for:', formData.username);
      
      // OAuth2PasswordRequestForm expects application/x-www-form-urlencoded
      const params = new URLSearchParams();
      params.append('username', formData.username);
      params.append('password', formData.password);

      const response = await api.post('/api/login', params.toString(), {
        headers: { 
          'Content-Type': 'application/x-www-form-urlencoded',
        },
      });

      console.log('[LOGIN] Login successful:', response.data);

      // Pass token and redirect info to parent
      onLogin(response.data.access_token, {
        has_completed_test: response.data.has_completed_test,
        redirect_to: response.data.redirect_to || "/dashboard"
      });
      
      // Redirect based on test history
      const redirectTo = response.data.redirect_to || "/dashboard";
      setTimeout(() => {
        navigate(redirectTo);
      }, 500);
      
    } catch (err) {
      console.error('[LOGIN] Error:', err);
      console.error('[LOGIN] Error response:', err.response?.data);
      setError(err.response?.data?.detail || 'Login failed. Please try again.');
    }
  };

  return (
    <div style={{ 
      minHeight: '100vh',
      display: 'flex',
      background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
      backgroundAttachment: 'fixed'
    }}>
      {/* Left Side - Project Information */}
      <div style={{
        flex: '1',
        display: 'flex',
        flexDirection: 'column',
        justifyContent: 'center',
        alignItems: 'center',
        padding: '60px 40px',
        color: 'white',
        position: 'relative',
        overflow: 'hidden'
      }}>
        {/* Animated Background Elements */}
        <div style={{
          position: 'absolute',
          top: '-50%',
          right: '-50%',
          width: '600px',
          height: '600px',
          background: 'radial-gradient(circle, rgba(255,255,255,0.1) 0%, transparent 70%)',
          borderRadius: '50%',
          animation: 'pulse 4s ease-in-out infinite'
        }} />
        <div style={{
          position: 'absolute',
          bottom: '-30%',
          left: '-30%',
          width: '500px',
          height: '500px',
          background: 'radial-gradient(circle, rgba(240,147,251,0.2) 0%, transparent 70%)',
          borderRadius: '50%',
          animation: 'pulse 5s ease-in-out infinite'
        }} />

        <div style={{ 
          position: 'relative',
          zIndex: 1,
          maxWidth: '500px',
          animation: 'fadeIn 0.8s ease'
        }}>
          <div style={{
            fontSize: '4rem',
            marginBottom: '24px',
            animation: 'float 3s ease-in-out infinite'
          }}>
            🎓
          </div>
          <h1 style={{
            fontSize: '3rem',
            fontWeight: 800,
            marginBottom: '20px',
            lineHeight: '1.2',
            textShadow: '0 4px 20px rgba(0,0,0,0.2)'
          }}>
            UniGuide
            <br />
            <span style={{
              background: 'linear-gradient(135deg, #fff 0%, rgba(255,255,255,0.8) 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}>
              Career Guidance
            </span>
          </h1>
          <p style={{
            fontSize: '1.25rem',
            marginBottom: '40px',
            opacity: 0.95,
            lineHeight: '1.6'
          }}>
            Discover your ideal specialization with AI-powered guidance.
            Assess your strengths and get personalized recommendations.
          </p>

          {/* Specializations Preview */}
          <div style={{
            display: 'grid',
            gridTemplateColumns: 'repeat(3, 1fr)',
            gap: '20px',
            marginTop: '40px'
          }}>
            {[
              { icon: '🤖', name: 'AI & Data', color: '#4facfe' },
              { icon: '🔒', name: 'Cybersecurity', color: '#f093fb' },
              { icon: '💻', name: 'Development', color: '#68d391' }
            ].map((spec, index) => (
              <div
                key={index}
                style={{
                  padding: '20px',
                  background: 'rgba(255,255,255,0.1)',
                  backdropFilter: 'blur(10px)',
                  borderRadius: '16px',
                  border: '1px solid rgba(255,255,255,0.2)',
                  textAlign: 'center',
                  transition: 'all 0.3s ease',
                  cursor: 'pointer'
                }}
                onMouseEnter={(e) => {
                  e.currentTarget.style.transform = 'translateY(-5px)';
                  e.currentTarget.style.background = 'rgba(255,255,255,0.15)';
                }}
                onMouseLeave={(e) => {
                  e.currentTarget.style.transform = 'translateY(0)';
                  e.currentTarget.style.background = 'rgba(255,255,255,0.1)';
                }}
              >
                <div style={{ fontSize: '2.5rem', marginBottom: '8px' }}>{spec.icon}</div>
                <div style={{ fontSize: '0.9rem', fontWeight: 600 }}>{spec.name}</div>
              </div>
            ))}
          </div>

          {/* Quick overview */}
          <div style={{
            marginTop: '40px',
            display: 'flex',
            gap: '30px',
            opacity: 0.9
          }}>
            <div>
              <div style={{ fontSize: '2rem', fontWeight: 800 }}>3</div>
              <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>Career paths</div>
            </div>
            <div>
              <div style={{ fontSize: '2rem', fontWeight: 800 }}>AI</div>
              <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>Guidance</div>
            </div>
            <div>
              <div style={{ fontSize: '2rem', fontWeight: 800 }}>1</div>
              <div style={{ fontSize: '0.9rem', opacity: 0.8 }}>Smart fit</div>
            </div>
          </div>
        </div>
      </div>

      {/* Right Side - Login Form */}
      <div style={{
        flex: '1',
        display: 'flex',
        alignItems: 'center',
        justifyContent: 'center',
        padding: '40px',
        background: 'rgba(255,255,255,0.95)',
        backdropFilter: 'blur(20px)',
        position: 'relative'
      }}>
        <div style={{
          width: '100%',
          maxWidth: '450px',
          animation: 'slideIn 0.6s ease'
        }}>
          <div style={{
            textAlign: 'center',
            marginBottom: '40px'
          }}>
            <h2 style={{
              fontSize: '2.5rem',
              fontWeight: 800,
              marginBottom: '12px',
              background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
              WebkitBackgroundClip: 'text',
              WebkitTextFillColor: 'transparent'
            }}>
              Login
            </h2>
            <p style={{
              color: '#718096',
              fontSize: '1rem'
            }}>
              Access your personalized dashboard
            </p>
          </div>

          {error && (
            <div style={{
              padding: '16px',
              background: 'linear-gradient(135deg, #fc8181 0%, #f56565 100%)',
              color: 'white',
              borderRadius: '12px',
              marginBottom: '24px',
              fontWeight: 600,
              animation: 'fadeIn 0.3s ease'
            }}>
              {error}
            </div>
          )}

          <form onSubmit={handleSubmit} style={{ marginBottom: '24px' }}>
            <div style={{ marginBottom: '24px' }}>
              <label style={{
                display: 'block',
                marginBottom: '8px',
                fontWeight: 600,
                color: '#4a5568',
                fontSize: '0.95rem'
              }}>
                Username
              </label>
              <input
                type="text"
                value={formData.username}
                onChange={(e) => setFormData({ ...formData, username: e.target.value })}
                required
                style={{
                  width: '100%',
                  padding: '16px 20px',
                  border: '2px solid #e2e8f0',
                  borderRadius: '12px',
                  fontSize: '1rem',
                  transition: 'all 0.3s ease',
                  background: '#fff'
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#667eea';
                  e.target.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = '#e2e8f0';
                  e.target.style.boxShadow = 'none';
                }}
              />
            </div>

            <div style={{ marginBottom: '32px' }}>
              <label style={{
                display: 'block',
                marginBottom: '8px',
                fontWeight: 600,
                color: '#4a5568',
                fontSize: '0.95rem'
              }}>
                Password
              </label>
              <input
                type="password"
                value={formData.password}
                onChange={(e) => setFormData({ ...formData, password: e.target.value })}
                required
                style={{
                  width: '100%',
                  padding: '16px 20px',
                  border: '2px solid #e2e8f0',
                  borderRadius: '12px',
                  fontSize: '1rem',
                  transition: 'all 0.3s ease',
                  background: '#fff'
                }}
                onFocus={(e) => {
                  e.target.style.borderColor = '#667eea';
                  e.target.style.boxShadow = '0 0 0 3px rgba(102, 126, 234, 0.1)';
                }}
                onBlur={(e) => {
                  e.target.style.borderColor = '#e2e8f0';
                  e.target.style.boxShadow = 'none';
                }}
              />
            </div>

            <button
              type="submit"
              style={{
                width: '100%',
                padding: '18px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '12px',
                fontSize: '1.1rem',
                fontWeight: 700,
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.5)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
              }}
            >
              Login
            </button>
          </form>

          <div style={{
            textAlign: 'center',
            paddingTop: '24px',
            borderTop: '1px solid #e2e8f0'
          }}>
            <p style={{ color: '#718096', marginBottom: '16px' }}>
              Don’t have an account?
            </p>
            <Link
              to="/register"
              style={{
                display: 'inline-block',
                padding: '12px 32px',
                background: 'transparent',
                color: '#667eea',
                border: '2px solid #667eea',
                borderRadius: '12px',
                textDecoration: 'none',
                fontWeight: 600,
                transition: 'all 0.3s ease'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.background = '#667eea';
                e.currentTarget.style.color = 'white';
                e.currentTarget.style.transform = 'translateY(-2px)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.background = 'transparent';
                e.currentTarget.style.color = '#667eea';
                e.currentTarget.style.transform = 'translateY(0)';
              }}
            >
              Sign up
            </Link>
          </div>
        </div>
      </div>
    </div>
  );
}

export default Login;
