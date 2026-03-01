#!/bin/bash

echo "=========================================="
echo "Specialization Prediction System - Setup"
echo "=========================================="

# Create directories
echo "Creating directories..."
mkdir -p dataset models results backend frontend

# Install Python dependencies
echo "Installing Python dependencies..."
pip install -r requirements.txt

# Generate dataset and train models
echo "Generating dataset and training models..."
python run_ml_pipeline.py

echo ""
echo "Setup completed!"
echo ""
echo "To start the backend:"
echo "  cd backend && uvicorn main:app --reload"
echo ""
echo "To start the frontend:"
echo "  cd frontend && npm install && npm start"

