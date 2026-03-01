"""
Script pour créer 5 tests avec progression pour l'utilisateur ibrahim
dans la filière dev (Développement Digital & Systèmes d'Information)
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from backend.database import SessionLocal, User, TestResult, PredictionHistory
# Import questions from main.py logic
import json
from datetime import datetime, timedelta
import random
import hashlib

def get_password_hash(password: str) -> str:
    """Hash password using SHA256"""
    return hashlib.sha256(password.encode('utf-8')).hexdigest()

def create_progression_tests():
    """Créer 5 tests avec progression pour ibrahim"""
    db = SessionLocal()
    
    try:
        # Trouver l'utilisateur ibrahim
        user = db.query(User).filter(User.username == 'ibrahim').first()
        
        if not user:
            print("Utilisateur 'ibrahim' non trouve. Creation de l'utilisateur...")
            # Créer l'utilisateur ibrahim
            user = User(
                username='ibrahim',
                email='ibrahim@example.com',
                hashed_password=get_password_hash('test123'),
                role='user'
            )
            db.add(user)
            db.commit()
            db.refresh(user)
            print(f"Utilisateur 'ibrahim' cree avec ID: {user.id}")
        else:
            print(f"Utilisateur 'ibrahim' trouve avec ID: {user.id}")
        
        # Récupérer les questions pour la filière "dev" depuis l'API
        # Ou utiliser des IDs de questions génériques
        # Pour simplifier, on va créer 25 questions avec des IDs génériques
        num_questions = 25
        dev_questions = [{'id': f'dev_q{i+1}'} for i in range(num_questions)]
        
        print(f"{len(dev_questions)} questions preparees pour la filiere 'dev'")
        
        # Dates pour les 5 tests (progression sur 2 mois)
        base_date = datetime.now() - timedelta(days=60)
        test_dates = [base_date + timedelta(days=i*15) for i in range(5)]
        
        # Niveaux de progression (1 à 5)
        levels = [1, 2, 2, 3, 4]
        
        # Scores de base qui augmentent progressivement
        base_scores = [
            {'practical': 45, 'logical': 50, 'problem': 48},  # Test 1 - Débutant
            {'practical': 55, 'logical': 58, 'problem': 56},  # Test 2 - Amélioration
            {'practical': 65, 'logical': 68, 'problem': 66},  # Test 3 - Intermédiaire
            {'practical': 75, 'logical': 78, 'problem': 76},  # Test 4 - Avancé
            {'practical': 85, 'logical': 88, 'problem': 86},  # Test 5 - Expert
        ]
        
        # Supprimer les anciens tests de ibrahim pour recommencer proprement
        old_tests = db.query(TestResult).filter(TestResult.user_id == user.id).all()
        old_predictions = db.query(PredictionHistory).filter(PredictionHistory.user_id == user.id).all()
        
        for old_test in old_tests:
            db.delete(old_test)
        for old_pred in old_predictions:
            db.delete(old_pred)
        
        db.commit()
        print(f"{len(old_tests)} anciens tests supprimes")
        
        # Créer les 5 tests avec progression
        for test_num in range(5):
            test_date = test_dates[test_num]
            level = levels[test_num]
            base_score = base_scores[test_num]
            
            # Générer des réponses avec progression (meilleures réponses au fil du temps)
            answers = {}
            practical_score = base_score['practical']
            logical_score = base_score['logical']
            problem_score = base_score['problem']
            
            # Pour chaque question, générer une réponse basée sur le niveau de progression
            for i, question in enumerate(dev_questions[:25]):  # Prendre les 25 premières questions
                question_id = question['id']
                
                # Plus le test est tardif, meilleures sont les réponses
                # Test 1: majorité de 0-1, Test 5: majorité de 2-3
                if test_num == 0:
                    # Débutant: beaucoup de 0 et 1
                    answer_value = random.choices([0, 1, 2], weights=[40, 40, 20])[0]
                elif test_num == 1:
                    # Amélioration: plus de 1 et 2
                    answer_value = random.choices([0, 1, 2, 3], weights=[20, 40, 30, 10])[0]
                elif test_num == 2:
                    # Intermédiaire: majorité de 2
                    answer_value = random.choices([1, 2, 3], weights=[30, 50, 20])[0]
                elif test_num == 3:
                    # Avancé: beaucoup de 2 et 3
                    answer_value = random.choices([1, 2, 3], weights=[20, 40, 40])[0]
                else:
                    # Expert: majorité de 3
                    answer_value = random.choices([2, 3], weights=[30, 70])[0]
                
                answers[question_id] = answer_value
            
            # Calculer les scores basés sur les réponses
            # Score pratique = moyenne des réponses * 25 (pour avoir un score 0-100)
            avg_answer = sum(answers.values()) / len(answers) if answers else 0
            practical_score = int(avg_answer * 100 / 3)  # Convertir 0-3 en 0-100
            practical_score = min(100, max(0, practical_score))  # Limiter à 0-100
            
            # Ajuster les autres scores pour qu'ils progressent aussi
            logical_score = base_score['logical'] + random.randint(-5, 5)
            problem_score = base_score['problem'] + random.randint(-5, 5)
            
            # Limiter les scores à 0-100
            logical_score = min(100, max(0, logical_score))
            problem_score = min(100, max(0, problem_score))
            
            # Calculer le niveau précédent (pour le premier test, pas de précédent)
            previous_level = level - 1 if test_num > 0 else 1
            
            # Calculer le taux d'amélioration
            if test_num > 0:
                prev_avg = (base_scores[test_num-1]['practical'] + base_scores[test_num-1]['logical'] + base_scores[test_num-1]['problem']) / 3
                curr_avg = (practical_score + logical_score + problem_score) / 3
                improvement_rate = ((curr_avg - prev_avg) / prev_avg * 100) if prev_avg > 0 else 0
            else:
                improvement_rate = 0
            
            # Temps passé (diminue avec l'expérience)
            time_spent = 45 - (test_num * 5)  # 45 min pour test 1, 25 min pour test 5
            
            # Créer le test result
            test_result = TestResult(
                user_id=user.id,
                filiere='Développement Digital & Systèmes d\'Information',
                predicted_specialization=None,  # Sera défini après
                confidence=None,
                practical_test_score=practical_score,
                logical_reasoning_score=logical_score,
                problem_solving_score=problem_score,
                time_spent_minutes=time_spent,
                previous_level=previous_level,
                current_level=level,
                improvement_rate=round(improvement_rate, 2),
                test_date=test_date
            )
            
            db.add(test_result)
            db.flush()  # Pour obtenir l'ID
            
            # Spécialisation prédite (basée sur les scores)
            # Pour dev, les spécialisations possibles sont liées au développement
            specializations = [
                'Full-Stack Developer',
                'Backend Developer',
                'Frontend Developer',
                'DevOps Engineer',
                'Mobile App Developer'
            ]
            
            # Plus les scores sont élevés, plus on prédit une spécialisation avancée
            if level >= 4:
                predicted_spec = random.choice(['Full-Stack Developer', 'DevOps Engineer'])
            elif level >= 3:
                predicted_spec = random.choice(['Backend Developer', 'Full-Stack Developer'])
            else:
                predicted_spec = random.choice(['Frontend Developer', 'Backend Developer'])
            
            # Mettre à jour le test_result avec la spécialisation prédite
            test_result.predicted_specialization = predicted_spec
            test_result.confidence = 0.75 + (test_num * 0.05)  # Confiance augmente avec la progression
            
            # Créer l'historique de prédiction
            prediction = PredictionHistory(
                user_id=user.id,
                test_result_id=test_result.id,
                predicted_specialization=predicted_spec,
                confidence=0.75 + (test_num * 0.05),  # Confiance augmente avec la progression
                prediction_date=test_date
            )
            
            db.add(prediction)
            
            print(f"\nTest {test_num + 1} cree:")
            print(f"   Date: {test_date.strftime('%Y-%m-%d')}")
            print(f"   Niveau: {level}/5")
            print(f"   Scores: Pratique={practical_score}, Logique={logical_score}, Resolution={problem_score}")
            print(f"   Specialisation predite: {predicted_spec}")
            print(f"   Taux d'amelioration: {improvement_rate:.2f}%")
            print(f"   Temps passe: {time_spent} minutes")
        
        db.commit()
        print(f"\n5 tests crees avec succes pour ibrahim dans la filiere dev!")
        print(f"   Progression visible: Niveau 1 -> 2 -> 2 -> 3 -> 4")
        print(f"   Scores en augmentation constante")
        print(f"   Dates espacees de 15 jours pour voir l'evolution")
        
    except Exception as e:
        db.rollback()
        print(f"Erreur: {e}")
        import traceback
        traceback.print_exc()
    finally:
        db.close()

if __name__ == '__main__':
    print("Creation de 5 tests avec progression pour ibrahim...")
    create_progression_tests()

