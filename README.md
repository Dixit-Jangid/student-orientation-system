<div align="center">
  <h1>🎯 Système d'Orientation Académique <br/>(Academic Orientation System)</h1>
  <p><strong>A Full-Stack, AI-Powered Recommendation Engine for Students & Professionals</strong></p>
</div>

<br />

## 🤝 Project Vision (Client Overview)

Welcome to the **Academic Orientation System**, a next-generation career and academic guidance platform. 

Imagine you are a student or a young professional facing the vast landscape of tech specializations—Should you be a Data Scientist? A Cybersecurity Analyst? A Full-Stack Developer? Making the wrong choice can cost years of frustration. 

Our system removes the guesswork. We provide a **data-driven ecosystem** that evaluates a user's technical knowledge, logical reasoning, and practical problem-solving skills through dynamic assessments. Behind the scenes, our advanced **Machine Learning Engine**, trained on rigorous academic methodologies, processes these scores to predict the exact career path where the user will thrive. 

More than just a prediction, the platform acts as a personal mentor. It pinpoints your exact skill gaps—down to topics like "Data Preprocessing" or "Model Evaluation"—and provides highly curated learning resources tailored to help you level up your career.

---

## 🌟 Advantages of the System

* **100% Data-Driven Confidence**: Replaces intuition with statistical models, giving students empirical proof of their strengths.
* **Granular Competency Tracking**: Doesn't just give a pass/fail grade. We map every single test question to specific industry skills.
* **Actionable Learning Paths**: Users don't just see what they did wrong; they are handed the exact courses (e.g., Coursera, Kaggle) to fix their weaknesses.
* **Continuous Improvement Tracking**: The system tracks user performance over time, visualizing their trajectory and improvement rates across multiple attempts.
* **Auto-Adaptive AI**: The backend is built with continuous learning in mind. As more students take tests, the model can be retrained on fresh data to remain highly accurate to modern standards.

---

## 💡 The Solutions We Provide

1. **Intelligent Diagnostics**: A comprehensive testing module that goes beyond multiple-choice to evaluate practical problem-solving and logic.
2. **Personalized Recommendations Algorithm**: Matches weak skills (scoring < 2.0) directly with industry-standard educational resources.
3. **Admin Telemetry & Dashboards**: Allows platform operators to monitor overall accuracy, see user distributions across specializations, and ensure the neural logic holds up in production.

---

## 📱 Platform Pages (Frontend Architecture)

Our React-based frontend is built with user experience in mind, offering a seamless journey across the following pages:

* **`/login` & `/register`**: Secure authentication portals via JWT.
* **`/select-filiere`**: The onboarding page where users declare their broad academic field before being drilled down.
* **`/test`**: The core diagnostic exam environment where the timer, scoring, and questions are processed.
* **`/results/:testId`**: An immediate, visually rich dashboard displaying the ML Prediction (e.g., "Machine Learning Engineer - 98% Confidence") along with granular skill feedback.
* **`/dashboard`**: The centralized portal for general users to begin new tests and view rapid summaries.
* **`/history`**: A ledger of all past exams taken by the user.
* **`/progress`**: A charting page (via Recharts) that visualizes the user's growth, `improvement_rate`, and skill trajectory over time.
* **`/admin`**: The master control and analytics dashboard restricted to operators.

---

## 👥 User Roles & Permissions

The platform employs Role-Based Access Control (RBAC) to ensure security and privacy:

* **Standard User (`"user"`)**
  * Can take diagnostic exams.
  * Has access to their personal test history, progress tracking, and personalized learning recommendations.
* **Administrator (`"admin"`)**
  * Cannot take tests.
  * Owns the `/admin` portal to view global telemetry, overall model confidence metrics, and user distribution data to ensure the ML pipeline is serving the business smoothly.

---
*(Technical Implementation Details Below)*
---

## 🧠 Machine Learning Methodology

The pipeline enforces a strict academic workflow ensuring robustness and reliability at every step:

1. **Dataset Description**: Loading dataset, calculating shape, memory footprint, and column composition.
2. **Exploratory Data Analysis (EDA)**: Descriptive statistics, Missing Values Analysis, Outlier detection (IQR method), Histograms, and Correlation Matrices.
3. **Data Cleaning**: Handling duplicates, missing values (using Mean and KNN imputation techniques), and correcting inconsistent data values.
4. **Data Preprocessing**: Label encoding for categorical data, Train/Test splitting, and feature scaling using `StandardScaler`.
5. **Model Selection & Training**: The pipeline trains multiple classifiers to compare performance:
   - Logistic Regression | K-Nearest Neighbors (KNN) | Decision Tree | Random Forest | Support Vector Machines (SVM)
6. **Model Evaluation**: Calculation of Accuracy, Precision, Recall, F1-Score, Cross-Validation (CV), Overfitting analysis, and generation of Confusion Matrices.

---

## 🛠️ Technology Stack

* **Machine Learning**: `scikit-learn`, `pandas`, `numpy`, `xgboost`, `imbalanced-learn`
* **Backend Framework**: `FastAPI`, `Uvicorn`, `Pydantic`
* **Database**: `SQLite` / `SQLAlchemy` ORM
* **Authentication**: `python-jose` (JWT), `passlib` (bcrypt/SHA256)
* **Frontend**: `React.js` (v18), `React Router v6`, `Recharts`, `Axios`
* **Data Visualization**: `matplotlib`, `seaborn`, `plotly`

---

## ⚙️ Setup and Installation

### 1. Backend (FastAPI & Machine Learning)

```bash
# Clone the repository
git clone <repository-url>
cd "SYSTÈME D’ORIENTATION"

# Create a virtual environment (optional but recommended)
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the FastAPI server
cd backend
uvicorn main:app --reload
```
*The backend API will run on `http://localhost:8000` (Docs: `http://localhost:8000/docs`).*

### 2. Frontend (React)

Open a new terminal session:

```bash
# Navigate to the frontend directory
cd "SYSTÈME D’ORIENTATION/frontend"

# Install Node modules
npm install

# Start the React development server
npm start
```
*The frontend will run on `http://localhost:3000`.*
