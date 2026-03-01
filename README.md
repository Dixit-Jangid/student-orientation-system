<div align="center">
  <h1>🎯 Système d'Orientation Académique <br/>(Academic Orientation System)</h1>
  <p><strong>A Full-Stack, AI-Powered Recommendation Engine for Students & Professionals</strong></p>
</div>

<br />

## 📖 What is this project?

The **Academic Orientation System** solves a critical problem in modern education and career development: *navigating the overwhelming number of technical specializations available today.*

Whether a student is studying Computer Science, Digital Development, or Information Systems, it can be extremely difficult to confidently choose the right career path (e.g., *Machine Learning Engineer*, *Cybersecurity Analyst*, *Full-Stack Developer*, or *Data Scientist*). Too often, students rely on intuition rather than empirical data about their own skills.

This project introduces a **data-driven, intelligent recommendation engine**. By putting users through a comprehensive evaluation that measures technical knowledge, practical problem-solving skills, logic, and time management, the system's Machine Learning backend accurately predicts the specialization where the user is most likely to succeed.

But it doesn't stop at predictions: the platform features a baked-in **Recommendation System** that analyzes precisely *why* a user scored a certain way, identifies granular skill gaps (like *Python*, *ML Theory*, or *Data Preprocessing*), and recommends specific learning resources (from Coursera, Kaggle, Codecademy, etc.) to help them improve.

---

## ✨ Key Features & Capabilities

### 🧠 1. Machine Learning Prediction Engine
* **Rigorous Academic Methodology**: The ML pipeline is built on a strict data science methodology, enforcing mandatory steps: *Exploratory Data Analysis (EDA)*, *Data Cleaning (KNN/Mean Imputation)*, *Preprocessing (Standardization/Label Encoding)*, and *Model Evaluation*.
* **Multi-Algorithm Evaluation**: The system automatically trains and compares multiple classifiers (`Logistic Regression`, `KNN`, `Decision Tree`, `Random Forest`, `SVM`) using Cross-Validation, retaining the highest-performing model to serve predictions.
* **Continuous Learning Architecture**: As more students take tests on the frontend, the system is designed to periodically evaluate new data and retrain the models automatically to preserve high accuracy over time.

### 📊 2. Deep Skill Profiling & Recommendations
* **Granular Skill Mapping**: The test doesn't just output a final grade. Every question is mapped to specific competencies (e.g., *Logical Reasoning*, *Ensemble Methods*, *Network Security*).
* **Actionable Feedback**: Using the `RecommendationSystem` module, the backend isolates the exact skills where the user scored poorly (< 2.0/3.0) and generates a personalized curriculum.
* **Progress Tracking**: Users can take tests sequentially over months or years. The database tracks `improvement_rate`, `previous_level`, and `current_level`, allowing students to visualize their growth.

### 🌐 3. Full-Stack Application Ecosystem
* **FastAPI Backend**: A highly performant, asynchronous API layer that serves predictions under milliseconds, handles JWT-based user authentication, and orchestrates database transactions via SQLAlchemy.
* **Interactive React Frontend**: A modern client side built with React 18 and Recharts, providing a smooth user experience from account creation to taking dynamic diagnostic exams to viewing detailed performance dashboards.

---

## 🏗️ Technical Architecture

This application is decoupled into three primary pillars:

```text
├── academic_ml_pipeline.py   # The offline Python pipeline that cleans data and exports .pkl models
├── /backend/                 # The Python REST API
│   ├── main.py               # Application entry point, endpoints & prediction logic
│   ├── auth.py               # Security, password hashing (bcrypt/SHA256) & JWT generation
│   ├── database.py           # SQLite context and SQLAlchemy ORM Models
│   ├── recommendation_system.py # Diagnostic logic linking scores to learning resources
│   └── continuous_learning.py   # Background tasks that retrain models with new data
└── /frontend/                # The React Web Application
    ├── package.json          # Node dependencies (Axios, React Router, Recharts)
    └── /src                  # UI Components, State Management, and API Services
```

### Stack Details
* **Machine Learning**: `scikit-learn`, `pandas`, `numpy`, `xgboost`, `imbalanced-learn`
* **Backend Framework**: `FastAPI`, `Uvicorn`, `Pydantic`
* **Database**: `SQLite` via `SQLAlchemy` ORM
* **Frontend UI**: `React.js` (v18), `React Router v6`, `Recharts` for charting.
* **Data Visualization**: `matplotlib`, `seaborn`, `plotly` (Generated during model training)

---

## 🚀 Setup & Installation Guide

### Prerequisites
* Python 3.9+
* Node.js 16+ & npm

### 1. Backend & ML Server Setup

Open a terminal and map to the project root:

```bash
# Clone the repository
git clone <repository-url>
cd "SYSTÈME D’ORIENTATION"

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows use: venv\Scripts\activate

# Install all Python dependencies
pip install -r requirements.txt

# Run the FastAPI server
cd backend
uvicorn main:app --reload
```
> The backend server will be live at `http://localhost:8000`. 
> You can visit the interactive API documentation at `http://localhost:8000/docs`.

### 2. Frontend React Application Setup

Open a new, separate terminal window:

```bash
# Navigate to the frontend directory
cd "SYSTÈME D’ORIENTATION/frontend"

# Install Node modules
npm install

# Start the React development server
npm start
```
> The React application will spin up at `http://localhost:3000`.

---

## 🔐 Security & Version Control
This repository is pre-configured with a comprehensive `.gitignore` ensuring that your SQLite databases (`*.db`, `*.sqlite`), trained binary models (`*.pkl`), sensitive `.env` files, and `node_modules/` are strictly excluded from source control, keeping your environment secure right out of the box.

---

<div align="center">
  <i>Developed to bridge the gap between academic theory and practical, intelligence-assisted career guidance.</i>
</div>
