"""
Dashboard API endpoints for ML monitoring
Loads and serves ML pipeline results for admin dashboard
"""

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from database import get_db, User, TestResult, PredictionHistory
from auth import get_current_user
import pandas as pd
import numpy as np
import joblib
import os
import json
from fastapi.responses import FileResponse

router = APIRouter(prefix="/api/dashboard/ml", tags=["dashboard-ml"])

def load_ml_results():
    """Load ML pipeline results from files"""
    results = {
        'eda_available': False,
        'cleaning_available': False,
        'evaluation_available': False,
        'model_available': False
    }
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    
    # Check EDA results
    eda_dir = os.path.join(base_dir, 'results', 'eda')
    if os.path.exists(eda_dir):
        results['eda_available'] = True
        results['eda_dir'] = eda_dir
    
    # Check cleaning results
    cleaning_dir = os.path.join(base_dir, 'results', 'cleaning')
    if os.path.exists(cleaning_dir):
        results['cleaning_available'] = True
        cleaning_summary_path = os.path.join(cleaning_dir, 'cleaning_summary.csv')
        if os.path.exists(cleaning_summary_path):
            try:
                results['cleaning_summary'] = pd.read_csv(cleaning_summary_path).to_dict('records')
            except:
                pass
    
    # Check evaluation results
    eval_dir = os.path.join(base_dir, 'results', 'evaluation')
    if os.path.exists(eval_dir):
        results['evaluation_available'] = True
        model_comparison_path = os.path.join(eval_dir, 'model_comparison.csv')
        if os.path.exists(model_comparison_path):
            try:
                results['model_comparison'] = pd.read_csv(model_comparison_path).to_dict('records')
            except:
                pass
    
    # Load model - PRIORITY: notebook output, else old path
    model_paths = [
        os.path.join(base_dir, 'reports', 'model', 'best_model.pkl'),  # Notebook output (priority)
        os.path.join(base_dir, 'models', 'best_model.pkl')             # Old path (fallback)
    ]
    for model_path in model_paths:
        if os.path.exists(model_path):
            try:
                model_data = joblib.load(model_path)
                results['model_available'] = True
                results['model_data'] = model_data
                results['model_path'] = model_path
                break
            except:
                continue
    
    # Load preprocessing info
    preprocessing_path = os.path.join(base_dir, 'models', 'preprocessing_info.json')
    if os.path.exists(preprocessing_path):
        try:
            with open(preprocessing_path, 'r') as f:
                results['preprocessing_info'] = json.load(f)
        except:
            pass
    
    return results

@router.get("/pipeline-results")
async def get_ml_pipeline_results(
    current_user: User = Depends(get_current_user)
):
    """Get ML pipeline results for admin dashboard"""
    is_admin = getattr(current_user, 'role', 'user') == 'admin'
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    
    return load_ml_results()

@router.get("/eda-results")
async def get_eda_results(
    current_user: User = Depends(get_current_user)
):
    """Get EDA results"""
    is_admin = getattr(current_user, 'role', 'user') == 'admin'
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    eda_dir = os.path.join(base_dir, 'results', 'eda')
    
    results = {}
    
    # Load descriptive statistics
    desc_stats_path = os.path.join(eda_dir, 'descriptive_statistics.csv')
    if os.path.exists(desc_stats_path):
        try:
            results['descriptive_stats'] = pd.read_csv(desc_stats_path).to_dict('records')
        except:
            pass
    
    # Load missing values analysis
    missing_path = os.path.join(eda_dir, 'missing_values_analysis.csv')
    if os.path.exists(missing_path):
        try:
            results['missing_analysis'] = pd.read_csv(missing_path).to_dict('records')
        except:
            pass
    
    # Load outlier detection
    outlier_path = os.path.join(eda_dir, 'outlier_detection_iqr.csv')
    if os.path.exists(outlier_path):
        try:
            results['outlier_detection'] = pd.read_csv(outlier_path).to_dict('records')
        except:
            pass
    
    # Load target distribution
    target_path = os.path.join(eda_dir, 'target_distribution.csv')
    if os.path.exists(target_path):
        try:
            target_df = pd.read_csv(target_path)
            results['target_distribution'] = target_df.to_dict('records')
        except:
            pass
    
    return results

@router.get("/cleaning-results")
async def get_cleaning_results(
    current_user: User = Depends(get_current_user)
):
    """Get data cleaning results"""
    is_admin = getattr(current_user, 'role', 'user') == 'admin'
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    cleaning_dir = os.path.join(base_dir, 'results', 'cleaning')
    
    results = {}
    
    # Load cleaning summary
    cleaning_summary_path = os.path.join(cleaning_dir, 'cleaning_summary.csv')
    if os.path.exists(cleaning_summary_path):
        try:
            results['cleaning_summary'] = pd.read_csv(cleaning_summary_path).to_dict('records')
        except:
            pass
    
    return results

@router.get("/evaluation-results")
async def get_evaluation_results(
    current_user: User = Depends(get_current_user)
):
    """Get model evaluation results"""
    is_admin = getattr(current_user, 'role', 'user') == 'admin'
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    eval_dir = os.path.join(base_dir, 'results', 'evaluation')
    
    results = {}
    
    # Load model comparison
    model_comp_path = os.path.join(eval_dir, 'model_comparison.csv')
    if os.path.exists(model_comp_path):
        try:
            results['model_comparison'] = pd.read_csv(model_comp_path).to_dict('records')
        except:
            pass
    
    # Load classification report
    report_path = os.path.join(eval_dir, 'classification_report_best_model.csv')
    if os.path.exists(report_path):
        try:
            results['classification_report'] = pd.read_csv(report_path).to_dict('records')
        except:
            pass
    
    return results

@router.get("/summary")
async def get_reports_summary(
    current_user: User = Depends(get_current_user)
):
    """
    Return notebook-driven report artifacts from /reports
    Includes: metrics.json, kpi.json, clean_vs_raw.json, figures list
    """
    is_admin = getattr(current_user, 'role', 'user') == 'admin'
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    
    base_dir = os.path.dirname(os.path.dirname(__file__))
    reports_dir = os.path.join(base_dir, 'reports')
    figs_dir = os.path.join(reports_dir, 'figures')
    data_dir = os.path.join(reports_dir, 'data')
    model_dir = os.path.join(reports_dir, 'model')
    
    summary = {
        "exists": os.path.exists(reports_dir),
        "metrics": {},
        "kpi": {},
        "clean_vs_raw": {},
        "figures": [],
        "data_files": [],
        "model_files": []
    }
    
    try:
        metrics_path = os.path.join(reports_dir, 'metrics.json')
        if os.path.exists(metrics_path):
            with open(metrics_path, 'r', encoding='utf-8') as f:
                summary["metrics"] = json.load(f)
    except:
        pass
    
    try:
        kpi_path = os.path.join(reports_dir, 'kpi.json')
        if os.path.exists(kpi_path):
            with open(kpi_path, 'r', encoding='utf-8') as f:
                summary["kpi"] = json.load(f)
    except:
        pass
    
    try:
        cvr_path = os.path.join(reports_dir, 'clean_vs_raw.json')
        if os.path.exists(cvr_path):
            with open(cvr_path, 'r', encoding='utf-8') as f:
                summary["clean_vs_raw"] = json.load(f)
    except:
        pass
    
    # List figures and data/model artifacts
    if os.path.exists(figs_dir):
        try:
            summary["figures"] = [
                os.path.join('reports', 'figures', f) for f in os.listdir(figs_dir)
                if os.path.isfile(os.path.join(figs_dir, f))
            ]
        except:
            pass
    if os.path.exists(data_dir):
        try:
            summary["data_files"] = [
                os.path.join('reports', 'data', f) for f in os.listdir(data_dir)
                if os.path.isfile(os.path.join(data_dir, f))
            ]
        except:
            pass
    if os.path.exists(model_dir):
        try:
            summary["model_files"] = [
                os.path.join('reports', 'model', f) for f in os.listdir(model_dir)
                if os.path.isfile(os.path.join(model_dir, f))
            ]
        except:
            pass
    
    return summary

@router.get("/list-reports")
async def list_report_files(
    current_user: User = Depends(get_current_user)
):
    """List all files under /reports for download links in UI"""
    is_admin = getattr(current_user, 'role', 'user') == 'admin'
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    base_dir = os.path.dirname(os.path.dirname(__file__))
    reports_dir = os.path.join(base_dir, 'reports')
    all_files = []
    for root, _, files in os.walk(reports_dir):
        for f in files:
            full = os.path.join(root, f)
            rel = os.path.relpath(full, base_dir).replace("\\", "/")
            all_files.append(rel)
    return {"files": all_files}

@router.get("/download")
async def download_report(path: str, current_user: User = Depends(get_current_user)):
    """Serve a file under project root securely (only within /reports)"""
    is_admin = getattr(current_user, 'role', 'user') == 'admin'
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    base_dir = os.path.dirname(os.path.dirname(__file__))
    abs_path = os.path.abspath(os.path.join(base_dir, path))
    reports_dir = os.path.abspath(os.path.join(base_dir, 'reports'))
    if not abs_path.startswith(reports_dir):
        raise HTTPException(status_code=400, detail="Invalid path")
    if not os.path.exists(abs_path):
        raise HTTPException(status_code=404, detail="File not found")
    return FileResponse(abs_path, filename=os.path.basename(abs_path))

@router.post("/retrain")
async def trigger_retraining(current_user: User = Depends(get_current_user)):
    """Trigger retraining in background using academic pipeline outputs"""
    is_admin = getattr(current_user, 'role', 'user') == 'admin'
    if not is_admin:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Access denied. Admin privileges required."
        )
    # Run pipeline in a background thread to avoid blocking
    import threading
    def _run():
        try:
            from academic_ml_pipeline import AcademicMLPipeline
            p = AcademicMLPipeline(data_path='dataset/student_tests.csv')
            p.run_complete_pipeline()
        except Exception as e:
            print("[RETRAIN] Error:", e)
    t = threading.Thread(target=_run, daemon=True)
    t.start()
    return {"status": "started"}
