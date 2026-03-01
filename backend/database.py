"""
Database models and setup
"""

from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os

# Use database from parent directory (project root)
# Get the directory where this file is located (backend/)
# Then go to parent directory (project root)
BACKEND_DIR = os.path.dirname(os.path.abspath(__file__))
BASE_DIR = os.path.dirname(BACKEND_DIR)
DATABASE_PATH = os.path.join(BASE_DIR, "specialization_prediction.db")
DATABASE_URL = os.getenv("DATABASE_URL", f"sqlite:///{DATABASE_PATH}")

# Debug: print database path on import
print(f"[DATABASE] Database path: {DATABASE_PATH}")
print(f"[DATABASE] Database exists: {os.path.exists(DATABASE_PATH)}")

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    role = Column(String, default="user")  # "user" or "admin"

class TestResult(Base):
    __tablename__ = "test_results"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    filiere = Column(String)
    predicted_specialization = Column(String)
    confidence = Column(Float)
    practical_test_score = Column(Float)
    logical_reasoning_score = Column(Float)
    problem_solving_score = Column(Float)
    time_spent_minutes = Column(Float)
    previous_level = Column(Integer)
    current_level = Column(Integer)
    improvement_rate = Column(Float)
    test_date = Column(DateTime)

class PredictionHistory(Base):
    __tablename__ = "prediction_history"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    test_result_id = Column(Integer, ForeignKey("test_results.id"))
    predicted_specialization = Column(String)
    confidence = Column(Float)
    prediction_date = Column(DateTime)

def init_db():
    """Initialize database tables"""
    Base.metadata.create_all(bind=engine)

def get_db():
    """Get database session"""
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

