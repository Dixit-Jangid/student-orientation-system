import React, { useState, useEffect } from 'react';
import { Link } from 'react-router-dom';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';
import api from '../services/api';

function Progress({ user }) {
  const [progress, setProgress] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchProgress();
  }, []);

  const fetchProgress = async () => {
    try {
      const response = await api.get('/api/progress');
      setProgress(response.data);
      setLoading(false);
    } catch (error) {
      console.error('Error fetching progress:', error);
      setLoading(false);
    }
  };

  if (loading) {
    return <div className="loading">Loading progress...</div>;
  }

  if (!progress || progress.message) {
    return (
      <div>
        <nav className="navbar">
          <div className="navbar-content">
            <h1>Progress</h1>
            <Link to="/dashboard" className="btn btn-secondary">
              Dashboard
            </Link>
          </div>
        </nav>
        <div className="container">
          <div className="card">
            <p style={{ textAlign: 'center', color: '#666' }}>
              No progress data is available yet. Complete assessments to track your progress.
            </p>
            <Link to="/dashboard" className="btn btn-primary" style={{ display: 'block', textAlign: 'center', marginTop: '20px' }}>
              Take an assessment
            </Link>
          </div>
        </div>
      </div>
    );
  }

  const chartData = progress.history?.map((h, index) => ({
    name: `Test ${index + 1}`,
    Level: h.current_level,
    Score: h.practical_test_score,
  })) || [];

  return (
    <div>
      <nav className="navbar">
        <div className="navbar-content">
          <h1>Progress</h1>
          <Link to="/dashboard" className="btn btn-secondary">
            Dashboard
          </Link>
        </div>
      </nav>

      <div className="container">
        <div className="card">
          <h2 className="text-gradient" style={{ marginBottom: '32px' }}>
            Progress Analysis
          </h2>

          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(220px, 1fr))', gap: '24px', marginBottom: '32px' }}>
            <div className="stat-card">
              <h3>Assessments completed</h3>
              <p>{progress.total_tests || 0}</p>
            </div>
            <div className="stat-card">
              <h3>Current level</h3>
              <p>{progress.current_level || 0}/5</p>
            </div>
            <div className="stat-card">
              <h3>Average score</h3>
              <p>{progress.average_score ? progress.average_score.toFixed(1) : 0}/100</p>
            </div>
            <div className="stat-card">
              <h3>Tendance</h3>
              <p style={{ fontSize: '1.5rem', marginTop: '12px' }}>
                {progress.level_trend === 'improving' ? '📈 Improving' :
                 progress.level_trend === 'stable' ? '➡️ Stable' : '📉 Declining'}
              </p>
            </div>
          </div>

          {chartData.length > 0 ? (
            <div style={{ marginTop: '32px' }}>
              <h3 className="text-gradient" style={{ marginBottom: '24px' }}>
                Level and Score Trends
              </h3>
              <div style={{ background: '#f8f9fa', padding: '24px', borderRadius: '12px' }}>
                <ResponsiveContainer width="100%" height={400}>
                  <LineChart data={chartData} margin={{ top: 5, right: 30, left: 20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#e2e8f0" />
                    <XAxis 
                      dataKey="name" 
                      tick={{ fill: '#718096', fontSize: 12, fontWeight: 600 }}
                      stroke="#cbd5e0"
                    />
                    <YAxis 
                      tick={{ fill: '#718096', fontSize: 12 }}
                      stroke="#cbd5e0"
                    />
                    <Tooltip 
                      contentStyle={{
                        backgroundColor: 'white',
                        border: '1px solid #e2e8f0',
                        borderRadius: '8px',
                        boxShadow: '0 4px 6px rgba(0, 0, 0, 0.1)'
                      }}
                    />
                    <Legend 
                      wrapperStyle={{ paddingTop: '20px' }}
                      iconType="line"
                    />
                    <Line 
                      type="monotone" 
                      dataKey="Level"
                      stroke="#667eea" 
                      strokeWidth={3}
                      dot={{ fill: '#667eea', r: 6 }}
                      activeDot={{ r: 8 }}
                      name="Level"
                    />
                    <Line 
                      type="monotone" 
                      dataKey="Score" 
                      stroke="#764ba2" 
                      strokeWidth={3}
                      dot={{ fill: '#764ba2', r: 6 }}
                      activeDot={{ r: 8 }}
                      name="Score (/100)"
                    />
                  </LineChart>
                </ResponsiveContainer>
              </div>
            </div>
          ) : (
            <div className="stat-card" style={{ textAlign: 'center', padding: '40px' }}>
              <h3 className="text-gradient" style={{ marginBottom: '16px' }}>
                No progress data available
              </h3>
              <p style={{ color: '#718096', marginBottom: '24px' }}>
                Complete more assessments to see your progress on the chart
              </p>
            </div>
          )}

          {progress.improvement_rate !== undefined && (
            <div style={{ marginTop: '30px', padding: '20px', background: '#f8f9fa', borderRadius: '8px' }}>
              <h3 style={{ color: '#667eea', marginBottom: '10px' }}>Improvement rate</h3>
              <p style={{ fontSize: '1.5em', fontWeight: 'bold' }}>
                {(progress.improvement_rate * 100).toFixed(1)}%
              </p>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default Progress;

