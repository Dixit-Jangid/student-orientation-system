"""Run ML pipeline - Fast version for quick completion"""
import os
import sys
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, classification_report, confusion_matrix
from sklearn.impute import SimpleImputer, KNNImputer
import joblib
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns

print("="*60)
print("FAST ML PIPELINE - OPTIMIZED FOR QUICK COMPLETION")
print("="*60)

# Create directories
os.makedirs('models', exist_ok=True)
os.makedirs('results', exist_ok=True)

# Load data
print("\n[1/5] Loading dataset...")
df = pd.read_csv('dataset/student_tests.csv')
df = df.dropna(subset=['filiere', 'specialization_label']).copy()
df['filiere'] = df['filiere'].astype(str).str.strip()
df['specialization_label'] = df['specialization_label'].astype(str).str.strip()
print(f"Dataset shape: {df.shape}")

# Preprocessing
print("\n[2/5] Preprocessing...")
question_cols = [f'q{i}_score' for i in range(1, 26)]
numeric_cols = ['practical_test_score', 'logical_reasoning_score', 
               'problem_solving_score', 'time_spent_minutes',
               'previous_level', 'current_level', 'improvement_rate']

# Handle missing values
imputer_mean = SimpleImputer(strategy='mean')
df[question_cols] = imputer_mean.fit_transform(df[question_cols])

missing_numeric = df[numeric_cols].isnull().sum()
if missing_numeric.sum() > 0:
    knn_imputer = KNNImputer(n_neighbors=5)
    df[numeric_cols] = knn_imputer.fit_transform(df[numeric_cols])

# Handle outliers
for col in question_cols:
    df[col] = df[col].clip(0, 3)

Q1 = df['time_spent_minutes'].quantile(0.25)
Q3 = df['time_spent_minutes'].quantile(0.75)
IQR = Q3 - Q1
df['time_spent_minutes'] = df['time_spent_minutes'].clip(Q1 - 1.5*IQR, Q3 + 1.5*IQR)

score_cols = ['practical_test_score', 'logical_reasoning_score', 'problem_solving_score']
for col in score_cols:
    df[col] = df[col].clip(0, 100)

# Encode
label_encoder = LabelEncoder()
df['filiere_encoded'] = label_encoder.fit_transform(df['filiere'])

# Prepare features
feature_cols = question_cols + numeric_cols + ['filiere_encoded']
X = df[feature_cols].copy()
y = df['specialization_label'].copy()

target_encoder = LabelEncoder()
y_encoded = target_encoder.fit_transform(y)
class_names = target_encoder.classes_

# Split
X_train, X_test, y_train, y_test = train_test_split(
    X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
)

print(f"Training set: {X_train.shape}")
print(f"Test set: {X_test.shape}")

# Train model
print("\n[3/5] Training Random Forest model...")
model = RandomForestClassifier(
    n_estimators=200,
    max_depth=20,
    min_samples_split=5,
    random_state=42,
    n_jobs=-1,
    verbose=1
)
model.fit(X_train, y_train)

# Evaluate
print("\n[4/5] Evaluating model...")
y_train_pred = model.predict(X_train)
y_test_pred = model.predict(X_test)

train_acc = accuracy_score(y_train, y_train_pred)
test_acc = accuracy_score(y_test, y_test_pred)
test_precision = precision_score(y_test, y_test_pred, average='weighted', zero_division=0)
test_recall = recall_score(y_test, y_test_pred, average='weighted', zero_division=0)
test_f1 = f1_score(y_test, y_test_pred, average='weighted', zero_division=0)

print(f"\nResults:")
print(f"  Train Accuracy: {train_acc:.4f}")
print(f"  Test Accuracy: {test_acc:.4f}")
print(f"  Precision: {test_precision:.4f}")
print(f"  Recall: {test_recall:.4f}")
print(f"  F1-Score: {test_f1:.4f}")
print(f"  Overfitting: {train_acc - test_acc:.4f}")

# Confusion Matrix
print("\nGenerating confusion matrix...")
cm = confusion_matrix(y_test, y_test_pred)
plt.figure(figsize=(14, 12))
sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
           xticklabels=class_names, yticklabels=class_names)
plt.title('Confusion Matrix')
plt.ylabel('True Label')
plt.xlabel('Predicted Label')
plt.xticks(rotation=45, ha='right')
plt.yticks(rotation=0)
plt.tight_layout()
plt.savefig('results/confusion_matrix.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: results/confusion_matrix.png")

# Feature Importance
print("\nGenerating feature importance...")
feature_importance = pd.DataFrame({
    'feature': feature_cols,
    'importance': model.feature_importances_
}).sort_values('importance', ascending=False)

plt.figure(figsize=(10, 8))
top_features = feature_importance.head(15)
plt.barh(range(len(top_features)), top_features['importance'])
plt.yticks(range(len(top_features)), top_features['feature'])
plt.xlabel('Importance')
plt.title('Top 15 Feature Importances')
plt.gca().invert_yaxis()
plt.tight_layout()
plt.savefig('results/feature_importance.png', dpi=300, bbox_inches='tight')
plt.close()
print("  Saved: results/feature_importance.png")

# Save model
print("\n[5/5] Saving model...")
# Create and fit scaler (even if not used for Random Forest, backend needs it)
scaler = StandardScaler()
scaler.fit(X_train)  # Fit scaler on training data for future use
print("  Scaler fitted on training data")
joblib.dump({
    'model': model,
    'scaler': scaler,
    'label_encoder': label_encoder,
    'class_names': class_names,
    'feature_names': feature_cols
}, 'models/best_model.pkl')
print("  Saved: models/best_model.pkl")

print("\n" + "="*60)
print("PIPELINE COMPLETED SUCCESSFULLY!")
print("="*60)
print(f"\nFinal Results:")
print(f"  Test Accuracy: {test_acc:.4f}")
print(f"  F1-Score: {test_f1:.4f}")
print(f"  Precision: {test_precision:.4f}")
print(f"  Recall: {test_recall:.4f}")
print(f"\nFiles created:")
print(f"  - models/best_model.pkl")
print(f"  - results/confusion_matrix.png")
print(f"  - results/feature_importance.png")
print(f"\nYou can now start the backend:")
print(f"  cd backend && uvicorn main:app --reload")

