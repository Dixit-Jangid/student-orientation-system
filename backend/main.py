"""
FastAPI Backend for Specialization Prediction System
"""

from fastapi import FastAPI, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List, Optional, Dict
import joblib
import numpy as np
import pandas as pd
from datetime import datetime
import os
import sys
import subprocess

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from database import get_db, init_db, User, TestResult, PredictionHistory
from auth import get_current_user, create_access_token, verify_password, get_password_hash
from recommendation_system import RecommendationSystem
from questions_bank import get_questions_for_specialization

app = FastAPI(title="Specialization Prediction System")

# Include dashboard routers
try:
    from api_dashboard import router as dashboard_router
    app.include_router(dashboard_router)
except ImportError:
    print("Warning: Dashboard router not available")

try:
    from api_dashboard_ml import router as dashboard_ml_router
    app.include_router(dashboard_ml_router)
except ImportError:
    print("Warning: Dashboard ML router not available")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:5173"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

    # Load ML model - PRIORITY: notebook output (/reports/model), else old path
base_dir = os.path.dirname(os.path.dirname(__file__))
MODEL_PATHS = [
    os.path.join(base_dir, 'reports', 'model', 'best_model.pkl'),  # Notebook output (priority)
    os.path.join(base_dir, 'models', 'best_model.pkl')             # Old path (fallback)
]
model_data = None

FILIERE_ALIASES = {
    "Artificial Intelligence & Data Science": "Intelligence Artificielle & Sciences des Données",
    "Cybersecurity & Network Infrastructure": "Cybersécurité & Infrastructures Réseaux",
    "Digital Development & Information Systems": "Développement Digital & Systèmes d'Information",
}


def canonicalize_filiere(filiere: str) -> str:
    """Keep model-facing path names consistent across old and English UI labels."""
    return FILIERE_ALIASES.get(filiere.strip(), filiere.strip())

def train_model_if_missing():
    project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    training_script = os.path.join(project_root, 'excute', 'run_ml_pipeline.py')
    if os.path.exists(training_script):
        print("[MODEL] No trained model found. Starting training pipeline...")
        subprocess.run([sys.executable, training_script], cwd=project_root, check=False)
    else:
        print(f"[MODEL] Training script not found at: {training_script}")


def load_model():
    global model_data
    if model_data is None:
        for model_path in MODEL_PATHS:
            if os.path.exists(model_path):
                try:
                    model_data = joblib.load(model_path)
                    print(f"[MODEL] Loaded from: {model_path}")
                    break
                except Exception as e:
                    print(f"[MODEL] Error loading from {model_path}: {e}")
                    continue
    if model_data is None:
        print(f"[MODEL] Warning: No model found. Checked paths: {MODEL_PATHS}")
        train_model_if_missing()
        for model_path in MODEL_PATHS:
            if os.path.exists(model_path):
                try:
                    model_data = joblib.load(model_path)
                    print(f"[MODEL] Loaded after training from: {model_path}")
                    break
                except Exception as e:
                    print(f"[MODEL] Error loading after training from {model_path}: {e}")
                    continue
    return model_data

# Initialize database
@app.on_event("startup")
async def startup_event():
    init_db()
    load_model()

# Pydantic models
class UserCreate(BaseModel):
    username: str
    email: str
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: str
    
    class Config:
        from_attributes = True

class TestSubmission(BaseModel):
    filiere: str
    answers: Dict[str, int]  # question_id: answer (0-3)
    practical_test_score: float
    logical_reasoning_score: float
    problem_solving_score: float
    time_spent_minutes: float

class PredictionResponse(BaseModel):
    predicted_specialization: str  # Top 1
    confidence: float
    top_3_specializations: List[Dict]  # Top 3 alternatives with confidence
    recommendations: Dict
    test_id: int

class QuestionResponse(BaseModel):
    id: str
    question: str
    options: List[str]
    skill: str

# Routes
@app.get("/")
async def root():
    return {"message": "Specialization Prediction API"}

@app.post("/api/register", response_model=UserResponse)
async def register(user_data: UserCreate, db: Session = Depends(get_db)):
    """Register a new user"""
    # Check if user exists
    existing_user = db.query(User).filter(User.username == user_data.username).first()
    if existing_user:
        raise HTTPException(status_code=400, detail="Username already exists")
    
    # Create new user
    hashed_password = get_password_hash(user_data.password)
    print(f"[REGISTER] Creating user: {user_data.username}")
    print(f"[REGISTER] Password hash: {hashed_password}")
    
    new_user = User(
        username=user_data.username,
        email=user_data.email,
        hashed_password=hashed_password,
        role="user"  # Default role is user
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    print(f"[REGISTER] User created successfully: id={new_user.id}, username={new_user.username}")
    print(f"[REGISTER] Stored hash in DB: {new_user.hashed_password}")
    
    return new_user

@app.post("/api/login")
async def login(form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    """Login and get access token with redirection info"""
    # Debug logging
    print(f"[LOGIN] Attempting login for username: {form_data.username}")
    
    user = db.query(User).filter(User.username == form_data.username).first()
    
    # Debug: Check all users in database
    all_users = db.query(User).all()
    print(f"[LOGIN] Total users in database: {len(all_users)}")
    for u in all_users:
        print(f"[LOGIN] User in DB: id={u.id}, username='{u.username}', email='{u.email}'")
    
    if not user:
        print(f"[LOGIN] User '{form_data.username}' not found in database")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    print(f"[LOGIN] User found: {user.username}")
    print(f"[LOGIN] Stored hash: {user.hashed_password}")
    
    # Verify password
    password_valid = verify_password(form_data.password, user.hashed_password)
    print(f"[LOGIN] Password provided: {form_data.password}")
    print(f"[LOGIN] Password valid: {password_valid}")
    
    if not password_valid:
        # Try to hash the provided password and compare directly
        import hashlib
        provided_hash = hashlib.sha256(form_data.password.encode('utf-8')).hexdigest()
        print(f"[LOGIN] Provided password hash: {provided_hash}")
        print(f"[LOGIN] Stored hash: {user.hashed_password}")
        print(f"[LOGIN] Hash match: {provided_hash == user.hashed_password}")
        
        # If hash matches but verify_password failed, there's a bug - force accept
        if provided_hash == user.hashed_password:
            print("[LOGIN] Hash matches directly - forcing password valid")
            password_valid = True
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    # Check if user has completed any test
    test_count = db.query(TestResult).filter(TestResult.user_id == user.id).count()
    has_completed_test = test_count > 0
    
    access_token = create_access_token(data={"sub": user.username})
    
    # Determine redirect based on role and test history
    is_admin = getattr(user, 'role', 'user') == 'admin'
    if is_admin:
        redirect_to = "/admin"
    elif has_completed_test:
        redirect_to = "/dashboard"
    else:
        redirect_to = "/select-filiere"
    
    return {
        "access_token": access_token,
        "token_type": "bearer",
        "user_id": user.id,
        "has_completed_test": has_completed_test,
        "is_admin": is_admin,
        "redirect_to": redirect_to
    }

@app.get("/api/user/me")
async def get_current_user_info(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get current user information with test status"""
    test_count = db.query(TestResult).filter(TestResult.user_id == current_user.id).count()
    has_completed_test = test_count > 0
    is_admin = getattr(current_user, 'role', 'user') == 'admin'
    
    return {
        "id": current_user.id,
        "username": current_user.username,
        "email": current_user.email,
        "has_completed_test": has_completed_test,
        "test_count": test_count,
        "is_admin": is_admin,
        "role": getattr(current_user, 'role', 'user')
    }

@app.get("/api/questions/{filiere}")
async def get_questions(filiere: str):
    """Get questions for a filière"""
    try:
        # Decode filiere in case it's URL encoded
        from urllib.parse import unquote
        filiere = canonicalize_filiere(unquote(filiere))
        
        # Map filière to specializations and get questions
        specializations = {
            "Intelligence Artificielle & Sciences des Données": ["Machine Learning Engineer", "Data Scientist"],
            "Cybersécurité & Infrastructures Réseaux": ["Cybersecurity Analyst"],
            "Développement Digital & Systèmes d'Information": ["Full-Stack Developer"]
        }
        
        # Get questions from first specialization in filière
        spec_list = specializations.get(filiere, ["Full-Stack Developer"])
        if not spec_list:
            raise HTTPException(status_code=404, detail=f"Path '{filiere}' was not found.")
        
        spec = spec_list[0]
        questions = get_questions_for_specialization(spec, num_questions=25)
        
        if not questions or len(questions) == 0:
            raise HTTPException(status_code=404, detail=f"No questions are available for specialization '{spec}'.")
        
        return [QuestionResponse(**q) for q in questions]
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error in get_questions: {e}")
        raise HTTPException(status_code=500, detail=f"Error while loading questions: {str(e)}")

@app.post("/api/predict", response_model=PredictionResponse)
async def predict_specialization(
    test_data: TestSubmission,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Predict specialization based on test results"""
    print(f"[PREDICT] Received test submission from user: {current_user.username}")
    test_data.filiere = canonicalize_filiere(test_data.filiere)
    print(f"[PREDICT] Filiere: {test_data.filiere}")
    print(f"[PREDICT] Answers count: {len(test_data.answers)}")
    print(f"[PREDICT] Scores: practical={test_data.practical_test_score}, logical={test_data.logical_reasoning_score}, problem={test_data.problem_solving_score}")
    
    try:
        # Load model
        model_data = load_model()
        if not model_data:
            print(f"ERROR: Model not loaded. Checked paths: {MODEL_PATHS}")
            for path in MODEL_PATHS:
                print(f"  - {path}: exists={os.path.exists(path)}")
            raise HTTPException(status_code=500, detail="Model is not loaded. Please train the model first.")
        
        model = model_data['model']
        scaler = model_data['scaler']
        class_names = model_data['class_names']
        feature_names = model_data['feature_names']
        label_encoder = model_data.get('label_encoder')
        
        if label_encoder is None:
            raise HTTPException(status_code=500, detail="Label encoder was not found in the model.")
        
        # Prepare features from test submission
        features = {}
        
        # Get questions to map answer indices to question IDs
        specializations = {
            "Intelligence Artificielle & Sciences des Données": ["Machine Learning Engineer", "Data Scientist"],
            "Cybersécurité & Infrastructures Réseaux": ["Cybersecurity Analyst"],
            "Développement Digital & Systèmes d'Information": ["Full-Stack Developer"]
        }
        spec = specializations.get(test_data.filiere, ["Full-Stack Developer"])[0]
        questions = get_questions_for_specialization(spec, num_questions=25)
        
        # Map answers to question scores (q1_score to q25_score)
        # answers dict has question_id as key and answer index (0-3) as value
        question_id_to_index = {q['id']: idx for idx, q in enumerate(questions)}

        # Calculate the practical score from correctness, not from the option index.
        # Option index 0 is a valid answer and must not be treated as zero points.
        answered_correctly = sum(
            question['id'] in test_data.answers
            and test_data.answers[question['id']] == question.get('correct')
            for question in questions
        )
        practical_score = round(
            (answered_correctly / len(questions)) * 100, 2
        ) if questions else 0.0
        
        for i in range(1, 26):
            q_key = f'q{i}_score'
            if i <= len(questions):
                question_id = questions[i-1]['id']
                # Get answer index (0-3) from test submission, default to 0 if not answered
                answer_index = test_data.answers.get(question_id, 0)
                features[q_key] = answer_index
            else:
                features[q_key] = 0
        
        # Other features
        features['practical_test_score'] = practical_score
        features['logical_reasoning_score'] = test_data.logical_reasoning_score
        features['problem_solving_score'] = test_data.problem_solving_score
        features['time_spent_minutes'] = test_data.time_spent_minutes
        
        # Previous and current level (get from user history or default)
        user_history = db.query(TestResult).filter(TestResult.user_id == current_user.id).order_by(TestResult.test_date.desc()).first()
        if user_history:
            features['previous_level'] = user_history.current_level
        else:
            features['previous_level'] = 1

        # Map the assessment score to a transparent five-level scale.
        if practical_score >= 80:
            features['current_level'] = 5
        elif practical_score >= 60:
            features['current_level'] = 4
        elif practical_score >= 40:
            features['current_level'] = 3
        elif practical_score >= 20:
            features['current_level'] = 2
        else:
            features['current_level'] = 1
        
        features['improvement_rate'] = (features['current_level'] - features['previous_level']) / 5.0
        
        # Encode filière
        try:
            filiere_encoded = label_encoder.transform([test_data.filiere])[0]
            features['filiere_encoded'] = filiere_encoded
        except ValueError as e:
            print(f"ERROR encoding filiere '{test_data.filiere}': {e}")
            # Fallback: use first available filiere
            available_filieres = label_encoder.classes_
            if len(available_filieres) > 0:
                filiere_encoded = label_encoder.transform([available_filieres[0]])[0]
                features['filiere_encoded'] = filiere_encoded
                print(f"Using fallback filiere: {available_filieres[0]}")
            else:
                raise HTTPException(status_code=500, detail=f"Error while encoding the path: {str(e)}")
        
        # Create feature vector in correct order
        try:
            feature_vector = np.array([features.get(f, 0) for f in feature_names]).reshape(1, -1)
            
            # Scale features
            feature_vector_scaled = scaler.transform(feature_vector)
            
            # Predict - determine if model needs scaled data
            from sklearn.svm import SVC
            from sklearn.neural_network import MLPClassifier
            
            if isinstance(model, (SVC, MLPClassifier)):
                # SVM and Neural Network need scaled data
                prediction = model.predict(feature_vector_scaled)[0]
                probabilities = model.predict_proba(feature_vector_scaled)[0]
            else:
                # Random Forest, Gradient Boosting, XGBoost use original features
                prediction = model.predict(feature_vector)[0]
                probabilities = model.predict_proba(feature_vector)[0]
        except Exception as e:
            print(f"ERROR during prediction: {e}")
            print(f"Feature vector shape: {feature_vector.shape if 'feature_vector' in locals() else 'N/A'}")
            print(f"Feature names count: {len(feature_names)}")
            print(f"Features dict keys count: {len(features)}")
            raise HTTPException(status_code=500, detail=f"Prediction error: {str(e)}")
        
        predicted_specialization = class_names[prediction]
        if pd.isna(predicted_specialization) or not isinstance(predicted_specialization, str):
            fallback_specializations = {
                "Intelligence Artificielle & Sciences des Données": "Machine Learning Engineer",
                "Cybersécurité & Infrastructures Réseaux": "Cybersecurity Analyst",
                "Développement Digital & Systèmes d'Information": "Full-Stack Developer",
            }
            predicted_specialization = fallback_specializations.get(
                test_data.filiere,
                "Full-Stack Developer"
            )
            print(
                f"[PREDICT] Invalid model class {class_names[prediction]!r}; "
                f"using fallback: {predicted_specialization}"
            )
        confidence = float(probabilities[prediction])
        
        # Get Top 3 specializations
        top_3_indices = np.argsort(probabilities)[-3:][::-1]  # Top 3 highest probabilities
        top_3_specializations = [
            {
                "specialization": class_names[idx],
                "confidence": float(probabilities[idx])
            }
            for idx in top_3_indices
            if isinstance(class_names[idx], str) and not pd.isna(class_names[idx])
        ]
        
        # Generate recommendations
        try:
            rec_system = RecommendationSystem(model, model_data.get('feature_importance', pd.DataFrame()), class_names)
            recommendations = rec_system.generate_recommendations(
                features,
                predicted_specialization,
                features['previous_level'],
                features['current_level']
            )
        except Exception as e:
            print(f"WARNING: Error generating recommendations: {e}")
            # Provide default recommendations
            recommendations = {
                "skills_to_improve": ["General technical skills"],
                "topics_to_study": ["Specialization fundamentals"],
                "learning_recommendations": ["Keep learning and practicing"],
                "suggested_tests": ["Advanced assessment"]
            }
        
        # Save test result
        try:
            test_result = TestResult(
                user_id=current_user.id,
                filiere=test_data.filiere,
                predicted_specialization=predicted_specialization,
                confidence=confidence,
                practical_test_score=practical_score,
                logical_reasoning_score=test_data.logical_reasoning_score,
                problem_solving_score=test_data.problem_solving_score,
                time_spent_minutes=test_data.time_spent_minutes,
                previous_level=features['previous_level'],
                current_level=features['current_level'],
                improvement_rate=features['improvement_rate'],
                test_date=datetime.now()
            )
            db.add(test_result)
            db.commit()
            db.refresh(test_result)
        except Exception as e:
            print(f"ERROR saving test result: {e}")
            db.rollback()
            raise HTTPException(status_code=500, detail=f"Error while saving the result: {str(e)}")
        
        # Save prediction history
        try:
            pred_history = PredictionHistory(
                user_id=current_user.id,
                test_result_id=test_result.id,
                predicted_specialization=predicted_specialization,
                confidence=confidence,
                prediction_date=datetime.now()
            )
            db.add(pred_history)
            db.commit()
        except Exception as e:
            print(f"WARNING: Error saving prediction history: {e}")
            db.rollback()
            # Don't fail if history save fails, test result is already saved
        
        # Trigger continuous learning check (async, non-blocking)
        try:
            from continuous_learning import ContinuousLearning
            cl = ContinuousLearning()
            cl.check_and_retrain(db)  # Check if retraining is needed
        except Exception as e:
            print(f"Warning: Continuous learning check failed: {e}")
    
        return PredictionResponse(
            predicted_specialization=predicted_specialization,
            confidence=confidence,
            top_3_specializations=top_3_specializations,
            recommendations=recommendations,
            test_id=test_result.id
        )
    except HTTPException:
        # Re-raise HTTP exceptions as-is
        raise
    except Exception as e:
        # Catch any other unexpected errors
        import traceback
        print(f"UNEXPECTED ERROR in predict_specialization: {e}")
        print(traceback.format_exc())
        raise HTTPException(status_code=500, detail=f"Unexpected prediction error: {str(e)}")

@app.get("/api/history")
async def get_user_history(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user test history"""
    history = db.query(TestResult).filter(TestResult.user_id == current_user.id).order_by(TestResult.test_date.desc()).all()
    
    return [
        {
            "id": h.id,
            "filiere": h.filiere,
            "predicted_specialization": h.predicted_specialization,
            "confidence": h.confidence,
            "current_level": h.current_level,
            "test_date": h.test_date.isoformat(),
            "practical_test_score": h.practical_test_score
        }
        for h in history
    ]

@app.get("/api/progress")
async def get_user_progress(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    """Get user progress analysis"""
    history = db.query(TestResult).filter(TestResult.user_id == current_user.id).order_by(TestResult.test_date.asc()).all()
    
    if not history:
        return {"message": "No test history available"}
    
    history_data = [
        {
            "current_level": h.current_level,
            "practical_test_score": h.practical_test_score,
            "test_date": h.test_date.isoformat()
        }
        for h in history
    ]
    
    model_data = load_model()
    if model_data and 'feature_importance' in model_data:
        rec_system = RecommendationSystem(
            model_data['model'],
            model_data['feature_importance'],
            model_data['class_names']
        )
        progress_analysis = rec_system.get_progress_analysis(history_data)
        progress_analysis['history'] = history_data
        return progress_analysis
    
    levels = [item['current_level'] for item in history_data]
    scores = [item['practical_test_score'] for item in history_data]
    return {
        "history": history_data,
        "total_tests": len(history_data),
        "current_level": levels[-1] if levels else 0,
        "average_score": float(np.mean(scores)) if scores else 0,
        "level_trend": "stable",
        "score_trend": "stable",
        "improvement_rate": 0
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)

