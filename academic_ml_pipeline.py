"""
ACADEMIC MACHINE LEARNING PIPELINE
Following Strict University Methodology

Strict Order:
1. Dataset Description
2. Exploratory Data Analysis (EDA) - BEFORE cleaning
3. Data Cleaning
4. Data Preprocessing - AFTER cleaning
5. Model Selection
6. Model Training
7. Model Evaluation
8. Model Improvement
9. Results & Interpretation
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, cross_val_score, GridSearchCV, StratifiedKFold
from sklearn.preprocessing import StandardScaler, LabelEncoder, MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from sklearn.metrics import (
    accuracy_score, precision_score, recall_score, f1_score,
    classification_report, confusion_matrix
)
from sklearn.impute import SimpleImputer, KNNImputer
import joblib
import matplotlib
matplotlib.use('Agg')  # Non-interactive backend
import matplotlib.pyplot as plt
import seaborn as sns
import os
from datetime import datetime
import warnings
warnings.filterwarnings('ignore')

class AcademicMLPipeline:
    """
    Academic ML Pipeline following strict methodology
    """
    
    def __init__(self, data_path='dataset/student_tests.csv'):
        self.data_path = data_path
        self.df_raw = None  # Raw data BEFORE any processing
        self.df_cleaned = None  # Data AFTER cleaning
        self.df_processed = None  # Data AFTER preprocessing
        
        # Preprocessing objects
        self.scaler = StandardScaler()
        self.label_encoder = LabelEncoder()
        
        # Models and results
        self.models = {}
        self.best_model = None
        self.best_model_name = None
        self.model_results = {}
        
        # Data splits
        self.X_train = None
        self.X_test = None
        self.y_train = None
        self.y_test = None
        
        # Feature names
        self.feature_names = None
        self.class_names = None
        
        # Statistics
        self.before_stats = {}
        self.after_stats = {}
        self.eda_results = {}
        
        # Create directories
        os.makedirs('results', exist_ok=True)
        os.makedirs('results/eda', exist_ok=True)
        os.makedirs('results/cleaning', exist_ok=True)
        os.makedirs('results/evaluation', exist_ok=True)
        os.makedirs('models', exist_ok=True)
    
    # ========================================
    # STEP 1: DATASET DESCRIPTION
    # ========================================
    def step1_dataset_description(self):
        """Step 1: Describe the dataset"""
        print("\n" + "="*70)
        print("STEP 1: DATASET DESCRIPTION")
        print("="*70)
        
        # Load raw data
        print("\n[1.1] Loading raw dataset...")
        self.df_raw = pd.read_csv(self.data_path)
        
        print(f"\n[1.2] Dataset Shape:")
        print(f"  - Rows: {len(self.df_raw):,}")
        print(f"  - Columns: {len(self.df_raw.columns)}")
        print(f"  - Memory usage: {self.df_raw.memory_usage(deep=True).sum() / 1024**2:.2f} MB")
        
        print(f"\n[1.3] Column Information:")
        print(f"  - Total columns: {len(self.df_raw.columns)}")
        print(f"  - Numeric columns: {len(self.df_raw.select_dtypes(include=[np.number]).columns)}")
        print(f"  - Categorical columns: {len(self.df_raw.select_dtypes(include=['object']).columns)}")
        
        print(f"\n[1.4] Column Names:")
        for i, col in enumerate(self.df_raw.columns, 1):
            dtype = self.df_raw[col].dtype
            null_count = self.df_raw[col].isnull().sum()
            null_pct = (null_count / len(self.df_raw)) * 100
            print(f"  {i:2d}. {col:30s} | Type: {str(dtype):10s} | Missing: {null_count:5d} ({null_pct:5.2f}%)")
        
        print(f"\n[1.5] Data Types:")
        print(self.df_raw.dtypes.value_counts())
        
        # Store basic statistics
        self.before_stats = {
            'rows': len(self.df_raw),
            'columns': len(self.df_raw.columns),
            'missing_total': self.df_raw.isnull().sum().sum(),
            'duplicates': self.df_raw.duplicated().sum(),
            'memory_mb': self.df_raw.memory_usage(deep=True).sum() / 1024**2
        }
        
        print(f"\n[1.6] Basic Statistics:")
        print(f"  - Total rows: {self.before_stats['rows']:,}")
        print(f"  - Total columns: {self.before_stats['columns']}")
        print(f"  - Total missing values: {self.before_stats['missing_total']:,}")
        print(f"  - Duplicate rows: {self.before_stats['duplicates']:,}")
        
        print("\n[OK] Dataset description completed!")
        return self.df_raw
    
    # ========================================
    # STEP 2: EXPLORATORY DATA ANALYSIS (EDA)
    # ========================================
    def step2_eda(self):
        """Step 2: Exploratory Data Analysis BEFORE cleaning"""
        print("\n" + "="*70)
        print("STEP 2: EXPLORATORY DATA ANALYSIS (EDA) - BEFORE CLEANING")
        print("="*70)
        
        df = self.df_raw.copy()
        
        # 2.1 Descriptive Statistics
        print("\n[2.1] Descriptive Statistics...")
        numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
        
        desc_stats = df[numeric_cols].describe()
        print("\nDescriptive Statistics (Numerical Features):")
        print(desc_stats)
        
        # Save descriptive statistics
        desc_stats.to_csv('results/eda/descriptive_statistics.csv')
        
        # 2.2 Missing Values Analysis
        print("\n[2.2] Missing Values Analysis...")
        missing_analysis = pd.DataFrame({
            'Column': df.columns,
            'Missing_Count': df.isnull().sum(),
            'Missing_Percentage': (df.isnull().sum() / len(df)) * 100,
            'Data_Type': df.dtypes
        })
        missing_analysis = missing_analysis.sort_values('Missing_Count', ascending=False)
        missing_analysis = missing_analysis[missing_analysis['Missing_Count'] > 0]
        
        if len(missing_analysis) > 0:
            print("\nMissing Values per Column:")
            print(missing_analysis.to_string(index=False))
            missing_analysis.to_csv('results/eda/missing_values_analysis.csv', index=False)
            
            # Visualize missing values
            plt.figure(figsize=(14, 8))
            missing_analysis_subset = missing_analysis.head(20)  # Top 20 columns with missing values
            plt.barh(range(len(missing_analysis_subset)), missing_analysis_subset['Missing_Percentage'])
            plt.yticks(range(len(missing_analysis_subset)), missing_analysis_subset['Column'])
            plt.xlabel('Missing Percentage (%)')
            plt.title('Missing Values Distribution (Top 20 Columns)')
            plt.gca().invert_yaxis()
            plt.tight_layout()
            plt.savefig('results/eda/missing_values_heatmap.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("  Saved: results/eda/missing_values_heatmap.png")
        else:
            print("  No missing values found in the dataset")
        
        # 2.3 Duplicate Detection
        print("\n[2.3] Duplicate Detection...")
        duplicate_count = df.duplicated().sum()
        print(f"  - Duplicate rows: {duplicate_count:,}")
        if duplicate_count > 0:
            duplicate_pct = (duplicate_count / len(df)) * 100
            print(f"  - Percentage: {duplicate_pct:.2f}%")
        
        # 2.4 Distribution of Numerical Features
        print("\n[2.4] Generating Histograms for Numerical Features...")
        numeric_cols_plot = [col for col in numeric_cols if col not in ['user_id']]
        n_cols = min(4, len(numeric_cols_plot))
        n_rows = int(np.ceil(len(numeric_cols_plot) / n_cols))
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(16, 4*n_rows))
        axes = axes.flatten() if n_rows > 1 else [axes] if n_cols == 1 else axes
        
        for idx, col in enumerate(numeric_cols_plot[:n_cols*n_rows]):
            axes[idx].hist(df[col].dropna(), bins=50, edgecolor='black', alpha=0.7)
            axes[idx].set_title(f'Distribution of {col}')
            axes[idx].set_xlabel(col)
            axes[idx].set_ylabel('Frequency')
            axes[idx].grid(True, alpha=0.3)
        
        # Hide empty subplots
        for idx in range(len(numeric_cols_plot[:n_cols*n_rows]), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        plt.savefig('results/eda/histograms_numerical_features.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  Saved: results/eda/histograms_numerical_features.png")
        
        # 2.5 Boxplots for Outlier Detection
        print("\n[2.5] Generating Boxplots for Outlier Detection...")
        score_cols = [col for col in numeric_cols_plot if 'score' in col.lower()][:12]
        if len(score_cols) > 0:
            n_cols_box = 4
            n_rows_box = int(np.ceil(len(score_cols) / n_cols_box))
            
            fig, axes = plt.subplots(n_rows_box, n_cols_box, figsize=(16, 4*n_rows_box))
            axes = axes.flatten() if n_rows_box > 1 else [axes] if n_cols_box == 1 else axes
            
            for idx, col in enumerate(score_cols[:n_cols_box*n_rows_box]):
                axes[idx].boxplot(df[col].dropna())
                axes[idx].set_title(f'Boxplot: {col}')
                axes[idx].set_ylabel('Value')
                axes[idx].grid(True, alpha=0.3)
            
            for idx in range(len(score_cols[:n_cols_box*n_rows_box]), len(axes)):
                axes[idx].axis('off')
            
            plt.tight_layout()
            plt.savefig('results/eda/boxplots_outlier_detection.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("  Saved: results/eda/boxplots_outlier_detection.png")
        
        # 2.6 Correlation Matrix
        print("\n[2.6] Generating Correlation Matrix...")
        # Select numeric columns for correlation (excluding user_id)
        corr_cols = [col for col in numeric_cols if col not in ['user_id']]
        if len(corr_cols) > 15:
            corr_cols = corr_cols[:15]  # Limit for readability
        
        correlation_matrix = df[corr_cols].corr()
        
        plt.figure(figsize=(14, 12))
        sns.heatmap(correlation_matrix, annot=True, fmt='.2f', cmap='coolwarm', 
                   center=0, square=True, linewidths=1, cbar_kws={"shrink": 0.8})
        plt.title('Correlation Matrix - Numerical Features')
        plt.tight_layout()
        plt.savefig('results/eda/correlation_matrix.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  Saved: results/eda/correlation_matrix.png")
        
        # 2.7 Class Distribution (Target Variable)
        print("\n[2.7] Target Variable Distribution...")
        if 'specialization_label' in df.columns:
            target_dist = df['specialization_label'].value_counts()
            print("\nClass Distribution (Target Variable):")
            print(target_dist)
            
            target_dist.to_csv('results/eda/target_distribution.csv')
            
            plt.figure(figsize=(14, 8))
            target_dist.plot(kind='bar')
            plt.title('Target Variable Distribution (Specialization Label)')
            plt.xlabel('Specialization')
            plt.ylabel('Count')
            plt.xticks(rotation=45, ha='right')
            plt.grid(True, alpha=0.3, axis='y')
            plt.tight_layout()
            plt.savefig('results/eda/target_distribution.png', dpi=300, bbox_inches='tight')
            plt.close()
            print("  Saved: results/eda/target_distribution.png")
            
            # Calculate class imbalance
            imbalance_ratio = target_dist.max() / target_dist.min()
            print(f"\nClass Imbalance Ratio: {imbalance_ratio:.2f}")
            if imbalance_ratio > 2:
                print("  [WARNING] Significant class imbalance detected!")
        
        # 2.8 Outlier Detection using IQR
        print("\n[2.8] Outlier Detection using IQR Method...")
        outlier_summary = {}
        for col in numeric_cols_plot[:20]:  # Check first 20 numeric columns
            Q1 = df[col].quantile(0.25)
            Q3 = df[col].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            outliers = df[(df[col] < lower_bound) | (df[col] > upper_bound)][col]
            outlier_count = len(outliers)
            outlier_pct = (outlier_count / len(df)) * 100
            outlier_summary[col] = {
                'count': outlier_count,
                'percentage': outlier_pct,
                'lower_bound': lower_bound,
                'upper_bound': upper_bound
            }
        
        outlier_df = pd.DataFrame(outlier_summary).T
        outlier_df = outlier_df.sort_values('count', ascending=False)
        outlier_df.to_csv('results/eda/outlier_detection_iqr.csv')
        
        print("\nTop 10 Columns with Most Outliers:")
        print(outlier_df.head(10)[['count', 'percentage']].to_string())
        print("  Saved: results/eda/outlier_detection_iqr.csv")
        
        # Store EDA results
        self.eda_results = {
            'missing_analysis': missing_analysis if len(missing_analysis) > 0 else pd.DataFrame(),
            'duplicate_count': duplicate_count,
            'correlation_matrix': correlation_matrix,
            'outlier_summary': outlier_df,
            'descriptive_stats': desc_stats
        }
        
        print("\n[OK] EDA completed!")
        return self.eda_results
    
    # ========================================
    # STEP 3: DATA CLEANING
    # ========================================
    def step3_data_cleaning(self):
        """Step 3: Clean the data"""
        print("\n" + "="*70)
        print("STEP 3: DATA CLEANING")
        print("="*70)
        
        df = self.df_raw.copy()
        
        print(f"\n[3.0] Initial Dataset Shape: {df.shape}")
        
        # 3.1 Remove Duplicates
        print("\n[3.1] Removing Duplicates...")
        duplicates_before = df.duplicated().sum()
        print(f"  - Duplicate rows before: {duplicates_before:,}")
        df = df.drop_duplicates()
        print(f"  - Duplicate rows removed: {duplicates_before:,}")
        print(f"  - Dataset shape after: {df.shape}")
        
        # 3.2 Fix Inconsistent Values
        print("\n[3.2] Fixing Inconsistent Values...")
        
        # Question scores should be 0-3
        question_cols = [f'q{i}_score' for i in range(1, 26)]
        for col in question_cols:
            if col in df.columns:
                # Fix negative values
                negative_count = (df[col] < 0).sum()
                if negative_count > 0:
                    print(f"  - {col}: Fixed {negative_count} negative values")
                    df[col] = df[col].clip(lower=0)
                
                # Fix values > 3
                high_count = (df[col] > 3).sum()
                if high_count > 0:
                    print(f"  - {col}: Fixed {high_count} values > 3")
                    df[col] = df[col].clip(upper=3)
        
        # Score columns should be 0-100
        score_cols = ['practical_test_score', 'logical_reasoning_score', 'problem_solving_score']
        for col in score_cols:
            if col in df.columns:
                negative_count = (df[col] < 0).sum()
                high_count = (df[col] > 100).sum()
                if negative_count > 0 or high_count > 0:
                    print(f"  - {col}: Fixed {negative_count} negative and {high_count} > 100 values")
                    df[col] = df[col].clip(lower=0, upper=100)
        
        # Time should be positive
        if 'time_spent_minutes' in df.columns:
            negative_time = (df['time_spent_minutes'] < 0).sum()
            if negative_time > 0:
                print(f"  - time_spent_minutes: Fixed {negative_time} negative values")
                df['time_spent_minutes'] = df['time_spent_minutes'].clip(lower=0)
        
        # 3.3 Handle Missing Values
        print("\n[3.3] Handling Missing Values...")
        
        missing_before = df.isnull().sum().sum()
        print(f"  - Total missing values before: {missing_before:,}")
        
        # Strategy 1: Mean imputation for question scores
        for col in question_cols:
            if col in df.columns and df[col].isnull().sum() > 0:
                mean_val = df[col].mean()
                missing_count = df[col].isnull().sum()
                df[col] = df[col].fillna(mean_val)
                print(f"  - {col}: Filled {missing_count} missing values with mean ({mean_val:.2f})")
        
        # Strategy 2: KNN imputation for other numeric columns
        numeric_cols = ['practical_test_score', 'logical_reasoning_score', 
                       'problem_solving_score', 'time_spent_minutes',
                       'previous_level', 'current_level', 'improvement_rate']
        numeric_cols = [col for col in numeric_cols if col in df.columns]
        
        missing_numeric = df[numeric_cols].isnull().sum()
        if missing_numeric.sum() > 0:
            print(f"  - Applying KNN imputation for numeric columns...")
            knn_imputer = KNNImputer(n_neighbors=5)
            df[numeric_cols] = knn_imputer.fit_transform(df[numeric_cols])
            print(f"  - KNN imputation completed")
        
        missing_after = df.isnull().sum().sum()
        print(f"  - Total missing values after: {missing_after:,}")
        print(f"  - Missing values removed: {missing_before - missing_after:,}")
        
        # 3.4 Handle Outliers
        print("\n[3.4] Handling Outliers...")
        
        # Clip outliers using IQR method for time_spent_minutes
        if 'time_spent_minutes' in df.columns:
            Q1 = df['time_spent_minutes'].quantile(0.25)
            Q3 = df['time_spent_minutes'].quantile(0.75)
            IQR = Q3 - Q1
            lower_bound = Q1 - 1.5 * IQR
            upper_bound = Q3 + 1.5 * IQR
            
            outliers_before = ((df['time_spent_minutes'] < lower_bound) | 
                              (df['time_spent_minutes'] > upper_bound)).sum()
            df['time_spent_minutes'] = df['time_spent_minutes'].clip(lower_bound, upper_bound)
            print(f"  - time_spent_minutes: Clipped {outliers_before} outliers (IQR method)")
        
        # Clip score outliers (should be 0-100)
        for col in score_cols:
            if col in df.columns:
                outliers = ((df[col] < 0) | (df[col] > 100)).sum()
                if outliers > 0:
                    df[col] = df[col].clip(0, 100)
                    print(f"  - {col}: Clipped {outliers} outliers to [0, 100]")
        
        # Store cleaned data
        self.df_cleaned = df.copy()
        
        # Calculate after statistics
        self.after_stats = {
            'rows': len(df),
            'columns': len(df.columns),
            'missing_total': df.isnull().sum().sum(),
            'duplicates': df.duplicated().sum(),
            'memory_mb': df.memory_usage(deep=True).sum() / 1024**2
        }
        
        # Save cleaning summary
        cleaning_summary = pd.DataFrame({
            'Metric': ['Rows', 'Columns', 'Missing Values', 'Duplicates'],
            'Before': [
                self.before_stats['rows'],
                self.before_stats['columns'],
                self.before_stats['missing_total'],
                self.before_stats['duplicates']
            ],
            'After': [
                self.after_stats['rows'],
                self.after_stats['columns'],
                self.after_stats['missing_total'],
                self.after_stats['duplicates']
            ],
            'Difference': [
                self.after_stats['rows'] - self.before_stats['rows'],
                self.after_stats['columns'] - self.before_stats['columns'],
                self.after_stats['missing_total'] - self.before_stats['missing_total'],
                self.after_stats['duplicates'] - self.before_stats['duplicates']
            ]
        })
        cleaning_summary.to_csv('results/cleaning/cleaning_summary.csv', index=False)
        
        print(f"\n[3.5] Cleaning Summary:")
        print(f"  - Rows: {self.before_stats['rows']:,} -> {self.after_stats['rows']:,} "
              f"({self.after_stats['rows'] - self.before_stats['rows']:,} removed)")
        print(f"  - Missing values: {self.before_stats['missing_total']:,} -> {self.after_stats['missing_total']:,} "
              f"({self.before_stats['missing_total'] - self.after_stats['missing_total']:,} filled)")
        print(f"  - Duplicates: {self.before_stats['duplicates']:,} -> {self.after_stats['duplicates']:,} "
              f"({self.before_stats['duplicates'] - self.after_stats['duplicates']:,} removed)")
        
        print("\n[OK] Data cleaning completed!")
        return self.df_cleaned
    
    # ========================================
    # STEP 4: DATA PREPROCESSING (AFTER CLEANING)
    # ========================================
    def step4_preprocessing(self):
        """Step 4: Preprocess cleaned data"""
        print("\n" + "="*70)
        print("STEP 4: DATA PREPROCESSING (AFTER CLEANING)")
        print("="*70)
        
        df = self.df_cleaned.copy()
        
        # 4.1 Encode Categorical Variables
        print("\n[4.1] Encoding Categorical Variables...")
        if 'filiere' in df.columns:
            df['filiere_encoded'] = self.label_encoder.fit_transform(df['filiere'])
            print(f"  - Encoded 'filiere' into {len(self.label_encoder.classes_)} categories")
            print(f"    Categories: {list(self.label_encoder.classes_)}")
        
        # 4.2 Prepare Features and Target
        print("\n[4.2] Preparing Features and Target...")
        question_cols = [f'q{i}_score' for i in range(1, 26) if f'q{i}_score' in df.columns]
        numeric_cols = ['practical_test_score', 'logical_reasoning_score', 
                       'problem_solving_score', 'time_spent_minutes',
                       'previous_level', 'current_level', 'improvement_rate']
        numeric_cols = [col for col in numeric_cols if col in df.columns]
        
        # Add encoded filiere if exists
        if 'filiere_encoded' in df.columns:
            feature_cols = question_cols + numeric_cols + ['filiere_encoded']
        else:
            feature_cols = question_cols + numeric_cols
        
        # Prepare X and y
        X = df[feature_cols].copy()
        
        if 'specialization_label' in df.columns:
            y = df['specialization_label'].copy()
            # Encode target
            target_encoder = LabelEncoder()
            y_encoded = target_encoder.fit_transform(y)
            self.class_names = target_encoder.classes_
            print(f"  - Target variable: {len(self.class_names)} classes")
            print(f"    Classes: {list(self.class_names[:5])}{'...' if len(self.class_names) > 5 else ''}")
        else:
            raise ValueError("Target variable 'specialization_label' not found in dataset")
        
        self.feature_names = feature_cols
        print(f"  - Features: {len(feature_cols)} columns")
        print(f"    Feature names: {feature_cols[:5]}{'...' if len(feature_cols) > 5 else ''}")
        
        # 4.3 Train/Test Split
        print("\n[4.3] Train/Test Split...")
        X_train, X_test, y_train, y_test = train_test_split(
            X, y_encoded, test_size=0.2, random_state=42, stratify=y_encoded
        )
        
        # Additional validation split
        X_train_final, X_val, y_train_final, y_val = train_test_split(
            X_train, y_train, test_size=0.2, random_state=42, stratify=y_train
        )
        
        print(f"  - Training set: {X_train_final.shape}")
        print(f"  - Validation set: {X_val.shape}")
        print(f"  - Test set: {X_test.shape}")
        
        # 4.4 Scaling/Normalization
        print("\n[4.4] Feature Scaling (Standardization)...")
        self.X_train = X_train_final
        self.X_test = X_test
        self.y_train = y_train_final
        self.y_test = y_test
        
        # Scale features
        self.X_train_scaled = self.scaler.fit_transform(self.X_train)
        self.X_test_scaled = self.scaler.transform(self.X_test)
        self.X_val_scaled = self.scaler.transform(X_val)
        
        print(f"  - StandardScaler fitted on training data")
        print(f"  - Mean: {self.scaler.mean_[:5]}")
        print(f"  - Scale: {self.scaler.scale_[:5]}")
        
        # Store processed data
        self.df_processed = df.copy()
        
        print("\n[OK] Data preprocessing completed!")
        return self.X_train, self.X_test, self.y_train, self.y_test
    
    # ========================================
    # STEP 5: MODEL SELECTION
    # ========================================
    def step5_model_selection(self):
        """Step 5: Train and compare multiple models"""
        print("\n" + "="*70)
        print("STEP 5: MODEL SELECTION & TRAINING")
        print("="*70)
        
        # Define models (as per academic requirements)
        models_to_train = {
            'Logistic Regression': LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1),
            'KNN': KNeighborsClassifier(n_neighbors=5, n_jobs=-1),
            'Decision Tree': DecisionTreeClassifier(random_state=42, max_depth=20),
            'Random Forest': RandomForestClassifier(n_estimators=100, random_state=42, n_jobs=-1, max_depth=20),
            'SVM': SVC(kernel='rbf', random_state=42, probability=True)
        }
        
        print(f"\n[5.1] Training {len(models_to_train)} models...")
        print(f"  Models: {', '.join(models_to_train.keys())}")
        
        results = {}
        
        for name, model in models_to_train.items():
            print(f"\n[5.2] Training {name}...")
            
            try:
                # Determine if model needs scaled data
                needs_scaling = name in ['Logistic Regression', 'KNN', 'SVM']
                X_train_use = self.X_train_scaled if needs_scaling else self.X_train
                X_test_use = self.X_test_scaled if needs_scaling else self.X_test
                
                # Train model
                start_time = datetime.now()
                model.fit(X_train_use, self.y_train)
                training_time = (datetime.now() - start_time).total_seconds()
                
                # Predictions
                y_train_pred = model.predict(X_train_use)
                y_test_pred = model.predict(X_test_use)
                
                # Calculate metrics
                train_acc = accuracy_score(self.y_train, y_train_pred)
                test_acc = accuracy_score(self.y_test, y_test_pred)
                test_precision = precision_score(self.y_test, y_test_pred, average='weighted', zero_division=0)
                test_recall = recall_score(self.y_test, y_test_pred, average='weighted', zero_division=0)
                test_f1 = f1_score(self.y_test, y_test_pred, average='weighted', zero_division=0)
                
                # Calculate overfitting
                overfitting = train_acc - test_acc
                
                # Cross-validation
                cv_scores = cross_val_score(model, X_train_use, self.y_train, cv=5, scoring='accuracy', n_jobs=-1)
                
                results[name] = {
                    'model': model,
                    'train_accuracy': train_acc,
                    'test_accuracy': test_acc,
                    'precision': test_precision,
                    'recall': test_recall,
                    'f1_score': test_f1,
                    'overfitting': overfitting,
                    'cv_mean': cv_scores.mean(),
                    'cv_std': cv_scores.std(),
                    'training_time': training_time,
                    'y_test_pred': y_test_pred
                }
                
                print(f"  [OK] {name} trained")
                print(f"    - Train Accuracy: {train_acc:.4f}")
                print(f"    - Test Accuracy: {test_acc:.4f}")
                print(f"    - CV Mean Accuracy: {cv_scores.mean():.4f} (+/- {cv_scores.std()*2:.4f})")
                print(f"    - Training Time: {training_time:.2f}s")
                
            except Exception as e:
                print(f"  [ERROR] Failed to train {name}: {str(e)}")
                continue
        
        self.models = models_to_train
        self.model_results = results
        
        # Select best model based on test accuracy
        if results:
            best_model_name = max(results.keys(), key=lambda x: results[x]['test_accuracy'])
            self.best_model_name = best_model_name
            self.best_model = results[best_model_name]['model']
            
            print(f"\n[5.3] Best Model Selected:")
            print(f"  - Model: {best_model_name}")
            print(f"  - Test Accuracy: {results[best_model_name]['test_accuracy']:.4f}")
            print(f"  - F1-Score: {results[best_model_name]['f1_score']:.4f}")
        
        print("\n[OK] Model selection completed!")
        return results
    
    # ========================================
    # STEP 6: MODEL EVALUATION
    # ========================================
    def step6_evaluation(self):
        """Step 6: Comprehensive Model Evaluation"""
        print("\n" + "="*70)
        print("STEP 6: MODEL EVALUATION")
        print("="*70)
        
        if not self.model_results:
            print("[ERROR] No models to evaluate. Train models first.")
            return None
        
        # 6.1 Model Comparison Table
        print("\n[6.1] Model Comparison...")
        comparison_data = []
        for name, results in self.model_results.items():
            comparison_data.append({
                'Model': name,
                'Train Accuracy': results['train_accuracy'],
                'Test Accuracy': results['test_accuracy'],
                'Precision': results['precision'],
                'Recall': results['recall'],
                'F1-Score': results['f1_score'],
                'Overfitting': results['overfitting'],
                'CV Mean': results['cv_mean'],
                'CV Std': results['cv_std'],
                'Training Time (s)': results['training_time']
            })
        
        comparison_df = pd.DataFrame(comparison_data)
        comparison_df = comparison_df.sort_values('Test Accuracy', ascending=False)
        print("\nModel Comparison:")
        print(comparison_df.to_string(index=False))
        comparison_df.to_csv('results/evaluation/model_comparison.csv', index=False)
        print("  Saved: results/evaluation/model_comparison.csv")
        
        # 6.2 Model Comparison Visualization
        print("\n[6.2] Generating Model Comparison Charts...")
        fig, axes = plt.subplots(2, 2, figsize=(16, 12))
        
        # Accuracy comparison
        axes[0, 0].bar(comparison_df['Model'], comparison_df['Test Accuracy'], alpha=0.7)
        axes[0, 0].set_title('Test Accuracy Comparison')
        axes[0, 0].set_ylabel('Accuracy')
        axes[0, 0].tick_params(axis='x', rotation=45)
        axes[0, 0].grid(True, alpha=0.3, axis='y')
        
        # Metrics comparison
        x_pos = np.arange(len(comparison_df))
        width = 0.15
        axes[0, 1].bar(x_pos - 2*width, comparison_df['Test Accuracy'], width, label='Accuracy', alpha=0.7)
        axes[0, 1].bar(x_pos - width, comparison_df['Precision'], width, label='Precision', alpha=0.7)
        axes[0, 1].bar(x_pos, comparison_df['Recall'], width, label='Recall', alpha=0.7)
        axes[0, 1].bar(x_pos + width, comparison_df['F1-Score'], width, label='F1-Score', alpha=0.7)
        axes[0, 1].set_title('All Metrics Comparison')
        axes[0, 1].set_ylabel('Score')
        axes[0, 1].set_xticks(x_pos)
        axes[0, 1].set_xticklabels(comparison_df['Model'], rotation=45, ha='right')
        axes[0, 1].legend()
        axes[0, 1].grid(True, alpha=0.3, axis='y')
        
        # Overfitting analysis
        axes[1, 0].bar(comparison_df['Model'], comparison_df['Train Accuracy'], alpha=0.7, label='Train', color='blue')
        axes[1, 0].bar(comparison_df['Model'], comparison_df['Test Accuracy'], alpha=0.7, label='Test', color='orange')
        axes[1, 0].set_title('Train vs Test Accuracy (Overfitting Analysis)')
        axes[1, 0].set_ylabel('Accuracy')
        axes[1, 0].tick_params(axis='x', rotation=45)
        axes[1, 0].legend()
        axes[1, 0].grid(True, alpha=0.3, axis='y')
        
        # Training time comparison
        axes[1, 1].bar(comparison_df['Model'], comparison_df['Training Time (s)'], alpha=0.7)
        axes[1, 1].set_title('Training Time Comparison')
        axes[1, 1].set_ylabel('Time (seconds)')
        axes[1, 1].tick_params(axis='x', rotation=45)
        axes[1, 1].grid(True, alpha=0.3, axis='y')
        
        plt.tight_layout()
        plt.savefig('results/evaluation/model_comparison.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  Saved: results/evaluation/model_comparison.png")
        
        # 6.3 Confusion Matrices
        print("\n[6.3] Generating Confusion Matrices...")
        n_models = len(self.model_results)
        n_cols = min(3, n_models)
        n_rows = int(np.ceil(n_models / n_cols))
        
        fig, axes = plt.subplots(n_rows, n_cols, figsize=(6*n_cols, 5*n_rows))
        if n_rows == 1:
            axes = axes.reshape(1, -1) if n_cols > 1 else [axes]
        else:
            axes = axes.flatten()
        
        for idx, (name, results) in enumerate(self.model_results.items()):
            cm = confusion_matrix(self.y_test, results['y_test_pred'])
            sns.heatmap(cm, annot=True, fmt='d', cmap='Blues', ax=axes[idx],
                       xticklabels=self.class_names[:10] if len(self.class_names) <= 10 else range(len(self.class_names)),
                       yticklabels=self.class_names[:10] if len(self.class_names) <= 10 else range(len(self.class_names)))
            axes[idx].set_title(f'{name}\nAccuracy: {results["test_accuracy"]:.3f}')
            axes[idx].set_xlabel('Predicted')
            axes[idx].set_ylabel('True')
        
        # Hide empty subplots
        for idx in range(len(self.model_results), len(axes)):
            axes[idx].axis('off')
        
        plt.tight_layout()
        plt.savefig('results/evaluation/confusion_matrices.png', dpi=300, bbox_inches='tight')
        plt.close()
        print("  Saved: results/evaluation/confusion_matrices.png")
        
        # 6.4 Best Model Detailed Evaluation
        if self.best_model_name:
            print(f"\n[6.4] Best Model Detailed Evaluation: {self.best_model_name}")
            best_results = self.model_results[self.best_model_name]
            
            # Classification report
            report = classification_report(self.y_test, best_results['y_test_pred'], 
                                         target_names=self.class_names, output_dict=True)
            report_df = pd.DataFrame(report).transpose()
            report_df.to_csv('results/evaluation/classification_report_best_model.csv')
            
            print("\nClassification Report (Best Model):")
            print(classification_report(self.y_test, best_results['y_test_pred'], 
                                      target_names=self.class_names))
            print("  Saved: results/evaluation/classification_report_best_model.csv")
        
        print("\n[OK] Model evaluation completed!")
        return comparison_df
    
    # ========================================
    # STEP 7: MODEL IMPROVEMENT
    # ========================================
    def step7_model_improvement(self):
        """Step 7: Hyperparameter Tuning for Best Model"""
        print("\n" + "="*70)
        print("STEP 7: MODEL IMPROVEMENT (HYPERPARAMETER TUNING)")
        print("="*70)
        
        if not self.best_model_name:
            print("[ERROR] No best model selected. Run model selection first.")
            return None
        
        print(f"\n[7.1] Hyperparameter Tuning for: {self.best_model_name}")
        
        # Determine if model needs scaled data
        needs_scaling = self.best_model_name in ['Logistic Regression', 'KNN', 'SVM']
        X_train_use = self.X_train_scaled if needs_scaling else self.X_train
        
        # Define parameter grids based on model type
        if self.best_model_name == 'Random Forest':
            param_grid = {
                'n_estimators': [100, 200],
                'max_depth': [15, 20, 25],
                'min_samples_split': [2, 5]
            }
            base_model = RandomForestClassifier(random_state=42, n_jobs=-1)
        elif self.best_model_name == 'Decision Tree':
            param_grid = {
                'max_depth': [15, 20, 25],
                'min_samples_split': [2, 5, 10],
                'min_samples_leaf': [1, 2]
            }
            base_model = DecisionTreeClassifier(random_state=42)
        elif self.best_model_name == 'Logistic Regression':
            param_grid = {
                'C': [0.1, 1.0, 10.0],
                'solver': ['lbfgs', 'liblinear']
            }
            base_model = LogisticRegression(max_iter=1000, random_state=42, n_jobs=-1)
        elif self.best_model_name == 'KNN':
            param_grid = {
                'n_neighbors': [3, 5, 7, 9],
                'weights': ['uniform', 'distance']
            }
            base_model = KNeighborsClassifier(n_jobs=-1)
        else:
            print(f"  [INFO] Hyperparameter tuning not implemented for {self.best_model_name}")
            print("  Using default model")
            return self.best_model
        
        print(f"\n[7.2] Performing Grid Search...")
        print(f"  Parameter grid: {param_grid}")
        
        try:
            grid_search = GridSearchCV(
                base_model, 
                param_grid, 
                cv=3,  # Reduced for speed
                scoring='accuracy',
                n_jobs=-1,
                verbose=1
            )
            
            grid_search.fit(X_train_use, self.y_train)
            
            print(f"\n[7.3] Best Parameters Found:")
            for param, value in grid_search.best_params_.items():
                print(f"  - {param}: {value}")
            print(f"  - Best CV Score: {grid_search.best_score_:.4f}")
            
            # Evaluate tuned model
            best_tuned_model = grid_search.best_estimator_
            
            if needs_scaling:
                y_test_pred_tuned = best_tuned_model.predict(self.X_test_scaled)
            else:
                y_test_pred_tuned = best_tuned_model.predict(self.X_test)
            
            tuned_accuracy = accuracy_score(self.y_test, y_test_pred_tuned)
            
            # Compare with original
            original_accuracy = self.model_results[self.best_model_name]['test_accuracy']
            improvement = tuned_accuracy - original_accuracy
            
            print(f"\n[7.4] Tuned Model Performance:")
            print(f"  - Original Accuracy: {original_accuracy:.4f}")
            print(f"  - Tuned Accuracy: {tuned_accuracy:.4f}")
            print(f"  - Improvement: {improvement:+.4f} ({improvement/original_accuracy*100:+.2f}%)")
            
            if improvement > 0:
                self.best_model = best_tuned_model
                print(f"  [OK] Tuned model is better! Using tuned model.")
            else:
                print(f"  [INFO] Original model is better. Keeping original model.")
            
        except Exception as e:
            print(f"  [WARNING] Grid search failed: {str(e)}")
            print(f"  Using original model")
        
        print("\n[OK] Model improvement completed!")
        return self.best_model
    
    # ========================================
    # STEP 8: SAVE MODEL & RESULTS
    # ========================================
    def step8_save_model(self):
        """Step 8: Save best model and all results"""
        print("\n" + "="*70)
        print("STEP 8: SAVING MODEL & RESULTS")
        print("="*70)
        
        if not self.best_model:
            print("[ERROR] No model to save. Train models first.")
            return None
        
        print("\n[8.1] Saving best model...")
        
        # Determine model needs scaling
        needs_scaling = self.best_model_name in ['Logistic Regression', 'KNN', 'SVM']
        
        model_data = {
            'model': self.best_model,
            'scaler': self.scaler if needs_scaling else None,
            'label_encoder': self.label_encoder,
            'class_names': self.class_names,
            'feature_names': self.feature_names,
            'model_name': self.best_model_name,
            'needs_scaling': needs_scaling
        }
        
        joblib.dump(model_data, 'models/best_model.pkl')
        print("  Saved: models/best_model.pkl")
        
        # Save preprocessing information
        preprocessing_info = {
            'feature_names': self.feature_names,
            'class_names': self.class_names.tolist(),
            'scaler_mean': self.scaler.mean_.tolist() if needs_scaling else None,
            'scaler_scale': self.scaler.scale_.tolist() if needs_scaling else None,
            'label_encoder_classes': self.label_encoder.classes_.tolist()
        }
        
        import json
        with open('models/preprocessing_info.json', 'w') as f:
            json.dump(preprocessing_info, f, indent=2)
        print("  Saved: models/preprocessing_info.json")
        
        print("\n[OK] Model and results saved!")
        return model_data
    
    # ========================================
    # RUN COMPLETE PIPELINE
    # ========================================
    def run_complete_pipeline(self):
        """Run the complete academic ML pipeline"""
        print("\n" + "="*70)
        print("ACADEMIC MACHINE LEARNING PIPELINE")
        print("Following Strict University Methodology")
        print("="*70)
        
        try:
            # Step 1: Dataset Description
            self.step1_dataset_description()
            
            # Step 2: EDA (BEFORE cleaning)
            self.step2_eda()
            
            # Step 3: Data Cleaning
            self.step3_data_cleaning()
            
            # Step 4: Preprocessing (AFTER cleaning)
            self.step4_preprocessing()
            
            # Step 5: Model Selection & Training
            self.step5_model_selection()
            
            # Step 6: Model Evaluation
            self.step6_evaluation()
            
            # Step 7: Model Improvement
            self.step7_model_improvement()
            
            # Step 8: Save Model
            self.step8_save_model()
            
            print("\n" + "="*70)
            print("PIPELINE COMPLETED SUCCESSFULLY!")
            print("="*70)
            print(f"\nBest Model: {self.best_model_name}")
            if self.best_model_name:
                best_results = self.model_results[self.best_model_name]
                print(f"Test Accuracy: {best_results['test_accuracy']:.4f}")
                print(f"F1-Score: {best_results['f1_score']:.4f}")
            
            print("\nGenerated Files:")
            print("  - results/eda/ (EDA visualizations)")
            print("  - results/cleaning/ (Cleaning summaries)")
            print("  - results/evaluation/ (Model comparisons)")
            print("  - models/best_model.pkl (Trained model)")
            
            return {
                'best_model': self.best_model_name,
                'results': self.model_results,
                'before_stats': self.before_stats,
                'after_stats': self.after_stats
            }
            
        except Exception as e:
            print(f"\n[ERROR] Pipeline failed: {str(e)}")
            import traceback
            traceback.print_exc()
            return None

if __name__ == "__main__":
    pipeline = AcademicMLPipeline()
    results = pipeline.run_complete_pipeline()

