"""
Run the Academic ML Pipeline
This script runs the complete academic pipeline following strict methodology
"""

from academic_ml_pipeline import AcademicMLPipeline
import os

# Ensure dataset exists
if not os.path.exists('dataset/student_tests.csv'):
    print("[INFO] Dataset not found. Generating dataset...")
    from dataset_generator import generate_dataset
    generate_dataset(n_samples=50000)
    print("[OK] Dataset generated!")

# Run academic pipeline
print("\n" + "="*70)
print("STARTING ACADEMIC ML PIPELINE")
print("="*70)

pipeline = AcademicMLPipeline(data_path='dataset/student_tests.csv')
results = pipeline.run_complete_pipeline()

if results:
    print("\n" + "="*70)
    print("ACADEMIC PIPELINE COMPLETED!")
    print("="*70)
    print("\nNext steps:")
    print("  1. Review results in 'results/' directory")
    print("  2. Check model in 'models/best_model.pkl'")
    print("  3. Start backend: cd backend && uvicorn main:app --reload")
else:
    print("\n[ERROR] Pipeline failed!")

