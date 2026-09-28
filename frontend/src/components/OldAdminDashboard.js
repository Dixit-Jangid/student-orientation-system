import React, { useState, useEffect } from 'react';
import api from '../services/api';
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, PieChart, Pie, Cell } from 'recharts';

function OldAdminDashboard({ user, onLogout, onBackToNew }) {
  const [dashboardData, setDashboardData] = useState(null);
  const [loading, setLoading] = useState(true);
  const [summary, setSummary] = useState(null);
  const [reportFiles, setReportFiles] = useState([]);
  const [retrainStatus, setRetrainStatus] = useState(null);

  useEffect(() => {
    fetchAdminData();
    fetchSummary();
    fetchReportFiles();
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

  const fetchSummary = async () => {
    try {
      const response = await api.get('/api/dashboard/ml/summary');
      setSummary(response.data);
    } catch (e) {
      console.warn('No ML summary yet');
    }
  };

  const fetchReportFiles = async () => {
    try {
      const response = await api.get('/api/dashboard/ml/list-reports');
      setReportFiles(response.data.files || []);
    } catch (e) {
      setReportFiles([]);
    }
  };

  const triggerRetrain = async () => {
    setRetrainStatus('starting');
    try {
      await api.post('/api/dashboard/ml/retrain');
      setRetrainStatus('started');
    } catch (e) {
      setRetrainStatus('error');
    }
  };

  if (loading) {
    return <div className="loading">Loading admin dashboard...</div>;
  }

  if (!dashboardData) {
    return <div className="error">Unable to load dashboard data.</div>;
  }

  const filiereChartData = dashboardData.filiere_distribution?.map(d => ({
    name: d.filiere.substring(0, 20),
    count: d.count
  })) || [];

  const specChartData = dashboardData.top_specializations?.slice(0, 10).map(d => ({
    name: d.specialization.substring(0, 15),
    count: d.count
  })) || [];

  const featureChartData = dashboardData.feature_importance?.slice(0, 10).map(d => ({
    name: d.feature.substring(0, 15),
    importance: d.importance * 100
  })) || [];

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-content">
          <h1>UniGuide Admin - ML Monitoring</h1>
          <div className="navbar-actions">
            {onBackToNew && (
              <button 
                onClick={onBackToNew} 
                className="btn btn-primary"
                style={{ marginRight: '12px' }}
              >
                📊 Nouveau Dashboard
              </button>
            )}
            <button onClick={onLogout} className="btn btn-secondary">Logout</button>
          </div>
        </div>
      </nav>

      <div className="container">
        {/* Actions */}
        <div className="card" style={{ marginBottom: '24px' }}>
          <h2 className="text-gradient" style={{ marginBottom: '12px' }}>Actions</h2>
          <div style={{ display: 'flex', gap: '12px', flexWrap: 'wrap' }}>
            <button onClick={triggerRetrain} className="btn btn-primary">
              {retrainStatus === 'starting' ? 'Starting...' : 'Retrain model'}
            </button>
            {retrainStatus === 'started' && <div className="success">Retraining started in the background.</div>}
            {retrainStatus === 'error' && <div className="error">Unable to start retraining.</div>}
          </div>
        </div>

        {/* Statistics Cards */}
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '24px', marginBottom: '32px' }}>
          <div className="stat-card">
            <h3>Utilisateurs</h3>
            <p>{dashboardData.total_users}</p>
          </div>
          <div className="stat-card">
            <h3>Tests</h3>
            <p>{dashboardData.total_tests}</p>
          </div>
          <div className="stat-card">
            <h3>Dataset</h3>
            <p style={{ fontSize: '2rem' }}>{dashboardData.dataset_stats?.total_rows?.toLocaleString() || 0} lignes</p>
          </div>
          <div className="stat-card">
            <h3>Accuracy</h3>
            <p>{(dashboardData.model_performance?.test_accuracy * 100 || 0).toFixed(1)}%</p>
          </div>
        </div>

        {/* Model Performance */}
        <div className="card">
          <h2 className="text-gradient" style={{ marginBottom: '24px' }}>
            Performance du Modèle ML
            {dashboardData.model_performance?.best_model_name && (
              <span style={{ fontSize: '0.8em', color: '#667eea', marginLeft: '12px', fontWeight: 400 }}>
                ({dashboardData.model_performance.best_model_name})
              </span>
            )}
          </h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(180px, 1fr))', gap: '20px' }}>
            <div className="stat-card">
              <h4 style={{ color: '#718096', fontSize: '0.875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>Test Accuracy</h4>
              <p style={{ fontSize: '2rem', fontWeight: 800, margin: 0 }}>
                {(dashboardData.model_performance?.test_accuracy * 100 || 0).toFixed(2)}%
              </p>
            </div>
            <div className="stat-card">
              <h4 style={{ color: '#718096', fontSize: '0.875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>Precision</h4>
              <p style={{ fontSize: '2rem', fontWeight: 800, margin: 0 }}>
                {(dashboardData.model_performance?.precision * 100 || 0).toFixed(2)}%
              </p>
            </div>
            <div className="stat-card">
              <h4 style={{ color: '#718096', fontSize: '0.875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>Recall</h4>
              <p style={{ fontSize: '2rem', fontWeight: 800, margin: 0 }}>
                {(dashboardData.model_performance?.recall * 100 || 0).toFixed(2)}%
              </p>
            </div>
            <div className="stat-card">
              <h4 style={{ color: '#718096', fontSize: '0.875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>F1-Score</h4>
              <p style={{ fontSize: '2rem', fontWeight: 800, margin: 0 }}>
                {(dashboardData.model_performance?.f1_score * 100 || 0).toFixed(2)}%
              </p>
            </div>
            {dashboardData.model_performance?.overfitting !== undefined && (
              <div className="stat-card">
                <h4 style={{ color: '#718096', fontSize: '0.875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>Overfitting</h4>
                <p style={{ 
                  fontSize: '2rem', 
                  fontWeight: 800, 
                  margin: 0,
                  color: (dashboardData.model_performance.overfitting * 100) > 10 ? '#e53e3e' : '#38a169'
                }}>
                  {(dashboardData.model_performance.overfitting * 100).toFixed(2)}%
                </p>
              </div>
            )}
          </div>
        </div>

        {/* Filière Distribution */}
        {filiereChartData.length > 0 && (
          <div className="card">
            <h3 className="text-gradient" style={{ marginBottom: '24px' }}>Path Distribution</h3>
            <ResponsiveContainer width="100%" height={300}>
              <BarChart data={filiereChartData}>
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis dataKey="name" angle={-45} textAnchor="end" height={100} />
                <YAxis />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#667eea" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Dataset Overview */}
        <div className="card">
          <h2 className="text-gradient" style={{ marginBottom: '24px' }}>Aperçu du Dataset</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px', marginBottom: '32px' }}>
            <div className="stat-card">
              <h4 style={{ color: '#718096', fontSize: '0.875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>Lignes (Avant)</h4>
              <p style={{ fontSize: '2rem', fontWeight: 800, margin: 0 }}>
                {dashboardData.dataset_stats?.total_rows?.toLocaleString() || 0}
              </p>
            </div>
            <div className="stat-card">
              <h4 style={{ color: '#718096', fontSize: '0.875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>Lignes (Après)</h4>
              <p style={{ fontSize: '2rem', fontWeight: 800, margin: 0 }}>
                {dashboardData.dataset_stats?.rows_after_cleaning?.toLocaleString() || dashboardData.dataset_stats?.total_rows?.toLocaleString() || 0}
              </p>
            </div>
            <div className="stat-card">
              <h4 style={{ color: '#718096', fontSize: '0.875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>Valeurs Manquantes (Avant)</h4>
              <p style={{ fontSize: '2rem', fontWeight: 800, margin: 0 }}>
                {dashboardData.dataset_stats?.missing_values?.toLocaleString() || 0}
              </p>
            </div>
            <div className="stat-card">
              <h4 style={{ color: '#718096', fontSize: '0.875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>Valeurs Manquantes (Après)</h4>
              <p style={{ fontSize: '2rem', fontWeight: 800, margin: 0 }}>
                {dashboardData.dataset_stats?.missing_after_cleaning?.toLocaleString() || 0}
              </p>
            </div>
            <div className="stat-card">
              <h4 style={{ color: '#718096', fontSize: '0.875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>Colonnes</h4>
              <p style={{ fontSize: '2rem', fontWeight: 800, margin: 0 }}>
                {dashboardData.dataset_stats?.columns || 0}
              </p>
            </div>
            <div className="stat-card">
              <h4 style={{ color: '#718096', fontSize: '0.875rem', fontWeight: 600, textTransform: 'uppercase', letterSpacing: '0.5px', marginBottom: '12px' }}>Doublons</h4>
              <p style={{ fontSize: '2rem', fontWeight: 800, margin: 0 }}>
                {dashboardData.dataset_stats?.duplicates?.toLocaleString() || 0}
              </p>
            </div>
          </div>
          
          {/* Data Cleaning Summary Table */}
          {dashboardData.cleaning_summary && dashboardData.cleaning_summary.length > 0 && (
            <div style={{ marginTop: '32px' }}>
              <h3 className="text-gradient" style={{ marginBottom: '20px' }}>Résumé du Nettoyage des Données</h3>
              <div style={{ overflowX: 'auto' }}>
                <table style={{ width: '100%', borderCollapse: 'collapse', background: '#f8f9fa', borderRadius: '8px', overflow: 'hidden' }}>
                  <thead>
                    <tr style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                      <th style={{ padding: '12px', textAlign: 'left', fontWeight: 600 }}>Métrique</th>
                      <th style={{ padding: '12px', textAlign: 'right', fontWeight: 600 }}>Avant</th>
                      <th style={{ padding: '12px', textAlign: 'right', fontWeight: 600 }}>Après</th>
                      <th style={{ padding: '12px', textAlign: 'right', fontWeight: 600 }}>Différence</th>
                    </tr>
                  </thead>
                  <tbody>
                    {dashboardData.cleaning_summary.map((row, index) => (
                      <tr key={index} style={{ borderBottom: '1px solid #e2e8f0' }}>
                        <td style={{ padding: '12px', fontWeight: 600, color: '#1a202c' }}>{row.Metric || row.metric}</td>
                        <td style={{ padding: '12px', textAlign: 'right', color: '#718096' }}>
                          {typeof row.Before === 'number' ? row.Before.toLocaleString() : row.Before || row.before || 'N/A'}
                        </td>
                        <td style={{ padding: '12px', textAlign: 'right', color: '#718096' }}>
                          {typeof row.After === 'number' ? row.After.toLocaleString() : row.After || row.after || 'N/A'}
                        </td>
                        <td style={{ 
                          padding: '12px', 
                          textAlign: 'right', 
                          fontWeight: 600,
                          color: typeof row.Difference === 'number' && row.Difference < 0 ? '#38a169' : '#1a202c'
                        }}>
                          {typeof row.Difference === 'number' ? (row.Difference < 0 ? '' : '+') + row.Difference.toLocaleString() : row.Difference || row.difference || 'N/A'}
                        </td>
                      </tr>
                    ))}
                  </tbody>
                </table>
              </div>
            </div>
          )}
        </div>
        
        {/* Model Comparison */}
        {dashboardData.model_comparison && dashboardData.model_comparison.length > 0 && (
          <div className="card">
            <h2 className="text-gradient" style={{ marginBottom: '24px' }}>Comparaison des Modèles</h2>
            <div style={{ overflowX: 'auto' }}>
              <table style={{ width: '100%', borderCollapse: 'collapse', background: '#f8f9fa', borderRadius: '8px', overflow: 'hidden' }}>
                <thead>
                  <tr style={{ background: 'linear-gradient(135deg, #667eea 0%, #764ba2 100%)', color: 'white' }}>
                    <th style={{ padding: '12px', textAlign: 'left', fontWeight: 600 }}>Modèle</th>
                    <th style={{ padding: '12px', textAlign: 'right', fontWeight: 600 }}>Train Accuracy</th>
                    <th style={{ padding: '12px', textAlign: 'right', fontWeight: 600 }}>Test Accuracy</th>
                    <th style={{ padding: '12px', textAlign: 'right', fontWeight: 600 }}>Precision</th>
                    <th style={{ padding: '12px', textAlign: 'right', fontWeight: 600 }}>Recall</th>
                    <th style={{ padding: '12px', textAlign: 'right', fontWeight: 600 }}>F1-Score</th>
                    <th style={{ padding: '12px', textAlign: 'right', fontWeight: 600 }}>Overfitting</th>
                  </tr>
                </thead>
                <tbody>
                  {dashboardData.model_comparison.map((model, index) => (
                    <tr 
                      key={index} 
                      style={{ 
                        borderBottom: '1px solid #e2e8f0',
                        background: index === 0 ? 'rgba(102, 126, 234, 0.05)' : 'white'
                      }}
                    >
                      <td style={{ padding: '12px', fontWeight: index === 0 ? 700 : 600, color: index === 0 ? '#667eea' : '#1a202c' }}>
                        {model.Model || model.model} {index === 0 && '🏆'}
                      </td>
                      <td style={{ padding: '12px', textAlign: 'right', color: '#718096' }}>
                        {((model['Train Accuracy'] || model.train_accuracy || 0) * 100).toFixed(2)}%
                      </td>
                      <td style={{ padding: '12px', textAlign: 'right', fontWeight: 600, color: '#1a202c' }}>
                        {((model['Test Accuracy'] || model.test_accuracy || 0) * 100).toFixed(2)}%
                      </td>
                      <td style={{ padding: '12px', textAlign: 'right', color: '#718096' }}>
                        {((model.Precision || model.precision || 0) * 100).toFixed(2)}%
                      </td>
                      <td style={{ padding: '12px', textAlign: 'right', color: '#718096' }}>
                        {((model.Recall || model.recall || 0) * 100).toFixed(2)}%
                      </td>
                      <td style={{ padding: '12px', textAlign: 'right', color: '#718096' }}>
                        {((model['F1-Score'] || model.f1_score || 0) * 100).toFixed(2)}%
                      </td>
                      <td style={{ 
                        padding: '12px', 
                        textAlign: 'right', 
                        fontWeight: 600,
                        color: (model.Overfitting || model.overfitting || 0) > 0.1 ? '#e53e3e' : '#38a169'
                      }}>
                        {((model.Overfitting || model.overfitting || 0) * 100).toFixed(2)}%
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        )}

        {/* Specialization Distribution */}
        {specChartData.length > 0 && (
          <div className="card">
            <h3 className="text-gradient" style={{ marginBottom: '24px' }}>Top 10 Predicted Specializations</h3>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={specChartData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" width={150} />
                <Tooltip />
                <Legend />
                <Bar dataKey="count" fill="#764ba2" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Feature Importance */}
        {featureChartData.length > 0 && (
          <div className="card">
            <h3 className="text-gradient" style={{ marginBottom: '24px' }}>Top 10 Features les Plus Importantes</h3>
            <ResponsiveContainer width="100%" height={400}>
              <BarChart data={featureChartData} layout="vertical">
                <CartesianGrid strokeDasharray="3 3" />
                <XAxis type="number" />
                <YAxis dataKey="name" type="category" width={150} />
                <Tooltip />
                <Legend />
                <Bar dataKey="importance" fill="#f093fb" />
              </BarChart>
            </ResponsiveContainer>
          </div>
        )}

        {/* Average Scores */}
        {dashboardData.average_scores && (
          <div className="card">
            <h3 className="text-gradient" style={{ marginBottom: '24px' }}>Scores Moyens</h3>
            <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '20px' }}>
              <div>
                <h4>Practical Test</h4>
                <p style={{ fontSize: '1.5em', fontWeight: 'bold' }}>
                  {dashboardData.average_scores.practical?.toFixed(1) || 0}/100
                </p>
              </div>
              <div>
                <h4>Raisonnement Logique</h4>
                <p style={{ fontSize: '1.5em', fontWeight: 'bold' }}>
                  {dashboardData.average_scores.logical?.toFixed(1) || 0}/100
                </p>
              </div>
              <div>
                <h4>Problem Solving</h4>
                <p style={{ fontSize: '1.5em', fontWeight: 'bold' }}>
                  {dashboardData.average_scores.problem_solving?.toFixed(1) || 0}/100
                </p>
              </div>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}

export default OldAdminDashboard;

