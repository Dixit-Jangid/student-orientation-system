"""Check project status"""
import os
import sys

print("="*60)
print("PROJECT STATUS CHECK")
print("="*60)

# Check dataset
print("\n[1] Dataset:")
if os.path.exists('dataset/student_tests.csv'):
    import pandas as pd
    df = pd.read_csv('dataset/student_tests.csv')
    print(f"  [OK] Dataset exists: {len(df)} rows, {len(df.columns)} columns")
    print(f"  Missing values: {df.isnull().sum().sum()}")
else:
    print("  [MISSING] Dataset not found")

# Check model
print("\n[2] ML Model:")
if os.path.exists('models/best_model.pkl'):
    print("  [OK] Model file exists")
    try:
        import joblib
        model_data = joblib.load('models/best_model.pkl')
        print(f"  [OK] Model loaded successfully")
        print(f"  Model type: {type(model_data['model']).__name__}")
        print(f"  Classes: {len(model_data['class_names'])} specializations")
    except Exception as e:
        print(f"  [ERROR] Could not load model: {e}")
else:
    print("  [MISSING] Model not found - run pipeline first")

# Check results
print("\n[3] Results:")
results_files = []
if os.path.exists('results'):
    results_files = [f for f in os.listdir('results') if f.endswith('.png')]
if results_files:
    print(f"  [OK] Found {len(results_files)} result files:")
    for f in results_files:
        print(f"    - {f}")
else:
    print("  [MISSING] No result files found")

# Check database
print("\n[4] Database:")
if os.path.exists('specialization_prediction.db'):
    print("  [OK] Database file exists")
    try:
        from sqlalchemy import create_engine, inspect
        engine = create_engine('sqlite:///specialization_prediction.db')
        inspector = inspect(engine)
        tables = inspector.get_table_names()
        print(f"  [OK] Database has {len(tables)} tables: {', '.join(tables)}")
    except Exception as e:
        print(f"  [ERROR] Could not check database: {e}")
else:
    print("  [MISSING] Database not found - run init_database.py first")

# Check dependencies
print("\n[5] Dependencies:")
required = ['pandas', 'numpy', 'sklearn', 'xgboost', 'fastapi', 'sqlalchemy']
missing = []
for pkg in required:
    try:
        __import__(pkg)
        print(f"  [OK] {pkg}")
    except ImportError:
        print(f"  [MISSING] {pkg}")
        missing.append(pkg)

print("\n" + "="*60)
if missing:
    print(f"[WARNING] Missing dependencies: {', '.join(missing)}")
    print("Install with: pip install " + " ".join(missing))
else:
    print("[SUCCESS] All dependencies installed!")
print("="*60)

