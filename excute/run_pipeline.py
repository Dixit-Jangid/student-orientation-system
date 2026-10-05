"""Run ML pipeline"""
import os
from ml_pipeline import MLPipeline

os.makedirs('models', exist_ok=True)
os.makedirs('results', exist_ok=True)

print("Starting ML Pipeline...")
pipeline = MLPipeline(data_path='dataset/student_tests.csv')
results = pipeline.run_complete_pipeline()

print(f"\n[SUCCESS] Pipeline completed!")
print(f"Test Accuracy: {results['test_accuracy']:.4f}")
print(f"F1-Score: {results['f1_score']:.4f}")
print(f"Precision: {results['precision']:.4f}")
print(f"Recall: {results['recall']:.4f}")

