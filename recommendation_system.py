"""
Recommendation System
Provides personalized improvement recommendations based on predictions and feature importance
"""

import pandas as pd
import numpy as np
from typing import Dict, List

class RecommendationSystem:
    """
    Generates personalized recommendations for students
    """
    
    def __init__(self, model, feature_importance, class_names):
        self.model = model
        self.feature_importance = feature_importance
        self.class_names = class_names
        
        # Skill mapping
        self.skill_mapping = {
            'q1_score': 'ML Theory',
            'q2_score': 'Data Preprocessing',
            'q3_score': 'Model Evaluation',
            'q4_score': 'Python',
            'q5_score': 'Data Preprocessing',
            'q6_score': 'Model Evaluation',
            'q7_score': 'ML Theory',
            'q8_score': 'Deep Learning',
            'q9_score': 'Ensemble Methods',
            'q10_score': 'Model Optimization',
            'practical_test_score': 'Practical Skills',
            'logical_reasoning_score': 'Logical Reasoning',
            'problem_solving_score': 'Problem Solving',
            'time_spent_minutes': 'Time Management'
        }
        
        # Learning resources
        self.learning_resources = {
            'ML Theory': [
                'Coursera: Machine Learning by Andrew Ng',
                'Book: Pattern Recognition and Machine Learning',
                'Documentation: Scikit-learn User Guide'
            ],
            'Data Preprocessing': [
                'Kaggle: Data Cleaning Course',
                'Book: Python for Data Analysis',
                'Practice: Real-world datasets on Kaggle'
            ],
            'Model Evaluation': [
                'Article: Understanding Classification Metrics',
                'Practice: Build and evaluate multiple models',
                'Documentation: Scikit-learn Model Evaluation'
            ],
            'Python': [
                'Codecademy: Python Course',
                'Practice: LeetCode Python problems',
                'Book: Fluent Python'
            ],
            'Deep Learning': [
                'Fast.ai: Practical Deep Learning',
                'Book: Deep Learning by Ian Goodfellow',
                'Course: CS231n Stanford'
            ],
            'Practical Skills': [
                'Kaggle Competitions',
                'Personal Projects',
                'GitHub: Contribute to ML projects'
            ],
            'Logical Reasoning': [
                'Practice: Logic puzzles',
                'Book: Thinking, Fast and Slow',
                'Course: Critical Thinking'
            ],
            'Problem Solving': [
                'LeetCode: Algorithm problems',
                'HackerRank: Practice problems',
                'Book: Algorithm Design Manual'
            ]
        }
    
    def analyze_user_performance(self, user_data: Dict) -> Dict:
        """
        Analyze user performance and identify weaknesses
        """
        # Extract question scores
        question_scores = {}
        for i in range(1, 26):
            key = f'q{i}_score'
            if key in user_data:
                question_scores[key] = user_data[key]
        
        # Calculate average scores per skill category
        skill_scores = {}
        for q, skill in self.skill_mapping.items():
            if q in question_scores:
                if skill not in skill_scores:
                    skill_scores[skill] = []
                score = question_scores[q]
                if not pd.isna(score):
                    skill_scores[skill].append(score)
        
        # Average scores per skill
        avg_skill_scores = {
            skill: np.mean(scores) if scores else 0
            for skill, scores in skill_scores.items()
        }
        
        # Identify weak areas (scores < 2.0 on 0-3 scale)
        weak_skills = [
            skill for skill, score in avg_skill_scores.items()
            if score < 2.0
        ]
        
        return {
            'skill_scores': avg_skill_scores,
            'weak_skills': weak_skills,
            'overall_average': np.mean(list(avg_skill_scores.values())) if avg_skill_scores else 0
        }
    
    def generate_recommendations(self, user_data: Dict, predicted_specialization: str, 
                                previous_level: int = None, current_level: int = None) -> Dict:
        """
        Generate personalized recommendations
        """
        # Analyze performance
        performance = self.analyze_user_performance(user_data)
        
        # Determine improvement message
        if previous_level and current_level:
            if current_level > previous_level:
                improvement_message = "Bravo, votre niveau s'est amélioré ! Continuez sur cette voie."
            elif current_level == previous_level:
                improvement_message = "Votre niveau est stable. Votre progression nécessite plus de pratique."
            else:
                improvement_message = "Votre niveau a diminué. Il est temps de revoir les bases et de pratiquer davantage."
        else:
            improvement_message = "Continuez à pratiquer pour améliorer vos compétences."
        
        # Get feature importance for predicted specialization
        # Identify which features are most important for this specialization
        top_features = self.feature_importance.head(10)['feature'].tolist()
        
        # Generate skill recommendations
        skill_recommendations = []
        for skill in performance['weak_skills'][:5]:  # Top 5 weak skills
            skill_recommendations.append({
                'skill': skill,
                'current_level': performance['skill_scores'].get(skill, 0),
                'resources': self.learning_resources.get(skill, ['Practice more'])
            })
        
        # If no weak skills, recommend based on specialization requirements
        if not skill_recommendations:
            specialization_skills = {
                'Machine Learning Engineer': ['ML Theory', 'Python', 'Model Evaluation'],
                'Data Scientist': ['Statistics', 'Data Analysis', 'Python'],
                'Cybersecurity Analyst': ['Network Security', 'Threat Analysis', 'Security Monitoring'],
                'Full-Stack Developer': ['Web Development', 'API Design', 'Database']
            }
            
            required_skills = specialization_skills.get(predicted_specialization, [])
            for skill in required_skills[:3]:
                skill_recommendations.append({
                    'skill': skill,
                    'current_level': performance['skill_scores'].get(skill, 0),
                    'resources': self.learning_resources.get(skill, ['Practice more'])
                })
        
        # Topics to study
        topics_to_study = []
        if performance['weak_skills']:
            topics_to_study = performance['weak_skills'][:3]
        else:
            topics_to_study = ['Advanced ' + predicted_specialization, 'Best Practices', 'Industry Standards']
        
        recommendations = {
            'improvement_message': improvement_message,
            'predicted_specialization': predicted_specialization,
            'overall_performance': performance['overall_average'],
            'skill_recommendations': skill_recommendations,
            'topics_to_study': topics_to_study,
            'learning_resources': self.learning_resources,
            'next_steps': [
                f"Focus on improving: {', '.join(performance['weak_skills'][:3])}",
                f"Practice {predicted_specialization} specific skills",
                "Take more practice tests to track progress",
                "Work on personal projects in your specialization"
            ]
        }
        
        return recommendations
    
    def get_progress_analysis(self, user_history: List[Dict]) -> Dict:
        """
        Analyze user progress over time
        """
        if not user_history:
            return {'message': 'No history available'}
        
        # Extract levels and scores over time
        levels = [h.get('current_level', 0) for h in user_history]
        scores = [h.get('practical_test_score', 0) for h in user_history]
        
        # Calculate trends
        if len(levels) > 1:
            level_trend = 'improving' if levels[-1] > levels[0] else 'stable' if levels[-1] == levels[0] else 'declining'
            score_trend = 'improving' if scores[-1] > scores[0] else 'stable' if scores[-1] == scores[0] else 'declining'
        else:
            level_trend = 'stable'
            score_trend = 'stable'
        
        return {
            'total_tests': len(user_history),
            'current_level': levels[-1] if levels else 0,
            'average_score': np.mean(scores) if scores else 0,
            'level_trend': level_trend,
            'score_trend': score_trend,
            'improvement_rate': (levels[-1] - levels[0]) / len(levels) if len(levels) > 1 else 0
        }

