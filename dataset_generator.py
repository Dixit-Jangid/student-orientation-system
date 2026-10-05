"""
Dataset Generator for Specialization Prediction System
Generates a realistic synthetic dataset with 50,000+ student test attempts
"""

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import random
import os

# Define specializations
SPECIALIZATIONS = {
    "Intelligence Artificielle & Sciences des Données": [
        "Machine Learning Engineer",
        "Data Scientist",
        "Data Engineer",
        "AI Researcher",
        "Computer Vision Engineer",
        "NLP Engineer"
    ],
    "Cybersécurité & Infrastructures Réseaux": [
        "Cloud Security Engineer",
        "Cybersecurity Analyst",
        "Penetration Tester",
        "SOC Analyst",
        "Network Security Engineer",
        "Digital Forensics Analyst"
    ],
    "Développement Digital & Systèmes d'Information": [
        "Full-Stack Developer",
        "Backend Developer",
        "Frontend Developer",
        "DevOps Engineer",
        "Cloud Application Engineer",
        "Software Architect"
    ]
}

def generate_realistic_scores(specialization, question_num, num_samples):
    """
    Generate realistic question scores based on specialization
    Different specializations have different skill profiles
    """
    scores = []
    
    # Base skill profiles for each specialization
    skill_profiles = {
        "Machine Learning Engineer": [0.85, 0.90, 0.80, 0.75, 0.70],
        "Data Scientist": [0.80, 0.85, 0.90, 0.75, 0.70],
        "Data Engineer": [0.75, 0.80, 0.85, 0.70, 0.65],
        "AI Researcher": [0.90, 0.85, 0.80, 0.85, 0.75],
        "Computer Vision Engineer": [0.85, 0.80, 0.75, 0.90, 0.70],
        "NLP Engineer": [0.85, 0.80, 0.75, 0.70, 0.90],
        "Cloud Security Engineer": [0.80, 0.75, 0.70, 0.85, 0.80],
        "Cybersecurity Analyst": [0.75, 0.80, 0.85, 0.80, 0.75],
        "Penetration Tester": [0.85, 0.80, 0.75, 0.90, 0.80],
        "SOC Analyst": [0.75, 0.80, 0.85, 0.75, 0.80],
        "Network Security Engineer": [0.80, 0.75, 0.85, 0.80, 0.75],
        "Digital Forensics Analyst": [0.75, 0.80, 0.85, 0.75, 0.85],
        "Full-Stack Developer": [0.85, 0.80, 0.75, 0.80, 0.75],
        "Backend Developer": [0.80, 0.85, 0.80, 0.75, 0.70],
        "Frontend Developer": [0.75, 0.80, 0.85, 0.70, 0.75],
        "DevOps Engineer": [0.80, 0.75, 0.80, 0.85, 0.80],
        "Cloud Application Engineer": [0.80, 0.75, 0.80, 0.85, 0.75],
        "Software Architect": [0.85, 0.80, 0.85, 0.80, 0.75]
    }
    
    base_prob = skill_profiles.get(specialization, [0.75] * 5)
    # Map question to skill category (cycling through 5 categories)
    skill_idx = (question_num - 1) % 5
    base_score = base_prob[skill_idx]
    
    # Generate scores with some variance
    for _ in range(num_samples):
        # Most students score around their specialization's strength
        # Normalize probabilities to sum to 1
        p_wrong = 1 - base_score
        p_partial_wrong = (1 - base_score) * 0.3
        p_partial_correct = base_score * 0.4
        p_correct = base_score * 0.6
        prob_sum = p_wrong + p_partial_wrong + p_partial_correct + p_correct
        probabilities = [
            p_wrong / prob_sum,
            p_partial_wrong / prob_sum,
            p_partial_correct / prob_sum,
            p_correct / prob_sum
        ]
        score = np.random.choice([0, 1, 2, 3], p=probabilities)
        scores.append(score)
    
    return scores

def generate_dataset(n_samples=5000):
    """
    Generate synthetic dataset with realistic patterns, missing values, outliers, and errors.
    Kept at a moderate size so the project can train reliably on local machines.
    """
    print(f"Generating {n_samples} samples...")
    
    data = {
        'user_id': [],
        'filiere': [],
        'specialization_label': [],
        'previous_level': [],
        'current_level': [],
        'time_spent_minutes': [],
        'practical_test_score': [],
        'logical_reasoning_score': [],
        'problem_solving_score': [],
        'improvement_rate': [],
        'test_date': []
    }
    
    # Add question columns
    for i in range(1, 26):
        data[f'q{i}_score'] = []
    
    # Generate user IDs (some users take multiple tests)
    unique_users = n_samples // 3  # Average 3 tests per user
    user_ids = list(range(1, unique_users + 1))
    
    # Create class imbalance (some specializations are more popular)
    specialization_weights = {
        "Machine Learning Engineer": 0.12,
        "Data Scientist": 0.10,
        "Data Engineer": 0.08,
        "AI Researcher": 0.06,
        "Computer Vision Engineer": 0.05,
        "NLP Engineer": 0.04,
        "Cloud Security Engineer": 0.08,
        "Cybersecurity Analyst": 0.10,
        "Penetration Tester": 0.05,
        "SOC Analyst": 0.07,
        "Network Security Engineer": 0.06,
        "Digital Forensics Analyst": 0.04,
        "Full-Stack Developer": 0.15,
        "Backend Developer": 0.10,
        "Frontend Developer": 0.08,
        "DevOps Engineer": 0.07,
        "Cloud Application Engineer": 0.06,
        "Software Architect": 0.05
    }
    
    all_specializations = []
    for filiere, specs in SPECIALIZATIONS.items():
        for spec in specs:
            all_specializations.append((filiere, spec))
    
    # Normalize probabilities to sum to 1
    weights_list = list(specialization_weights.values())
    weights_sum = sum(weights_list)
    normalized_weights = [w / weights_sum for w in weights_list]
    
    # Generate samples
    for i in range(n_samples):
        # Select specialization with class imbalance
        spec_choice = np.random.choice(len(all_specializations), p=normalized_weights)
        filiere, specialization = all_specializations[spec_choice]
        
        # User ID (some users appear multiple times)
        user_id = np.random.choice(user_ids)
        data['user_id'].append(user_id)
        data['filiere'].append(filiere)
        data['specialization_label'].append(specialization)
        
        # Previous and current level (1-5 scale)
        previous_level = np.random.choice([1, 2, 3, 4, 5], p=[0.1, 0.2, 0.3, 0.3, 0.1])
        current_level = previous_level + np.random.choice([-1, 0, 1], p=[0.1, 0.6, 0.3])
        current_level = max(1, min(5, current_level))
        data['previous_level'].append(previous_level)
        data['current_level'].append(current_level)
        
        # Improvement rate
        improvement = (current_level - previous_level) / 5.0
        data['improvement_rate'].append(improvement)
        
        # Time spent (with some outliers and errors)
        base_time = np.random.normal(45, 10)  # Average 45 minutes
        if np.random.random() < 0.02:  # 2% outliers
            base_time = np.random.choice([-5, 300, 500])  # Negative or very high
        data['time_spent_minutes'].append(max(0, base_time))
        
        # Generate question scores
        for q_num in range(1, 26):
            scores = generate_realistic_scores(specialization, q_num, 1)
            score = scores[0]
            
            # Add some missing values (5% of questions)
            if np.random.random() < 0.05:
                score = np.nan
            
            # Add some outliers (1% of questions)
            if np.random.random() < 0.01:
                score = np.random.choice([-1, 4, 5])
            
            data[f'q{q_num}_score'].append(score)
        
        # Practical test score (0-100)
        practical_score = np.random.normal(70, 15)
        if np.random.random() < 0.02:  # Outliers
            practical_score = np.random.choice([-10, 150])
        data['practical_test_score'].append(max(0, min(100, practical_score)))
        
        # Logical reasoning score (0-100)
        logical_score = np.random.normal(65, 12)
        data['logical_reasoning_score'].append(max(0, min(100, logical_score)))
        
        # Problem solving score (0-100)
        problem_score = np.random.normal(68, 14)
        data['problem_solving_score'].append(max(0, min(100, problem_score)))
        
        # Test date (last 2 years)
        days_ago = np.random.randint(0, 730)
        test_date = datetime.now() - timedelta(days=days_ago)
        data['test_date'].append(test_date.strftime('%Y-%m-%d'))
    
    # Create DataFrame
    df = pd.DataFrame(data)
    
    # Add some additional missing values randomly (2% of all values)
    missing_mask = np.random.random(df.shape) < 0.02
    df = df.mask(missing_mask)
    
    print(f"Dataset generated: {len(df)} rows, {len(df.columns)} columns")
    print(f"Missing values: {df.isnull().sum().sum()}")
    print(f"Specialization distribution:")
    print(df['specialization_label'].value_counts())
    
    return df

if __name__ == "__main__":
    # Generate dataset
    df = generate_dataset(n_samples=5000)

    # Save to CSV
    os.makedirs('dataset', exist_ok=True)
    df.to_csv('dataset/student_tests.csv', index=False)
    print("\nDataset saved to 'dataset/student_tests.csv'")

