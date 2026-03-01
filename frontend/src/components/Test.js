import React, { useState, useEffect } from 'react';
import { useNavigate, useSearchParams } from 'react-router-dom';
import api from '../services/api';

function Test({ user }) {
  const [searchParams] = useSearchParams();
  const filiere = searchParams.get('filiere');
  const navigate = useNavigate();

  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [currentQuestion, setCurrentQuestion] = useState(0);
  const [loading, setLoading] = useState(true);
  const [submitting, setSubmitting] = useState(false);
  const [error, setError] = useState(null);
  const [scores, setScores] = useState({
    practical_test_score: 0,
    logical_reasoning_score: 0,
    problem_solving_score: 0,
    time_spent_minutes: 0,
  });

  useEffect(() => {
    if (!filiere) {
      // Redirect to select filiere if not provided
      navigate('/select-filiere');
      return;
    }
    fetchQuestions();
    const startTime = Date.now();
    return () => {
      const timeSpent = Math.round((Date.now() - startTime) / 60000);
      setScores((prev) => ({ ...prev, time_spent_minutes: timeSpent }));
    };
  }, [filiere, navigate]);

  const fetchQuestions = async () => {
    try {
      setError(null);
      const response = await api.get(`/api/questions/${encodeURIComponent(filiere)}`);
      if (response.data && response.data.length > 0) {
        setQuestions(response.data);
      } else {
        setError('Aucune question disponible pour cette filière');
      }
      setLoading(false);
    } catch (error) {
      console.error('Error fetching questions:', error);
      setError('Erreur lors du chargement des questions. Veuillez réessayer.');
      setLoading(false);
    }
  };

  const handleAnswer = (questionId, answerIndex) => {
    setAnswers({ ...answers, [questionId]: answerIndex });
  };

  const handleNext = () => {
    if (currentQuestion < questions.length - 1) {
      setCurrentQuestion(currentQuestion + 1);
    }
  };

  const handlePrevious = () => {
    if (currentQuestion > 0) {
      setCurrentQuestion(currentQuestion - 1);
    }
  };

  const handleCancelTest = () => {
    if (window.confirm('Êtes-vous sûr de vouloir annuler ce test ? Vos réponses ne seront pas sauvegardées.')) {
      navigate('/dashboard');
    }
  };

  const handleSubmit = async () => {
    if (submitting) return; // Prevent double submission
    
    setSubmitting(true);
    setError(null);

    try {
      console.log('[TEST] Starting submission...');
      console.log('[TEST] Filiere:', filiere);
      console.log('[TEST] Answers:', answers);
      console.log('[TEST] Number of answers:', Object.keys(answers).length);
      console.log('[TEST] Number of questions:', questions.length);

      // Calculate scores based on answers
      // Answer values are 0-3 (indices), we'll use them directly as scores
      const totalQuestions = questions.length;
      const answeredQuestions = Object.keys(answers).length;
      
      // Calculate average answer value (0-3 scale)
      const totalAnswerValue = Object.values(answers).reduce((sum, val) => sum + (val || 0), 0);
      const avgAnswerValue = answeredQuestions > 0 ? totalAnswerValue / answeredQuestions : 0;
      
      // Convert to 0-100 scale (multiply by 33.33 to get max 100)
      const practicalScore = Math.min(100, (avgAnswerValue / 3) * 100);
      const logicalScore = Math.min(100, practicalScore + (Math.random() * 10 - 5));
      const problemScore = Math.min(100, practicalScore + (Math.random() * 10 - 5));

      console.log('[TEST] Calculated scores:', {
        practical: practicalScore,
        logical: logicalScore,
        problem: problemScore,
        time: scores.time_spent_minutes || 30
      });

      // Ensure all questions have an answer (default to 0 if not answered)
      const completeAnswers = {};
      questions.forEach((q) => {
        completeAnswers[q.id] = answers[q.id] !== undefined ? answers[q.id] : 0;
      });

      console.log('[TEST] Complete answers:', completeAnswers);

      const response = await api.post('/api/predict', {
        filiere: filiere,
        answers: completeAnswers,
        practical_test_score: practicalScore,
        logical_reasoning_score: logicalScore,
        problem_solving_score: problemScore,
        time_spent_minutes: scores.time_spent_minutes || 30,
      });

      console.log('[TEST] Submission successful:', response.data);

      if (response.data && response.data.test_id) {
        navigate(`/results/${response.data.test_id}`, {
          state: { prediction: response.data },
        });
      } else {
        throw new Error('Réponse invalide du serveur');
      }
    } catch (error) {
      console.error('[TEST] Error submitting test:', error);
      console.error('[TEST] Error response:', error.response);
      const errorMessage = error.response?.data?.detail || error.response?.data?.message || error.message || 'Erreur lors de la soumission du test';
      setError(`Erreur: ${errorMessage}`);
      setSubmitting(false);
    }
  };

  if (loading) {
    return <div className="loading">Chargement des questions...</div>;
  }

  if (error) {
    return (
      <div className="container" style={{ maxWidth: '800px', marginTop: '50px' }}>
        <div className="card">
          <div className="error">{error}</div>
          <button 
            onClick={() => navigate('/select-filiere')} 
            className="btn btn-primary"
            style={{ marginTop: '20px' }}
          >
            Retour au choix de filière
          </button>
        </div>
      </div>
    );
  }

  if (questions.length === 0) {
    return (
      <div className="container" style={{ maxWidth: '800px', marginTop: '50px' }}>
        <div className="card">
          <div className="error">Aucune question disponible pour cette filière</div>
          <button 
            onClick={() => navigate('/select-filiere')} 
            className="btn btn-primary"
            style={{ marginTop: '20px' }}
          >
            Retour au choix de filière
          </button>
        </div>
      </div>
    );
  }

  const question = questions[currentQuestion];
  const progress = ((currentQuestion + 1) / questions.length) * 100;

  return (
    <div className="container">
      <div className="card">
        <div style={{ 
          display: 'flex', 
          justifyContent: 'space-between', 
          alignItems: 'center',
          marginBottom: '20px'
        }}>
          <h2 style={{ margin: 0, color: '#667eea' }}>
            Test de Spécialisation - {filiere}
          </h2>
          <button
            onClick={handleCancelTest}
            style={{
              padding: '10px 20px',
              background: 'linear-gradient(135deg, #fc8181 0%, #f56565 100%)',
              color: 'white',
              border: 'none',
              borderRadius: '12px',
              fontSize: '0.95rem',
              fontWeight: 600,
              cursor: 'pointer',
              boxShadow: '0 4px 15px rgba(245, 101, 101, 0.3)',
              transition: 'all 0.3s ease',
              display: 'flex',
              alignItems: 'center',
              gap: '8px'
            }}
            onMouseEnter={(e) => {
              e.currentTarget.style.transform = 'translateY(-2px)';
              e.currentTarget.style.boxShadow = '0 6px 20px rgba(245, 101, 101, 0.4)';
            }}
            onMouseLeave={(e) => {
              e.currentTarget.style.transform = 'translateY(0)';
              e.currentTarget.style.boxShadow = '0 4px 15px rgba(245, 101, 101, 0.3)';
            }}
          >
            <span>✕</span>
            Annuler ce test
          </button>
        </div>

        <div style={{ marginBottom: '20px' }}>
          <div
            style={{
              width: '100%',
              height: '20px',
              background: '#e0e0e0',
              borderRadius: '10px',
              overflow: 'hidden',
            }}
          >
            <div
              style={{
                width: `${progress}%`,
                height: '100%',
                background: 'linear-gradient(90deg, #667eea, #764ba2)',
                transition: 'width 0.3s',
              }}
            />
          </div>
          <p style={{ textAlign: 'center', marginTop: '10px' }}>
            Question {currentQuestion + 1} sur {questions.length}
          </p>
        </div>

        <div className="question-card">
          <h3>{question.question}</h3>
          <p style={{ color: '#666', marginBottom: '15px', fontSize: '14px' }}>
            Compétence: {question.skill}
          </p>
          <div>
            {question.options.map((option, index) => (
              <div
                key={index}
                className={`option ${answers[question.id] === index ? 'selected' : ''}`}
                onClick={() => handleAnswer(question.id, index)}
              >
                {option}
              </div>
            ))}
          </div>
        </div>

        {error && (
          <div className="error" style={{ marginTop: '20px', marginBottom: '10px' }}>
            {error}
          </div>
        )}

        <div style={{ display: 'flex', justifyContent: 'space-between', marginTop: '20px' }}>
          <button
            className="btn btn-secondary"
            onClick={handlePrevious}
            disabled={currentQuestion === 0 || submitting}
          >
            Précédent
          </button>

          {currentQuestion === questions.length - 1 ? (
            <button
              className="btn btn-primary"
              onClick={handleSubmit}
              disabled={submitting}
              style={{ 
                opacity: submitting ? 0.6 : 1,
                cursor: submitting ? 'not-allowed' : 'pointer'
              }}
            >
              {submitting ? 'Soumission en cours...' : 'Soumettre le test'}
            </button>
          ) : (
            <button className="btn btn-primary" onClick={handleNext}>
              Suivant
            </button>
          )}
        </div>
      </div>
    </div>
  );
}

export default Test;

