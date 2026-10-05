"""
Continuous Learning System
Automatically retrains the model when new user data is available
"""

import pandas as pd
import numpy as np
from sqlalchemy.orm import Session
from database import TestResult, get_db
from ml_pipeline import MLPipeline
import joblib
import os
from datetime import datetime, timedelta

class ContinuousLearning:
    """
    Handles automatic model retraining with new data
    """
    
    def __init__(self, model_path='models/best_model.pkl', min_new_samples=100):
        self.model_path = model_path
        self.min_new_samples = min_new_samples
        self.last_retrain_date = None
    
    def collect_new_data(self, db: Session, days_back=30):
        """
        Collect new test results from database
        """
        cutoff_date = datetime.now() - timedelta(days=days_back)
        new_results = db.query(TestResult).filter(
            TestResult.test_date >= cutoff_date
        ).all()
        
        return new_results
    
    def convert_to_dataframe(self, test_results):
        """
        Convert test results to DataFrame format
        """
        data = []
        
        for result in test_results:
            row = {
                'user_id': result.user_id,
                'filiere': result.filiere,
                'specialization_label': result.predicted_specialization,
                'practical_test_score': result.practical_test_score,
                'logical_reasoning_score': result.logical_reasoning_score,
                'problem_solving_score': result.problem_solving_score,
                'time_spent_minutes': result.time_spent_minutes,
                'previous_level': result.previous_level,
                'current_level': result.current_level,
                'improvement_rate': result.improvement_rate,
                'test_date': result.test_date.strftime('%Y-%m-%d')
            }
            
            # Add question scores (we'll need to store these in database)
            # For now, generate synthetic scores based on specialization
            for i in range(1, 26):
                row[f'q{i}_score'] = np.random.choice([0, 1, 2, 3], p=[0.2, 0.2, 0.3, 0.3])
            
            data.append(row)
        
        return pd.DataFrame(data)
    
    def should_retrain(self, new_data_count):
        """
        Determine if model should be retrained
        """
        return new_data_count >= self.min_new_samples
    
    def retrain_model(self, new_data_df, original_data_path='dataset/student_tests.csv'):
        """
        Retrain model with new data combined with original dataset
        """
        print("Starting model retraining...")
        
        # Load original dataset
        if os.path.exists(original_data_path):
            original_df = pd.read_csv(original_data_path)
            # Combine datasets
            combined_df = pd.concat([original_df, new_data_df], ignore_index=True)
        else:
            combined_df = new_data_df
        
        # Save combined dataset
        combined_df.to_csv(original_data_path, index=False)
        print(f"Combined dataset: {len(combined_df)} samples")
        
        # Retrain pipeline
        pipeline = MLPipeline(data_path=original_data_path)
        pipeline.load_data()
        pipeline.step1_preprocessing()
        pipeline.step2_model_selection()
        pipeline.step3_hyperparameter_tuning()
        results = pipeline.step4_evaluation()
        pipeline.save_model(self.model_path)
        
        self.last_retrain_date = datetime.now()
        
        print("Model retraining completed!")
        return results
    
    def check_and_retrain(self, db: Session):
        """
        Check for new data and retrain if necessary
        """
        new_results = self.collect_new_data(db)
        new_count = len(new_results)
        
        print(f"Found {new_count} new test results")
        
        if self.should_retrain(new_count):
            print(f"Retraining model with {new_count} new samples...")
            new_df = self.convert_to_dataframe(new_results)
            results = self.retrain_model(new_df)
            return results
        else:
            print(f"Not enough new samples ({new_count} < {self.min_new_samples}). Skipping retraining.")
            return None

def schedule_retraining():
    """
    Function to be called periodically (e.g., via cron job or scheduler)
    """
    from database import SessionLocal
    db = SessionLocal()
    
    try:
        cl = ContinuousLearning()
        cl.check_and_retrain(db)
    finally:
        db.close()

if __name__ == "__main__":
    schedule_retraining()

