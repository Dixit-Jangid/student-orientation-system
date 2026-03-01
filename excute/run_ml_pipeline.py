"""
Script to generate dataset and run ML pipeline
Run this first before starting the web application
"""

import os
import sys

def main():
    print("="*60)
    print("MACHINE LEARNING PIPELINE - SETUP")
    print("="*60)
    
    # Step 1: Generate dataset
    print("\n[1/2] Generating dataset...")
    from dataset_generator import generate_dataset
    os.makedirs('dataset', exist_ok=True)
    df = generate_dataset(n_samples=50000)
    df.to_csv('dataset/student_tests.csv', index=False)
    print("[OK] Dataset generated and saved")
    
    # Step 2: Run ML pipeline
    print("\n[2/2] Running ML pipeline...")
    from ml_pipeline import MLPipeline
    
    os.makedirs('models', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    pipeline = MLPipeline(data_path='dataset/student_tests.csv')
    results = pipeline.run_complete_pipeline()
    
    print("\n" + "="*60)
    print("SETUP COMPLETED!")
    print("="*60)
    print(f"Test Accuracy: {results['test_accuracy']:.4f}")
    print(f"F1-Score: {results['f1_score']:.4f}")
    print("\nYou can now start the web application with:")
    print("  cd backend && uvicorn main:app --reload")

if __name__ == "__main__":
    main()

