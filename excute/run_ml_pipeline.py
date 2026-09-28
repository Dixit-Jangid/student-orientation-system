"""
Script to generate dataset and run ML pipeline
Run this first before starting the web application
"""

import os
import sys
from pathlib import Path

PROJECT_ROOT = Path(__file__).resolve().parents[1]
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


def main():
    print("="*60)
    print("MACHINE LEARNING PIPELINE - SETUP")
    print("="*60)

    os.makedirs(PROJECT_ROOT / 'dataset', exist_ok=True)
    os.makedirs(PROJECT_ROOT / 'models', exist_ok=True)
    os.makedirs(PROJECT_ROOT / 'results', exist_ok=True)

    # Step 1: Generate dataset
    print("\n[1/2] Generating dataset...")
    from dataset_generator import generate_dataset
    df = generate_dataset(n_samples=5000)
    df.to_csv(PROJECT_ROOT / 'dataset' / 'student_tests.csv', index=False)
    print("[OK] Dataset generated and saved")

    # Step 2: Run ML pipeline
    print("\n[2/2] Running ML pipeline...")
    from ml_pipeline import MLPipeline

    pipeline = MLPipeline(data_path=str(PROJECT_ROOT / 'dataset' / 'student_tests.csv'))
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

