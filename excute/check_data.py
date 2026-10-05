"""Quick script to check database statistics"""
import sqlite3
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, "specialization_prediction.db")

conn = sqlite3.connect(DATABASE_PATH)
cursor = conn.cursor()

cursor.execute("SELECT COUNT(*) FROM users WHERE role='user'")
users = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM test_results")
tests = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT filiere) FROM test_results")
filieres = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(DISTINCT predicted_specialization) FROM test_results")
specs = cursor.fetchone()[0]

cursor.execute("SELECT filiere, COUNT(*) as count FROM test_results GROUP BY filiere")
filiere_dist = cursor.fetchall()

cursor.execute("SELECT predicted_specialization, COUNT(*) as count FROM test_results GROUP BY predicted_specialization ORDER BY count DESC LIMIT 10")
top_specs = cursor.fetchall()

print(f"\n{'='*60}")
print("STATISTIQUES DE LA BASE DE DONNEES")
print(f"{'='*60}\n")
print(f"Total utilisateurs: {users}")
print(f"Total tests: {tests}")
print(f"Filieres: {filieres}")
print(f"Specialisations: {specs}\n")

print("Distribution par filiere:")
for filiere, count in filiere_dist:
    print(f"  - {filiere}: {count} tests")

print(f"\nTop 10 specialisations:")
for spec, count in top_specs:
    print(f"  - {spec}: {count} tests")

conn.close()

