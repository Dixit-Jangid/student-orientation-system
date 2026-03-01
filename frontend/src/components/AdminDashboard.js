import React, { useState, useEffect } from 'react';
import api from '../services/api';
import OldAdminDashboard from './OldAdminDashboard';
import { 
  BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, 
  PieChart, Pie, Cell, LineChart, Line, AreaChart, Area, ComposedChart, RadarChart,
  PolarGrid, PolarAngleAxis, PolarRadiusAxis, Radar, Treemap
} from 'recharts';

const COLORS = ['#667eea', '#764ba2', '#f093fb', '#4facfe', '#00f2fe', '#f6ad55', '#fc8181', '#68d391', '#9f7aea', '#ed64a6'];
const GRADIENT_COLORS = [
  { start: '#667eea', end: '#764ba2' },
  { start: '#f093fb', end: '#4facfe' },
  { start: '#4facfe', end: '#00f2fe' },
  { start: '#f6ad55', end: '#fc8181' },
  { start: '#68d391', end: '#48bb78' }
];

function AdminDashboard({ user, onLogout }) {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [activeView, setActiveView] = useState('overview'); // 'overview' or specific visualization name
  const [showOldDashboard, setShowOldDashboard] = useState(false);

  useEffect(() => {
    fetchAdminData();
  }, []);

  const fetchAdminData = async () => {
    try {
      const response = await api.get('/api/dashboard/admin');
      setDashboardData(response.data);
    } catch (error) {
      console.error('Error fetching admin dashboard:', error);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Chargement du tableau de bord admin...</div>;
  }

  if (!dashboardData) {
    return <div className="error">Erreur lors du chargement des données</div>;
  }

  // Prepare chart data
  const filiereChartData = dashboardData.filiere_distribution?.map(d => ({
    name: d.filiere,
    count: d.count
  })) || [];

  const allSpecData = dashboardData.all_specializations?.map(d => ({
    name: d.specialization.length > 20 ? d.specialization.substring(0, 20) + '...' : d.specialization,
    fullName: d.specialization,
    count: d.count
  })) || [];

  const topSpecData = allSpecData.slice(0, 10);

  const questionData = dashboardData.question_average_scores ? 
    Object.entries(dashboardData.question_average_scores).map(([q, score]) => ({
      question: q,
      score: score.toFixed(2)
    })) : [];

  const topQuestions = [...questionData].sort((a, b) => parseFloat(b.score) - parseFloat(a.score)).slice(0, 10);

  // Navigation items
  const navigationItems = [
    { id: 'overview', name: '📊 Vue d\'ensemble', icon: '📊' },
    { id: 'filiere', name: 'Distribution Filières', icon: '🎓' },
    { id: 'specializations', name: 'Classification Classes', icon: '🎯' },
    { id: 'top-specializations', name: 'Top 10 Spécialisations', icon: '🏆' },
    { id: 'questions', name: 'Scores par Question', icon: '❓' },
    { id: 'top-questions', name: 'Top 10 Questions', icon: '⭐' },
    { id: 'comparison', name: 'Comparaison Filières', icon: '🔗' },
    { id: 'global-scores', name: 'Scores Globaux', icon: '📈' },
    { id: 'evolution', name: 'Évolution Questions', icon: '📉' }
  ];

  const handleViewChange = (viewId) => {
    setActiveView(viewId);
  };

  const handleBackToOverview = () => {
    setActiveView('overview');
  };

  // Check if we should show a specific visualization
  const shouldShowSection = (sectionId) => {
    return activeView === 'overview' || activeView === sectionId;
  };

  // Show old dashboard if toggle is on
  if (showOldDashboard) {
    return <OldAdminDashboard user={user} onLogout={onLogout} onBackToNew={() => setShowOldDashboard(false)} />;
  }

  return (
    <div style={{ display: 'flex', minHeight: '100vh' }}>
      {/* Left Sidebar Navigation */}
      <div style={{
        width: '280px',
        background: 'linear-gradient(180deg, #1a202c 0%, #2d3748 100%)',
        color: 'white',
        padding: '24px',
        position: 'fixed',
        height: '100vh',
        overflowY: 'auto',
        boxShadow: '4px 0 20px rgba(0,0,0,0.1)',
        zIndex: 1000
      }}>
        <div style={{ marginBottom: '32px' }}>
          <h2 style={{ 
            fontSize: '1.5rem', 
            fontWeight: 800, 
            marginBottom: '8px',
            background: 'linear-gradient(135deg, #667eea 0%, #f093fb 100%)',
            WebkitBackgroundClip: 'text',
            WebkitTextFillColor: 'transparent'
          }}>
            Navigation
          </h2>
          <p style={{ fontSize: '0.85rem', color: '#a0aec0', margin: 0 }}>
            Visualisations disponibles
          </p>
        </div>

        <div style={{ marginBottom: '24px' }}>
          <button
            onClick={() => setShowOldDashboard(true)}
            style={{
              width: '100%',
              padding: '12px 16px',
              background: 'rgba(102, 126, 234, 0.1)',
              border: '2px solid #667eea',
              borderRadius: '12px',
              color: 'white',
              fontWeight: 600,
              cursor: 'pointer',
              transition: 'all 0.3s ease',
              marginBottom: '16px'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.background = 'rgba(102, 126, 234, 0.2)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.background = 'rgba(102, 126, 234, 0.1)';
            }}
          >
            📋 Ancien Dashboard
          </button>
        </div>

        <nav style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
          {navigationItems.map((item) => (
            <button
              key={item.id}
              onClick={() => handleViewChange(item.id)}
              style={{
                width: '100%',
                padding: '14px 16px',
                background: activeView === item.id
                  ? 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)'
                  : 'transparent',
                border: activeView === item.id ? 'none' : '2px solid rgba(255,255,255,0.1)',
                borderRadius: '12px',
                color: 'white',
                textAlign: 'left',
                fontWeight: activeView === item.id ? 700 : 500,
                cursor: 'pointer',
                transition: 'all 0.3s ease',
                display: 'flex',
                alignItems: 'center',
                gap: '12px',
                fontSize: '0.95rem'
              }}
              onMouseEnter={(e) => {
                if (activeView !== item.id) {
                  e.currentTarget.style.background = 'rgba(102, 126, 234, 0.2)';
                  e.currentTarget.style.borderColor = 'rgba(102, 126, 234, 0.5)';
                }
              }}
              onMouseLeave={(e) => {
                if (activeView !== item.id) {
                  e.currentTarget.style.background = 'transparent';
                  e.currentTarget.style.borderColor = 'rgba(255,255,255,0.1)';
                }
              }}
            >
              <span style={{ fontSize: '1.2rem' }}>{item.icon}</span>
              <span>{item.name.replace(/^[^\s]+\s/, '')}</span>
            </button>
          ))}
        </nav>

        <div style={{ 
          marginTop: '32px', 
          padding: '16px', 
          background: 'rgba(102, 126, 234, 0.1)',
          borderRadius: '12px',
          border: '1px solid rgba(102, 126, 234, 0.3)'
        }}>
          <p style={{ fontSize: '0.8rem', color: '#a0aec0', margin: 0, lineHeight: '1.5' }}>
            💡 Cliquez sur une visualisation pour la voir en détail. Cliquez en dehors pour revenir à la vue d'ensemble.
          </p>
        </div>
      </div>

      {/* Main Content Area */}
      <div style={{ 
        marginLeft: '280px', 
        width: 'calc(100% - 280px)',
        minHeight: '100vh',
        background: 'linear-gradient(135deg, #667eea 0%, #764ba2 50%, #f093fb 100%)',
        backgroundAttachment: 'fixed'
      }}>
        <nav className="navbar">
          <div className="navbar-content">
            <h1>Tableau de Bord Admin - Visualisations</h1>
            <div className="navbar-actions">
              <button onClick={onLogout} className="btn btn-secondary">Déconnexion</button>
            </div>
          </div>
        </nav>

        <div className="container" 
          onClick={(e) => {
            // If clicking on container background (not on a card), go back to overview
            if (e.target.classList.contains('container') && activeView !== 'overview') {
              handleBackToOverview();
            }
          }}
          style={{ 
            cursor: activeView !== 'overview' ? 'pointer' : 'default',
            position: 'relative',
            paddingTop: '20px'
          }}
        >
        {/* Back to Overview Button - Show when specific view is active */}
        {activeView !== 'overview' && (
          <div style={{
            position: 'fixed',
            top: '80px',
            right: '40px',
            zIndex: 999,
            animation: 'fadeIn 0.3s ease'
          }}>
            <button
              onClick={handleBackToOverview}
              style={{
                padding: '12px 24px',
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                border: 'none',
                borderRadius: '25px',
                fontWeight: 600,
                cursor: 'pointer',
                boxShadow: '0 4px 15px rgba(102, 126, 234, 0.4)',
                transition: 'all 0.3s ease',
                display: 'flex',
                alignItems: 'center',
                gap: '8px',
                fontSize: '0.95rem'
              }}
              onMouseEnter={(e) => {
                e.currentTarget.style.transform = 'translateY(-2px)';
                e.currentTarget.style.boxShadow = '0 6px 20px rgba(102, 126, 234, 0.6)';
              }}
              onMouseLeave={(e) => {
                e.currentTarget.style.transform = 'translateY(0)';
                e.currentTarget.style.boxShadow = '0 4px 15px rgba(102, 126, 234, 0.4)';
              }}
            >
              <span>←</span> Retour à la vue d'ensemble
            </button>
          </div>
        )}

        {/* Statistics Cards - Enhanced */}
        {shouldShowSection('overview') && (
          <div style={{ 
            display: 'grid', 
            gridTemplateColumns: 'repeat(auto-fit, minmax(240px, 1fr))', 
            gap: '24px', 
            marginBottom: '40px',
            animation: activeView === 'overview' ? 'fadeIn 0.5s ease' : 'none'
          }}>
          <div className="stat-card" style={{ 
            background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
            color: 'white',
            transform: 'translateY(0)',
            transition: 'transform 0.3s ease',
            cursor: 'pointer'
          }}
          onMouseEnter={(e) => e.currentTarget.style.transform = 'translateY(-5px)'}
          onMouseLeave={(e) => e.currentTarget.style.transform = 'translateY(0)'}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between' }}>
              <div>
                <h3 style={{ color: 'rgba(255,255,255,0.9)', fontSize: '0.9rem', fontWeight: 600, marginBottom: '8px' }}>UTILISATEURS</h3>
                <p style={{ fontSize: '3rem', fontWeight: 800, margin: 0 }}>{dashboardData.total_users}</p>
              </div>
              <div style={{ fontSize: '3rem', opacity: 0.3 }}>👥</div>
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
                <h3 style={{ color: 'rgba(255,255,255,0.9)', fontSize: '0.9rem', fontWeight: 600, marginBottom: '8px' }}>TESTS</h3>
                <p style={{ fontSize: '3rem', fontWeight: 800, margin: 0 }}>{dashboardData.total_tests}</p>
              </div>
              <div style={{ fontSize: '3rem', opacity: 0.3 }}>📊</div>
            </div>
          </div>
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
                <h3 style={{ color: 'rgba(255,255,255,0.9)', fontSize: '0.9rem', fontWeight: 600, marginBottom: '8px' }}>FILIÈRES</h3>
                <p style={{ fontSize: '3rem', fontWeight: 800, margin: 0 }}>{filiereChartData.length}</p>
              </div>
              <div style={{ fontSize: '3rem', opacity: 0.3 }}>🎓</div>
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
                <h3 style={{ color: 'rgba(255,255,255,0.9)', fontSize: '0.9rem', fontWeight: 600, marginBottom: '8px' }}>SPÉCIALISATIONS</h3>
                <p style={{ fontSize: '3rem', fontWeight: 800, margin: 0 }}>{allSpecData.length}</p>
              </div>
              <div style={{ fontSize: '3rem', opacity: 0.3 }}>⭐</div>
            </div>
          </div>
        </div>
        )}

        {/* 1. Distribution par Filière - Enhanced */}
        {shouldShowSection('filiere') && filiereChartData.length > 0 && (
          <div 
            className="card" 
            style={{ 
              marginBottom: '40px', 
              boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
              animation: activeView === 'filiere' ? 'scaleIn 0.5s ease' : 'fadeIn 0.5s ease',
              cursor: 'default'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
              <h2 className="text-gradient" style={{ margin: 0, fontSize: '1.8rem' }}>📊 Distribution par Filière</h2>
              <div style={{ 
                background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                color: 'white',
                padding: '8px 16px',
                borderRadius: '20px',
                fontSize: '0.9rem',
                fontWeight: 600
              }}>
                Total: {filiereChartData.reduce((sum, d) => sum + d.count, 0)} tests
              </div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px', alignItems: 'center' }}>
              <div>
                <ResponsiveContainer width="100%" height={400}>
                  <PieChart>
                    <defs>
                      {filiereChartData.map((entry, index) => (
                        <linearGradient key={`gradient-${index}`} id={`gradient-${index}`} x1="0" y1="0" x2="1" y2="1">
                          <stop offset="0%" stopColor={GRADIENT_COLORS[index % GRADIENT_COLORS.length].start} stopOpacity={1}/>
                          <stop offset="100%" stopColor={GRADIENT_COLORS[index % GRADIENT_COLORS.length].end} stopOpacity={1}/>
                        </linearGradient>
                      ))}
                    </defs>
                    <Pie
                      data={filiereChartData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent, count }) => `${name.substring(0, 25)}${name.length > 25 ? '...' : ''}\n${(percent * 100).toFixed(1)}% (${count})`}
                      outerRadius={140}
                      innerRadius={60}
                      fill="#8884d8"
                      dataKey="count"
                      animationBegin={0}
                      animationDuration={800}
                    >
                      {filiereChartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={`url(#gradient-${index})`} stroke="#fff" strokeWidth={2} />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(value, name) => [`${value} tests`, 'Nombre']}
                      contentStyle={{ 
                        background: 'rgba(255, 255, 255, 0.95)', 
                        border: '1px solid #e2e8f0',
                        borderRadius: '8px',
                        padding: '12px'
                      }}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div>
                <ResponsiveContainer width="100%" height={400}>
                  <BarChart data={filiereChartData} layout="vertical" margin={{ left: 20, right: 20 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis type="number" tick={{ fill: '#718096' }} />
                    <YAxis 
                      dataKey="name" 
                      type="category" 
                      width={140}
                      tick={{ fill: '#4a5568', fontSize: 12 }}
                    />
                    <Tooltip 
                      formatter={(value) => [`${value} tests`, 'Nombre']}
                      contentStyle={{ 
                        background: 'rgba(255, 255, 255, 0.95)', 
                        border: '1px solid #e2e8f0',
                        borderRadius: '8px'
                      }}
                    />
                    <Bar 
                      dataKey="count" 
                      radius={[0, 8, 8, 0]}
                      animationDuration={800}
                    >
                      {filiereChartData.map((entry, index) => (
                        <Cell key={`bar-cell-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
            {/* Summary Stats */}
            <div style={{ 
              marginTop: '24px', 
              padding: '20px', 
              background: 'linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%)',
              borderRadius: '12px',
              display: 'grid',
              gridTemplateColumns: `repeat(${filiereChartData.length}, 1fr)`,
              gap: '16px'
            }}>
              {filiereChartData.map((item, index) => (
                <div key={index} style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '2rem', fontWeight: 800, color: COLORS[index % COLORS.length] }}>
                    {item.count}
                  </div>
                  <div style={{ fontSize: '0.85rem', color: '#718096', marginTop: '4px' }}>
                    {item.name}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#a0aec0', marginTop: '2px' }}>
                    {((item.count / filiereChartData.reduce((sum, d) => sum + d.count, 0)) * 100).toFixed(1)}%
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 2. Classification des Classes - Distribution des Spécialisations - Enhanced */}
        {shouldShowSection('specializations') && allSpecData.length > 0 && (
          <div 
            className="card" 
            style={{ 
              marginBottom: '40px', 
              boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
              animation: activeView === 'specializations' ? 'scaleIn 0.5s ease' : 'fadeIn 0.5s ease',
              cursor: 'default'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
              <h2 className="text-gradient" style={{ margin: 0, fontSize: '1.8rem' }}>🎯 Classification des Classes - Toutes les Spécialisations</h2>
              <div style={{ 
                background: 'linear-gradient(135deg, #764ba2 0%, #f093fb 100%)',
                color: 'white',
                padding: '8px 16px',
                borderRadius: '20px',
                fontSize: '0.9rem',
                fontWeight: 600
              }}>
                {allSpecData.length} spécialisations
              </div>
            </div>
            <ResponsiveContainer width="100%" height={600}>
              <BarChart data={allSpecData} layout="vertical" margin={{ left: 220, right: 40, top: 20, bottom: 20 }}>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis 
                  type="number" 
                  tick={{ fill: '#718096' }}
                  label={{ value: 'Nombre de tests', position: 'insideBottom', offset: -10, fill: '#4a5568' }}
                />
                <YAxis 
                  dataKey="name" 
                  type="category" 
                  width={200}
                  tick={{ fill: '#4a5568', fontSize: 11 }}
                />
                <Tooltip 
                  formatter={(value, name) => [`${value} tests`, 'Nombre']}
                  labelFormatter={(label) => `Spécialisation: ${label}`}
                  contentStyle={{ 
                    background: 'rgba(255, 255, 255, 0.95)', 
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px',
                    padding: '12px'
                  }}
                />
                <Bar 
                  dataKey="count" 
                  radius={[0, 8, 8, 0]}
                  animationDuration={1000}
                  animationBegin={0}
                >
                  {allSpecData.map((entry, index) => (
                    <Cell 
                      key={`spec-cell-${index}`} 
                      fill={COLORS[index % COLORS.length]}
                      opacity={0.8 + (index % 3) * 0.1}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
            {/* Top 5 Summary */}
            <div style={{ 
              marginTop: '24px', 
              padding: '20px', 
              background: 'linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%)',
              borderRadius: '12px',
              display: 'grid',
              gridTemplateColumns: 'repeat(5, 1fr)',
              gap: '16px'
            }}>
              {allSpecData.slice(0, 5).map((item, index) => (
                <div key={index} style={{ textAlign: 'center' }}>
                  <div style={{ fontSize: '1.5rem', fontWeight: 800, color: COLORS[index % COLORS.length] }}>
                    #{index + 1}
                  </div>
                  <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#2d3748', marginTop: '4px' }}>
                    {item.count}
                  </div>
                  <div style={{ fontSize: '0.8rem', color: '#718096', marginTop: '4px', lineHeight: '1.3' }}>
                    {item.fullName.substring(0, 30)}{item.fullName.length > 30 ? '...' : ''}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 3. Top 10 Spécialisations - Enhanced */}
        {shouldShowSection('top-specializations') && topSpecData.length > 0 && (
          <div className="card" style={{ marginBottom: '40px', boxShadow: '0 10px 30px rgba(0,0,0,0.1)' }}>
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
              <h2 className="text-gradient" style={{ margin: 0, fontSize: '1.8rem' }}>🏆 Top 10 Spécialisations</h2>
              <div style={{ 
                background: 'linear-gradient(135deg, #f093fb 0%, #4facfe 100%)',
                color: 'white',
                padding: '8px 16px',
                borderRadius: '20px',
                fontSize: '0.9rem',
                fontWeight: 600
              }}>
                {topSpecData.reduce((sum, d) => sum + d.count, 0)} tests au total
              </div>
            </div>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
              <div>
                <ResponsiveContainer width="100%" height={450}>
                  <PieChart>
                    <defs>
                      {topSpecData.map((entry, index) => (
                        <linearGradient key={`top-grad-${index}`} id={`top-grad-${index}`} x1="0" y1="0" x2="1" y2="1">
                          <stop offset="0%" stopColor={GRADIENT_COLORS[index % GRADIENT_COLORS.length].start} stopOpacity={1}/>
                          <stop offset="100%" stopColor={GRADIENT_COLORS[index % GRADIENT_COLORS.length].end} stopOpacity={1}/>
                        </linearGradient>
                      ))}
                    </defs>
                    <Pie
                      data={topSpecData}
                      cx="50%"
                      cy="50%"
                      labelLine={false}
                      label={({ name, percent, count }) => `${name}\n${(percent * 100).toFixed(1)}% (${count})`}
                      outerRadius={150}
                      innerRadius={70}
                      fill="#8884d8"
                      dataKey="count"
                      animationBegin={0}
                      animationDuration={1000}
                    >
                      {topSpecData.map((entry, index) => (
                        <Cell key={`top-cell-${index}`} fill={`url(#top-grad-${index})`} stroke="#fff" strokeWidth={2} />
                      ))}
                    </Pie>
                    <Tooltip 
                      formatter={(value, name) => [`${value} tests`, 'Nombre']}
                      contentStyle={{ 
                        background: 'rgba(255, 255, 255, 0.95)', 
                        border: '1px solid #e2e8f0',
                        borderRadius: '8px',
                        padding: '12px'
                      }}
                    />
                    <Legend 
                      verticalAlign="bottom" 
                      height={36}
                      formatter={(value) => value.length > 20 ? value.substring(0, 20) + '...' : value}
                    />
                  </PieChart>
                </ResponsiveContainer>
              </div>
              <div>
                <ResponsiveContainer width="100%" height={450}>
                  <AreaChart data={topSpecData} margin={{ top: 20, right: 30, left: 0, bottom: 60 }}>
                    <defs>
                      <linearGradient id="areaGradient" x1="0" y1="0" x2="0" y2="1">
                        <stop offset="5%" stopColor="#764ba2" stopOpacity={0.8}/>
                        <stop offset="95%" stopColor="#764ba2" stopOpacity={0.1}/>
                      </linearGradient>
                    </defs>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis 
                      dataKey="name" 
                      angle={-45} 
                      textAnchor="end" 
                      height={80}
                      tick={{ fill: '#718096', fontSize: 11 }}
                    />
                    <YAxis tick={{ fill: '#718096' }} />
                    <Tooltip 
                      formatter={(value) => [`${value} tests`, 'Nombre']}
                      contentStyle={{ 
                        background: 'rgba(255, 255, 255, 0.95)', 
                        border: '1px solid #e2e8f0',
                        borderRadius: '8px'
                      }}
                    />
                    <Area 
                      type="monotone" 
                      dataKey="count" 
                      stroke="#764ba2" 
                      strokeWidth={3}
                      fill="url(#areaGradient)" 
                      animationDuration={1000}
                    />
                  </AreaChart>
                </ResponsiveContainer>
              </div>
            </div>
            {/* Top 3 Highlight */}
            <div style={{ 
              marginTop: '24px', 
              padding: '24px', 
              background: 'linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%)',
              borderRadius: '12px',
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '20px'
            }}>
              {topSpecData.slice(0, 3).map((item, index) => (
                <div 
                  key={index} 
                  style={{ 
                    textAlign: 'center',
                    padding: '20px',
                    background: 'white',
                    borderRadius: '12px',
                    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                    border: `3px solid ${COLORS[index]}`
                  }}
                >
                  <div style={{ fontSize: '3rem', marginBottom: '8px' }}>
                    {index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉'}
                  </div>
                  <div style={{ fontSize: '2rem', fontWeight: 800, color: COLORS[index], marginBottom: '8px' }}>
                    {item.count}
                  </div>
                  <div style={{ fontSize: '0.9rem', color: '#4a5568', fontWeight: 600, lineHeight: '1.4' }}>
                    {item.fullName}
                  </div>
                  <div style={{ fontSize: '0.75rem', color: '#718096', marginTop: '4px' }}>
                    {((item.count / topSpecData.reduce((sum, d) => sum + d.count, 0)) * 100).toFixed(1)}% du total
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 4. Scores Moyens par Question - Enhanced */}
        {shouldShowSection('questions') && questionData.length > 0 && (
          <div 
            className="card" 
            style={{ 
              marginBottom: '40px', 
              boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
              animation: activeView === 'questions' ? 'scaleIn 0.5s ease' : 'fadeIn 0.5s ease',
              cursor: 'default'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
              <h2 className="text-gradient" style={{ margin: 0, fontSize: '1.8rem' }}>❓ Scores Moyens par Question (Q1-Q25)</h2>
              <div style={{ 
                background: 'linear-gradient(135deg, #4facfe 0%, #00f2fe 100%)',
                color: 'white',
                padding: '8px 16px',
                borderRadius: '20px',
                fontSize: '0.9rem',
                fontWeight: 600
              }}>
                Moyenne: {(questionData.reduce((sum, q) => sum + parseFloat(q.score), 0) / questionData.length).toFixed(2)}/3
              </div>
            </div>
            <ResponsiveContainer width="100%" height={450}>
              <ComposedChart data={questionData} margin={{ top: 20, right: 30, left: 0, bottom: 80 }}>
                <defs>
                  <linearGradient id="barGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#4facfe" stopOpacity={0.9}/>
                    <stop offset="95%" stopColor="#00f2fe" stopOpacity={0.9}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis 
                  dataKey="question" 
                  angle={-45} 
                  textAnchor="end" 
                  height={100}
                  tick={{ fill: '#718096', fontSize: 11 }}
                />
                <YAxis 
                  domain={[0, 3]}
                  tick={{ fill: '#718096' }}
                  label={{ value: 'Score moyen (0-3)', angle: -90, position: 'insideLeft', fill: '#4a5568' }}
                />
                <Tooltip 
                  formatter={(value) => [`Score: ${parseFloat(value).toFixed(2)}/3`, '']}
                  contentStyle={{ 
                    background: 'rgba(255, 255, 255, 0.95)', 
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px'
                  }}
                />
                <Bar 
                  dataKey="score" 
                  fill="url(#barGradient)" 
                  radius={[4, 4, 0, 0]}
                  animationDuration={1000}
                />
                <Line 
                  type="monotone" 
                  dataKey="score" 
                  stroke="#00f2fe" 
                  strokeWidth={3}
                  dot={{ fill: '#00f2fe', r: 4 }}
                  activeDot={{ r: 6 }}
                  animationDuration={1000}
                />
              </ComposedChart>
            </ResponsiveContainer>
            {/* Question Stats */}
            <div style={{ 
              marginTop: '24px', 
              padding: '20px', 
              background: 'linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%)',
              borderRadius: '12px',
              display: 'grid',
              gridTemplateColumns: 'repeat(4, 1fr)',
              gap: '16px'
            }}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#4facfe' }}>
                  {Math.max(...questionData.map(q => parseFloat(q.score))).toFixed(2)}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#718096', marginTop: '4px' }}>Score Maximum</div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#00f2fe' }}>
                  {Math.min(...questionData.map(q => parseFloat(q.score))).toFixed(2)}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#718096', marginTop: '4px' }}>Score Minimum</div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#764ba2' }}>
                  {(questionData.reduce((sum, q) => sum + parseFloat(q.score), 0) / questionData.length).toFixed(2)}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#718096', marginTop: '4px' }}>Moyenne</div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 700, color: '#f093fb' }}>
                  {questionData.length}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#718096', marginTop: '4px' }}>Total Questions</div>
              </div>
            </div>
          </div>
        )}

        {/* 5. Top 10 Questions avec Meilleurs Scores - Enhanced */}
        {shouldShowSection('top-questions') && topQuestions.length > 0 && (
          <div 
            className="card" 
            style={{ 
              marginBottom: '40px', 
              boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
              animation: activeView === 'top-questions' ? 'scaleIn 0.5s ease' : 'fadeIn 0.5s ease',
              cursor: 'default'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
              <h2 className="text-gradient" style={{ margin: 0, fontSize: '1.8rem' }}>⭐ Top 10 Questions avec Meilleurs Scores</h2>
              <div style={{ 
                background: 'linear-gradient(135deg, #f093fb 0%, #fc8181 100%)',
                color: 'white',
                padding: '8px 16px',
                borderRadius: '20px',
                fontSize: '0.9rem',
                fontWeight: 600
              }}>
                Meilleur: {parseFloat(topQuestions[0]?.score || 0).toFixed(2)}/3
              </div>
            </div>
            <ResponsiveContainer width="100%" height={450}>
              <BarChart data={topQuestions} layout="vertical" margin={{ left: 60, right: 40, top: 20, bottom: 20 }}>
                <defs>
                  <linearGradient id="questionGradient" x1="0" y1="0" x2="1" y2="0">
                    <stop offset="0%" stopColor="#f093fb" stopOpacity={1}/>
                    <stop offset="100%" stopColor="#fc8181" stopOpacity={1}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis 
                  type="number" 
                  domain={[0, 3]}
                  tick={{ fill: '#718096' }}
                  label={{ value: 'Score moyen (0-3)', position: 'insideBottom', offset: -10, fill: '#4a5568' }}
                />
                <YAxis 
                  dataKey="question" 
                  type="category" 
                  width={80}
                  tick={{ fill: '#4a5568', fontSize: 12, fontWeight: 600 }}
                />
                <Tooltip 
                  formatter={(value) => [`Score: ${parseFloat(value).toFixed(2)}/3`, '']}
                  contentStyle={{ 
                    background: 'rgba(255, 255, 255, 0.95)', 
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px'
                  }}
                />
                <Bar 
                  dataKey="score" 
                  fill="url(#questionGradient)" 
                  radius={[0, 8, 8, 0]}
                  animationDuration={1000}
                >
                  {topQuestions.map((entry, index) => (
                    <Cell 
                      key={`top-q-${index}`} 
                      fill={COLORS[(index + 4) % COLORS.length]}
                      opacity={0.9}
                    />
                  ))}
                </Bar>
              </BarChart>
            </ResponsiveContainer>
            {/* Top 3 Questions Highlight */}
            <div style={{ 
              marginTop: '24px', 
              padding: '20px', 
              background: 'linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%)',
              borderRadius: '12px',
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '16px'
            }}>
              {topQuestions.slice(0, 3).map((item, index) => (
                <div 
                  key={index} 
                  style={{ 
                    textAlign: 'center',
                    padding: '16px',
                    background: 'white',
                    borderRadius: '12px',
                    boxShadow: '0 4px 6px rgba(0,0,0,0.1)',
                    border: `3px solid ${COLORS[(index + 4) % COLORS.length]}`
                  }}
                >
                  <div style={{ fontSize: '2.5rem', marginBottom: '8px' }}>
                    {index === 0 ? '🥇' : index === 1 ? '🥈' : '🥉'}
                  </div>
                  <div style={{ fontSize: '1.8rem', fontWeight: 800, color: COLORS[(index + 4) % COLORS.length], marginBottom: '4px' }}>
                    {parseFloat(item.score).toFixed(2)}
                  </div>
                  <div style={{ fontSize: '1rem', color: '#4a5568', fontWeight: 600 }}>
                    {item.question}
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 6. Distribution Filière vs Spécialisations - Enhanced */}
        {shouldShowSection('comparison') && filiereChartData.length > 0 && allSpecData.length > 0 && (
          <div 
            className="card" 
            style={{ 
              marginBottom: '40px', 
              boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
              animation: activeView === 'comparison' ? 'scaleIn 0.5s ease' : 'fadeIn 0.5s ease',
              cursor: 'default'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <h2 className="text-gradient" style={{ marginBottom: '24px', fontSize: '1.8rem' }}>🔗 Comparaison Filières et Spécialisations</h2>
            <div style={{ display: 'grid', gridTemplateColumns: '1fr 1fr', gap: '32px' }}>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                  <h3 style={{ margin: 0, color: '#667eea', fontSize: '1.2rem', fontWeight: 700 }}>📚 Par Filière</h3>
                  <div style={{ 
                    background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)',
                    color: 'white',
                    padding: '4px 12px',
                    borderRadius: '12px',
                    fontSize: '0.8rem',
                    fontWeight: 600
                  }}>
                    {filiereChartData.length} filières
                  </div>
                </div>
                <ResponsiveContainer width="100%" height={350}>
                  <BarChart data={filiereChartData} margin={{ top: 20, right: 30, bottom: 80, left: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis 
                      dataKey="name" 
                      angle={-45} 
                      textAnchor="end" 
                      height={80}
                      tick={{ fill: '#718096', fontSize: 11 }}
                    />
                    <YAxis tick={{ fill: '#718096' }} />
                    <Tooltip 
                      formatter={(value) => [`${value} tests`, 'Nombre']}
                      contentStyle={{ 
                        background: 'rgba(255, 255, 255, 0.95)', 
                        border: '1px solid #e2e8f0',
                        borderRadius: '8px'
                      }}
                    />
                    <Bar dataKey="count" radius={[8, 8, 0, 0]} animationDuration={800}>
                      {filiereChartData.map((entry, index) => (
                        <Cell key={`filiere-bar-${index}`} fill={COLORS[index % COLORS.length]} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
              <div>
                <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '16px' }}>
                  <h3 style={{ margin: 0, color: '#764ba2', fontSize: '1.2rem', fontWeight: 700 }}>⭐ Top Spécialisations</h3>
                  <div style={{ 
                    background: 'linear-gradient(135deg, #764ba2 0%, #f093fb 100%)',
                    color: 'white',
                    padding: '4px 12px',
                    borderRadius: '12px',
                    fontSize: '0.8rem',
                    fontWeight: 600
                  }}>
                    Top {topSpecData.length}
                  </div>
                </div>
                <ResponsiveContainer width="100%" height={350}>
                  <BarChart data={topSpecData} margin={{ top: 20, right: 30, bottom: 80, left: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis 
                      dataKey="name" 
                      angle={-45} 
                      textAnchor="end" 
                      height={80}
                      tick={{ fill: '#718096', fontSize: 10 }}
                    />
                    <YAxis tick={{ fill: '#718096' }} />
                    <Tooltip 
                      formatter={(value) => [`${value} tests`, 'Nombre']}
                      contentStyle={{ 
                        background: 'rgba(255, 255, 255, 0.95)', 
                        border: '1px solid #e2e8f0',
                        borderRadius: '8px'
                      }}
                    />
                    <Bar dataKey="count" radius={[8, 8, 0, 0]} animationDuration={800}>
                      {topSpecData.map((entry, index) => (
                        <Cell key={`spec-bar-${index}`} fill={COLORS[(index + 2) % COLORS.length]} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        )}

        {/* 7. Scores Moyens Globaux - Enhanced */}
        {shouldShowSection('global-scores') && dashboardData.average_scores && (
          <div 
            className="card" 
            style={{ 
              marginBottom: '40px', 
              boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
              animation: activeView === 'global-scores' ? 'scaleIn 0.5s ease' : 'fadeIn 0.5s ease',
              cursor: 'default'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
              <h2 className="text-gradient" style={{ margin: 0, fontSize: '1.8rem' }}>📈 Scores Moyens Globaux</h2>
              <div style={{ 
                background: 'linear-gradient(135deg, #00f2fe 0%, #4facfe 100%)',
                color: 'white',
                padding: '8px 16px',
                borderRadius: '20px',
                fontSize: '0.9rem',
                fontWeight: 600
              }}>
                Moyenne: {((dashboardData.average_scores.practical + dashboardData.average_scores.logical + dashboardData.average_scores.problem_solving) / 3).toFixed(1)}/100
              </div>
            </div>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart 
                data={[
                  { name: 'Test Pratique', score: dashboardData.average_scores.practical || 0, color: '#4facfe' },
                  { name: 'Raisonnement Logique', score: dashboardData.average_scores.logical || 0, color: '#00f2fe' },
                  { name: 'Résolution Problèmes', score: dashboardData.average_scores.problem_solving || 0, color: '#68d391' }
                ]}
                margin={{ top: 20, right: 30, left: 0, bottom: 20 }}
              >
                <defs>
                  <linearGradient id="scoreGradient1" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#4facfe" stopOpacity={0.9}/>
                    <stop offset="95%" stopColor="#00f2fe" stopOpacity={0.9}/>
                  </linearGradient>
                  <linearGradient id="scoreGradient2" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#00f2fe" stopOpacity={0.9}/>
                    <stop offset="95%" stopColor="#68d391" stopOpacity={0.9}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis 
                  dataKey="name" 
                  tick={{ fill: '#718096', fontSize: 12 }}
                />
                <YAxis 
                  domain={[0, 100]} 
                  tick={{ fill: '#718096' }}
                  label={{ value: 'Score (0-100)', angle: -90, position: 'insideLeft', fill: '#4a5568' }}
                />
                <Tooltip 
                  formatter={(value) => [`${parseFloat(value).toFixed(1)}/100`, 'Score']}
                  contentStyle={{ 
                    background: 'rgba(255, 255, 255, 0.95)', 
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px'
                  }}
                />
                <Bar dataKey="score" radius={[8, 8, 0, 0]} animationDuration={1000}>
                  <Cell fill="url(#scoreGradient1)" />
                  <Cell fill="url(#scoreGradient2)" />
                  <Cell fill="#68d391" />
                </Bar>
              </BarChart>
            </ResponsiveContainer>
            {/* Score Cards */}
            <div style={{ 
              marginTop: '24px', 
              display: 'grid',
              gridTemplateColumns: 'repeat(3, 1fr)',
              gap: '16px'
            }}>
              {[
                { label: 'Test Pratique', score: dashboardData.average_scores.practical || 0, color: '#4facfe', icon: '💼' },
                { label: 'Raisonnement Logique', score: dashboardData.average_scores.logical || 0, color: '#00f2fe', icon: '🧠' },
                { label: 'Résolution Problèmes', score: dashboardData.average_scores.problem_solving || 0, color: '#68d391', icon: '🔧' }
              ].map((item, index) => (
                <div 
                  key={index}
                  style={{ 
                    padding: '20px',
                    background: `linear-gradient(135deg, ${item.color}15 0%, ${item.color}05 100%)`,
                    borderRadius: '12px',
                    border: `2px solid ${item.color}40`,
                    textAlign: 'center'
                  }}
                >
                  <div style={{ fontSize: '2rem', marginBottom: '8px' }}>{item.icon}</div>
                  <div style={{ fontSize: '2rem', fontWeight: 800, color: item.color, marginBottom: '4px' }}>
                    {item.score.toFixed(1)}
                  </div>
                  <div style={{ fontSize: '0.9rem', color: '#718096', fontWeight: 600 }}>
                    {item.label}
                  </div>
                  <div style={{ 
                    marginTop: '8px',
                    width: '100%',
                    height: '8px',
                    background: '#e2e8f0',
                    borderRadius: '4px',
                    overflow: 'hidden'
                  }}>
                    <div style={{
                      width: `${item.score}%`,
                      height: '100%',
                      background: `linear-gradient(90deg, ${item.color} 0%, ${item.color}dd 100%)`,
                      transition: 'width 1s ease'
                    }} />
                  </div>
                </div>
              ))}
            </div>
          </div>
        )}

        {/* 8. Évolution des Questions - Line Chart - Enhanced */}
        {shouldShowSection('evolution') && questionData.length > 0 && (
          <div 
            className="card" 
            style={{ 
              marginBottom: '40px', 
              boxShadow: '0 10px 30px rgba(0,0,0,0.1)',
              animation: activeView === 'evolution' ? 'scaleIn 0.5s ease' : 'fadeIn 0.5s ease',
              cursor: 'default'
            }}
            onClick={(e) => e.stopPropagation()}
          >
            <div style={{ display: 'flex', alignItems: 'center', justifyContent: 'space-between', marginBottom: '24px' }}>
              <h2 className="text-gradient" style={{ margin: 0, fontSize: '1.8rem' }}>📉 Évolution des Scores par Question</h2>
              <div style={{ 
                background: 'linear-gradient(135deg, #f093fb 0%, #fc8181 100%)',
                color: 'white',
                padding: '8px 16px',
                borderRadius: '20px',
                fontSize: '0.9rem',
                fontWeight: 600
              }}>
                Tendance: {parseFloat(questionData[questionData.length - 1]?.score || 0) > parseFloat(questionData[0]?.score || 0) ? '📈' : '📉'} 
                {((parseFloat(questionData[questionData.length - 1]?.score || 0) - parseFloat(questionData[0]?.score || 0)) * 100).toFixed(1)}%
              </div>
            </div>
            <ResponsiveContainer width="100%" height={450}>
              <LineChart data={questionData} margin={{ top: 20, right: 30, left: 0, bottom: 80 }}>
                <defs>
                  <linearGradient id="lineGradient" x1="0" y1="0" x2="0" y2="1">
                    <stop offset="5%" stopColor="#f093fb" stopOpacity={0.3}/>
                    <stop offset="95%" stopColor="#f093fb" stopOpacity={0.05}/>
                  </linearGradient>
                </defs>
                <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                <XAxis 
                  dataKey="question" 
                  angle={-45} 
                  textAnchor="end" 
                  height={100}
                  tick={{ fill: '#718096', fontSize: 11 }}
                />
                <YAxis 
                  domain={[0, 3]}
                  tick={{ fill: '#718096' }}
                  label={{ value: 'Score moyen (0-3)', angle: -90, position: 'insideLeft', fill: '#4a5568' }}
                />
                <Tooltip 
                  formatter={(value) => [`Score: ${parseFloat(value).toFixed(2)}/3`, '']}
                  contentStyle={{ 
                    background: 'rgba(255, 255, 255, 0.95)', 
                    border: '1px solid #e2e8f0',
                    borderRadius: '8px'
                  }}
                />
                <Area 
                  type="monotone" 
                  dataKey="score" 
                  stroke="none" 
                  fill="url(#lineGradient)"
                />
                <Line 
                  type="monotone" 
                  dataKey="score" 
                  stroke="#f093fb" 
                  strokeWidth={4}
                  dot={{ fill: '#f093fb', r: 5, strokeWidth: 2, stroke: '#fff' }}
                  activeDot={{ r: 8, fill: '#fc8181', stroke: '#fff', strokeWidth: 2 }}
                  animationDuration={1500}
                />
              </LineChart>
            </ResponsiveContainer>
            {/* Trend Analysis */}
            <div style={{ 
              marginTop: '24px', 
              padding: '20px', 
              background: 'linear-gradient(135deg, #f7fafc 0%, #edf2f7 100%)',
              borderRadius: '12px',
              display: 'grid',
              gridTemplateColumns: 'repeat(4, 1fr)',
              gap: '16px'
            }}>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#f093fb' }}>
                  {parseFloat(questionData[0]?.score || 0).toFixed(2)}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#718096', marginTop: '4px' }}>Début (Q1)</div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#fc8181' }}>
                  {parseFloat(questionData[questionData.length - 1]?.score || 0).toFixed(2)}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#718096', marginTop: '4px' }}>Fin (Q25)</div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#764ba2' }}>
                  {(Math.max(...questionData.map(q => parseFloat(q.score))) - Math.min(...questionData.map(q => parseFloat(q.score)))).toFixed(2)}
                </div>
                <div style={{ fontSize: '0.85rem', color: '#718096', marginTop: '4px' }}>Écart Max-Min</div>
              </div>
              <div style={{ textAlign: 'center' }}>
                <div style={{ fontSize: '1.2rem', fontWeight: 700, color: '#4facfe' }}>
                  {((parseFloat(questionData[questionData.length - 1]?.score || 0) - parseFloat(questionData[0]?.score || 0)) > 0 ? '+' : '') + 
                   ((parseFloat(questionData[questionData.length - 1]?.score || 0) - parseFloat(questionData[0]?.score || 0)) * 100).toFixed(1)}%
                </div>
                <div style={{ fontSize: '0.85rem', color: '#718096', marginTop: '4px' }}>Évolution</div>
              </div>
            </div>
          </div>
        )}
        </div>
      </div>
    </div>
  );
}

export default AdminDashboard;
