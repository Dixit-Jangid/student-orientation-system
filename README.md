# Système d'Orientation Académique (Academic Orientation System)

A robust, full-stack AI-powered system designed to recommend and predict the optimal academic or professional specialization for students based on their skills, test scores, and performance history.

## 🚀 Project Overview

The core of this project relies on a strictly applied **Academic Machine Learning Methodology** to process student data and train classification models. 

This project is divided into three major components:
1. **Machine Learning Pipeline (`academic_ml_pipeline.py`)**: Data ingestion, Exploratory Data Analysis (EDA), Cleaning, Preprocessing, Model Training, and Evaluation.
2. **FastAPI Backend (`/backend`)**: Exposes the trained ML models via RESTful APIs and handles user authentication, data storage, and progression tracking.
3. **React Frontend (`/frontend`)**: A modern, interactive web application where users take tests and view their orientation recommendations.

---

## 🧠 Machine Learning Methodology

The pipeline enforces a strict academic workflow ensuring robustness and reliability at every step:

1. **Dataset Description**: Loading dataset, calculating shape, memory footprint, and column composition.
2. **Exploratory Data Analysis (EDA)**: Descriptive statistics, Missing Values Analysis, Outlier detection (IQR method), Histograms, and Correlation Matrices.
3. **Data Cleaning**: Handling duplicates, missing values (using Mean and KNN imputation techniques), and correcting inconsistent data values.
4. **Data Preprocessing**: Label encoding for categorical data, Train/Test splitting, and feature scaling using `StandardScaler`.
5. **Model Selection & Training**: The pipeline trains multiple classifiers to compare performance:
   - Logistic Regression
   - K-Nearest Neighbors (KNN)
   - Decision Tree
   - Random Forest
   - Support Vector Machines (SVM)
6. **Model Evaluation**: Calculation of Accuracy, Precision, Recall, F1-Score, Cross-Validation (CV), Overfitting analysis, and generation of Confusion Matrices.

---

## 🛠️ Technology Stack

* **Machine Learning**: `scikit-learn`, `pandas`, `numpy`, `xgboost`, `imbalanced-learn`
* **Backend Framework**: `FastAPI`, `Uvicorn`, `Pydantic`
* **Database**: `SQLite` / `SQLAlchemy`
* **Authentication**: `python-jose` (JWT), `passlib` (bcrypt/SHA256)
* **Frontend**: `React.js` (v18), `React Router`, `Recharts`, `Axios`
* **Data Visualization (Backend/ML)**: `matplotlib`, `seaborn`, `plotly`

---

## 🏗️ Project Structure

```text
SYSTÈME D’ORIENTATION/
├── academic_ml_pipeline.py   # Core Academic ML Methodology Pipeline
├── dataset/                  # Contains raw data (e.g., student_tests.csv)
├── models/                   # Saved trained models (.pkl)
├── results/                  # Generated plots (EDA, Evaluation, Cleaning details)
├── backend/                  # FastAPI Application codebase
│   ├── main.py               # API Endpoints
│   ├── auth.py               # Authentication Logic
│   └── database.py           # DB connection and ORM models
├── frontend/                 # React Application codebase
│   ├── public/
│   └── src/                  # React Components & Services
└── requirements.txt          # Python dependencies
```

---

## ⚙️ Setup and Installation

### 1. Backend (FastAPI & Machine Learning)

```bash
# Clone the repository
git clone <repository-url>
cd "SYSTÈME D’ORIENTATION"

# Install Python requirements
pip install -r requirements.txt

# Run the FastAPI server
cd backend
uvicorn main:app --reload
```

*The backend will be available at `http://localhost:8000`. You can explore the API documentation at `http://localhost:8000/docs`.*

### 2. Frontend (React)

Open a new terminal session:

```bash
# Navigate to the frontend directory
cd "SYSTÈME D’ORIENTATION/frontend"

# Install Node.js dependencies
npm install

# Start the React development server
npm start
```

*The frontend will be available at `http://localhost:3000`.*
