"""
Complete Machine Learning Pipeline
Implements all academic ML steps: preprocessing, training, evaluation
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV
from sklearn.preprocessing import StandardScaler, LabelEncoder
from sklearn.ensemble import RandomForestClassifier, GradientBoostingClassifier
from sklearn.svm import SVC
from sklearn.neural_network import MLPClassifier
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)
from sklearn.impute import SimpleImputer, KNNImputer
import xgboost as xgb
import joblib
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime

class MLPipeline:
    """
    Complete ML Pipeline for Specialization Prediction
    """
    
    def __init__(self, data_path='dataset/student_tests.csv'):
        self.data_path = data_path
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        self.models = {}
        self.best_model = None
        self.feature_importance = None
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
    def load_data(self):
        """Load dataset"""
        print("Loading dataset...")
        self.df = pd.read_csv(self.data_path)
        print(f"Dataset shape: {self.df.shape}")
        return self.df
    
    def step1_preprocessing(self):
        """
        Step 1: Data Preprocessing
        - Handle missing values (mean, median, KNN)
        - Handle outliers
        - Encode categorical variables
        - Normalize/standardize data
        """
        print("\n" + "="*50)
        print("STEP 1: DATA PREPROCESSING")
        print("="*50)
        
        df = self.df.copy()
        
        # 1.1 Handle missing values in question scores
        print("\n1.1 Handling missing values...")
        question_cols = [f'q{i}_score' for i in range(1, 26)]
        
        # Strategy 1: Mean imputation for question scores
        imputer_mean = SimpleImputer(strategy='mean')
        df[question_cols] = imputer_mean.fit_transform(df[question_cols])
        
        # Strategy 2: KNN imputation for other numeric columns
        numeric_cols = ['practical_test_score', 'logical_reasoning_score', 
                       'problem_solving_score', 'time_spent_minutes',
                       'previous_level', 'current_level', 'improvement_rate']
        
        # Check for missing values in numeric cols
        missing_numeric = df[numeric_cols].isnull().sum()
        if missing_numeric.sum() > 0:
            print(f"Missing values in numeric columns: {missing_numeric[missing_numeric > 0]}")
            knn_imputer = KNNImputer(n_neighbors=5)
            df[numeric_cols] = knn_imputer.fit_transform(df[numeric_cols])
        
        # 1.2 Handle outliers
        print("\n1.2 Handling outliers...")
        
        # Remove impossible values from question scores (should be 0-3)
        for col in question_cols:
            df[col] = df[col].clip(0, 3)
        
        # Handle outliers in time_spent_minutes (remove negative and extreme values)
        Q1 = df['time_spent_minutes'].quantile(0.25)
        Q3 = df['time_spent_minutes'].quantile(0.75)
        IQR = Q3 - Q1
        lower_bound = Q1 - 1.5 * IQR
        upper_bound = Q3 + 1.5 * IQR
        df['time_spent_minutes'] = df['time_spent_minutes'].clip(lower_bound, upper_bound)
        
        # Handle outliers in scores (0-100)
        score_cols = ['practical_test_score', 'logical_reasoning_score', 'problem_solving_score']
        for col in score_cols:
            df[col] = df[col].clip(0, 100)
        
        # 1.3 Encode categorical variables
        print("\n1.3 Encoding categorical variables...")
        df['filiere_encoded'] = self.label_encoder.fit_transform(df['filiere'])
        
        # 1.4 Prepare features and target
        feature_cols = question_cols + numeric_cols + ['filiere_encoded']
        X = df[feature_cols].copy()
        y = df['specialization_label'].copy()
        
        # Encode target variable
        y_encoded = LabelEncoder().fit_transform(y)
        self.class_names = LabelEncoder().fit(y).classes_
        
        # 1.5 Train/Validation/Test split
        print("\n1.4 Train/Validation/Test split...")
        X_temp, self.X_test, y_temp, self.y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        self.X_train, self.X_val, self.y_train, self.y_val = train_test_split(
            X_temp, y_temp, test_size=0.2, random_state=42, stratify=y_temp
        )
        
        print(f"Training set: {self.X_train.shape}")
        print(f"Validation set: {self.X_val.shape}")
        print(f"Test set: {self.X_test.shape}")
        
        # 1.6 Normalize/Standardize features
        print("\n1.5 Normalizing features...")
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_val_scaled = self.scaler.transform(self.X_val)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        
        self.feature_names = feature_cols
        
        print("\n[OK] Preprocessing completed!")
        return X, y_encoded
    
    def step2_model_selection(self):
        """
        Step 2: Model Selection
        Train and compare: Random Forest, Gradient Boosting, XGBoost, SVM, Neural Network
        """
        print("\n" + "="*50)
        print("STEP 2: MODEL SELECTION & TRAINING")
        print("="*50)
        
        # Initialize models
        models = {
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1),
            'Gradient Boosting': GradientBoostingClassifier(n_estimators=100, random_state=42),
            'XGBoost': xgb.XGBClassifier(n_estimators=100, random_state=42, eval_metric='mlogloss'),
            'SVM': SVC(kernel='rbf', random_state=42, probability=True),
            'Neural Network': MLPClassifier(hidden_layer_sizes=(100, 50), max_iter=500, random_state=42)
        }
        
        results = {}
        
        for name, model in models.items():
            print(f"\nTraining {name}...")
            
            # Use scaled data for SVM and Neural Network
            if name in ['SVM', 'Neural Network']:
                X_train = self.X_train_scaled
                X_val = self.X_val_scaled
                # Performance safeguard: downsample for heavy models on large datasets
                max_samples = 20000
                if X_train.shape[0] > max_samples:
                    # stratified downsample to keep class balance
                    X_train, _, y_down, _ = train_test_split(
                        X_train, self.y_train,
                        train_size=max_samples,
                        stratify=self.y_train,
                        random_state=42
                    )
                    # Align y for training subset
                    y_train_local = y_down
                else:
                    y_train_local = self.y_train
            else:
                X_train = self.X_train
                X_val = self.X_val
                y_train_local = self.y_train
            
            # Train model
            model.fit(X_train, y_train_local)
            
            # Predictions
            y_train_pred = model.predict(X_train)
            y_val_pred = model.predict(X_val)
            
            # Calculate metrics
            train_acc = accuracy_score(self.y_train, y_train_pred)
            val_acc = accuracy_score(self.y_val, y_val_pred)
            
            train_f1 = f1_score(self.y_train, y_train_pred, average='weighted')
            val_f1 = f1_score(self.y_val, y_val_pred, average='weighted')
            
            results[name] = {
                'model': model,
                'train_accuracy': train_acc,
                'val_accuracy': val_acc,
                'train_f1': train_f1,
                'val_f1': val_f1,
                'overfitting': train_acc - val_acc
            }
            
            print(f"  Train Accuracy: {train_acc:.4f}")
            print(f"  Val Accuracy: {val_acc:.4f}")
            print(f"  Overfitting: {train_acc - val_acc:.4f}")
            
            self.models[name] = model
        
        # Select best model (lowest overfitting, highest validation accuracy)
        best_model_name = max(results.keys(), 
                             key=lambda k: results[k]['val_accuracy'] - 0.5 * results[k]['overfitting'])
        self.best_model = results[best_model_name]['model']
        
        print(f"\n[OK] Best model: {best_model_name}")
        print(f"  Validation Accuracy: {results[best_model_name]['val_accuracy']:.4f}")
        
        return results
    
    def step3_hyperparameter_tuning(self):
        """
        Step 3: Hyperparameter Tuning
        """
        print("\n" + "="*50)
        print("STEP 3: HYPERPARAMETER TUNING")
        print("="*50)
        
        # Tune best model (assuming Random Forest or XGBoost)
        if isinstance(self.best_model, RandomForestClassifier):
            print("Tuning Random Forest...")
            param_grid = {
                'n_estimators': [150, 250],
                'max_depth': [None, 20],
                'min_samples_split': [2, 5]
            }
            base_model = RandomForestClassifier(random_state=42, n_jobs=-1)
            
        elif isinstance(self.best_model, xgb.XGBClassifier):
            print("Tuning XGBoost...")
            param_grid = {
                'n_estimators': [150, 250],
                'max_depth': [3, 5],
                'learning_rate': [0.05, 0.1]
            }
            base_model = xgb.XGBClassifier(random_state=42, eval_metric='mlogloss')
        else:
            print("Skipping hyperparameter tuning for this model type")
            return self.best_model
        
        # Optionally downsample for tuning to keep it fast
        max_tune_samples = 30000
        if self.X_train.shape[0] > max_tune_samples:
            X_tune, _, y_tune, _ = train_test_split(
                self.X_train, self.y_train,
                train_size=max_tune_samples,
                stratify=self.y_train,
                random_state=42
            )
        else:
            X_tune, y_tune = self.X_train, self.y_train
        
        # Grid search with cross-validation (lighter CV)
        grid_search = GridSearchCV(
            base_model, param_grid, cv=3, scoring='accuracy', 
            n_jobs=-1, verbose=1
        )
        
        grid_search.fit(X_tune, y_tune)
        
        print(f"Best parameters: {grid_search.best_params_}")
        print(f"Best CV score: {grid_search.best_score_:.4f}")
        
        self.best_model = grid_search.best_estimator_
        return self.best_model
    
    def step4_evaluation(self):
        """
        Step 4: Evaluation
        Metrics: Accuracy, Precision, Recall, F1-score, Confusion Matrix, Overfitting analysis
        """
        print("\n" + "="*50)
        print("STEP 4: MODEL EVALUATION")
        print("="*50)
        
        # Determine if model needs scaled data
        if isinstance(self.best_model, (SVC, MLPClassifier)):
            X_test = self.X_test_scaled
        else:
            X_test = self.X_test
        
        # Predictions
        y_train_pred = self.best_model.predict(self.X_train if not isinstance(self.best_model, (SVC, MLPClassifier)) else self.X_train_scaled)
        y_test_pred = self.best_model.predict(X_test)
        
        # Calculate metrics
        print("\n4.1 Accuracy Metrics:")
        train_acc = accuracy_score(self.y_train, y_train_pred)
        test_acc = accuracy_score(self.y_test, y_test_pred)
        print(f"  Train Accuracy: {train_acc:.4f}")
        print(f"  Test Accuracy: {test_acc:.4f}")
        print(f"  Overfitting: {train_acc - test_acc:.4f}")
        
        print("\n4.2 Precision, Recall, F1-Score:")
        test_precision = precision_score(self.y_test, y_test_pred, average='weighted', zero_division=0)
        test_recall = recall_score(self.y_test, y_test_pred, average='weighted', zero_division=0)
        test_f1 = f1_score(self.y_test, y_test_pred, average='weighted', zero_division=0)
        
        print(f"  Precision: {test_precision:.4f}")
        print(f"  Recall: {test_recall:.4f}")
        print(f"  F1-Score: {test_f1:.4f}")
        
        print("\n4.3 Classification Report:")
        print(classification_report(self.y_test, y_test_pred, target_names=self.class_names, zero_division=0))
        
        # Confusion Matrix
        print("\n4.4 Confusion Matrix:")
        cm = confusion_matrix(self.y_test, y_test_pred)
        
        # Plot confusion matrix
        plt.figure(figsize=(14, 12))
        sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', 
                   xticklabels=self.class_names, yticklabels=self.class_names)
        plt.title('Confusion Matrix')
        plt.ylabel('True Label')
        plt.xlabel('Predicted Label')
        plt.xticks(rotation=45, ha='right')
        plt.yticks(rotation=0)
        plt.tight_layout()
        plt.savefig('results/confusion_matrix.png', dpi=300, bbox_inches='tight')
        print("  Confusion matrix saved to 'results/confusion_matrix.png'")
        
        # Feature Importance (if available)
        if hasattr(self.best_model, 'feature_importances_'):
            print("\n4.5 Feature Importance:")
            self.feature_importance = pd.DataFrame({
                'feature': self.feature_names,
                'importance': self.best_model.feature_importances_
            }).sort_values('importance', ascending=False)
            
            print(self.feature_importance.head(10))
            
            # Plot feature importance
            plt.figure(figsize=(10, 8))
            top_features = self.feature_importance.head(15)
            plt.barh(range(len(top_features)), top_features['importance'])
            plt.yticks(range(len(top_features)), top_features['feature'])
            plt.xlabel('Importance')
            plt.title('Top 15 Feature Importances')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.savefig('results/feature_importance.png', dpi=300, bbox_inches='tight')
            print("  Feature importance plot saved to 'results/feature_importance.png'")
        
        # Cross-validation
        print("\n4.6 Cross-Validation:")
        if isinstance(self.best_model, (SVC, MLPClassifier)):
            cv_scores = cross_val_score(self.best_model, self.X_train_scaled, self.y_train, cv=5, scoring='accuracy')
        else:
            cv_scores = cross_val_score(self.best_model, self.X_train, self.y_train, cv=5, scoring='accuracy')
        
        print(f"  CV Mean Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std() * 2:.4f})")
        
        results = {
            'train_accuracy': train_acc,
            'test_accuracy': test_acc,
            'precision': test_precision,
            'recall': test_recall,
            'f1_score': test_f1,
            'overfitting': train_acc - test_acc,
            'cv_mean': cv_scores.mean(),
            'cv_std': cv_scores.std()
        }
        
        print("\n[OK] Evaluation completed!")
        return results
    
    def save_model(self, path='models/best_model.pkl'):
        """Save the trained model"""
        os.makedirs(os.path.dirname(path), exist_ok=True)
        joblib.dump({
            'model': self.best_model,
            'scaler': self.scaler,
            'label_encoder': self.label_encoder,
            'class_names': self.class_names,
            'feature_names': self.feature_names
        }, path)
        print(f"\nModel saved to {path}")
    
    def run_complete_pipeline(self):
        """Run the complete ML pipeline"""
        self.load_data()
        self.step1_preprocessing()
        self.step2_model_selection()
        self.step3_hyperparameter_tuning()
        results = self.step4_evaluation()
        self.save_model()
        return results

if __name__ == "__main__":
    # Create necessary directories
    os.makedirs('dataset', exist_ok=True)
    os.makedirs('models', exist_ok=True)
    os.makedirs('results', exist_ok=True)
    
    # Run pipeline
    pipeline = MLPipeline()
    results = pipeline.run_complete_pipeline()
    print("\n" + "="*50)
    print("PIPELINE COMPLETED SUCCESSFULLY!")
    print("="*50)

