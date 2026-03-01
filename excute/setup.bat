@echo off
echo ==========================================
echo Specialization Prediction System - Setup
echo ==========================================

REM Create directories
echo Creating directories...
if not exist dataset mkdir dataset
if not exist models mkdir models
if not exist results mkdir results
if not exist backend mkdir backend
if not exist frontend mkdir frontend

REM Install Python dependencies
echo Installing Python dependencies...
pip install -r requirements.txt

REM Generate dataset and train models
echo Generating dataset and training models...
python run_ml_pipeline.py

echo.
echo Setup completed!
echo.
echo To start the backend:
echo   cd backend ^&^& uvicorn main:app --reload
echo.
echo To start the frontend:
echo   cd frontend ^&^& npm install ^&^& npm start

pause

