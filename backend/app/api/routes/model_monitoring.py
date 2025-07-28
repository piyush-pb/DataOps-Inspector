from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
import json
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.model_monitoring import ModelPerformance, ModelDrift
from app.services.model_monitoring_service import ModelMonitoringService
from app.schemas.model_monitoring import (
    ModelPerformanceCreate, ModelPerformanceResponse,
    ModelDriftResponse, ModelSummary
)

router = APIRouter()
model_service = ModelMonitoringService()

@router.post("/deploy", response_model=dict)
async def deploy_model(
    model_name: str,
    model_type: str = "classification",
    db: Session = Depends(get_db)
):
    """Deploy a sample ML model"""
    try:
        # Deploy sample model
        model_info = model_service.deploy_sample_model(model_name, model_type)
        
        return {
            "message": "Model deployed successfully",
            "model_name": model_name,
            "model_type": model_type,
            "version": model_info["version"],
            "status": "active"
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deploying model: {str(e)}")

@router.get("/models", response_model=List[str])
async def get_deployed_models(db: Session = Depends(get_db)):
    """Get list of deployed models"""
    try:
        models = model_service.get_deployed_models()
        return models
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error getting models: {str(e)}")

@router.post("/models/{model_name}/predict", response_model=dict)
async def make_prediction(
    model_name: str,
    features: dict,
    db: Session = Depends(get_db)
):
    """Make a prediction using the deployed model"""
    try:
        prediction = model_service.make_prediction(model_name, features)
        
        # Record performance metrics
        performance = ModelPerformance(
            model_name=model_name,
            model_version="1.0",
            metric_name="prediction",
            metric_value=prediction["confidence"],
            sample_size=1,
            metadata={"features": features, "prediction": prediction["prediction"]}
        )
        db.add(performance)
        db.commit()
        
        return prediction
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error making prediction: {str(e)}")

@router.get("/models/{model_name}/performance", response_model=List[ModelPerformanceResponse])
async def get_model_performance(
    model_name: str,
    metric: Optional[str] = None,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get model performance metrics"""
    query = db.query(ModelPerformance).filter(ModelPerformance.model_name == model_name)
    
    if metric:
        query = query.filter(ModelPerformance.metric_name == metric)
    
    # Filter by date range
    start_date = datetime.now() - timedelta(days=days)
    query = query.filter(ModelPerformance.timestamp >= start_date)
    
    performances = query.order_by(ModelPerformance.timestamp.desc()).all()
    
    return [
        ModelPerformanceResponse(
            id=perf.id,
            model_name=perf.model_name,
            model_version=perf.model_version,
            metric_name=perf.metric_name,
            metric_value=perf.metric_value,
            sample_size=perf.sample_size,
            timestamp=perf.timestamp
        ) for perf in performances
    ]

@router.post("/models/{model_name}/drift-check", response_model=List[ModelDriftResponse])
async def check_model_drift(
    model_name: str,
    db: Session = Depends(get_db)
):
    """Check for model drift"""
    try:
        drift_results = model_service.check_model_drift(model_name)
        
        # Save drift results
        drift_records = []
        for result in drift_results:
            drift_record = ModelDrift(
                model_name=model_name,
                model_version="1.0",
                drift_type=result["drift_type"],
                drift_score=result["drift_score"],
                threshold=result["threshold"],
                is_drift_detected=result["is_drift_detected"],
                feature_name=result.get("feature_name"),
                details=result["details"]
            )
            db.add(drift_record)
            drift_records.append(drift_record)
        
        db.commit()
        
        return [
            ModelDriftResponse(
                id=drift.id,
                model_name=drift.model_name,
                model_version=drift.model_version,
                drift_type=drift.drift_type,
                drift_score=drift.drift_score,
                threshold=drift.threshold,
                is_drift_detected=drift.is_drift_detected,
                feature_name=drift.feature_name,
                timestamp=drift.timestamp
            ) for drift in drift_records
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error checking drift: {str(e)}")

@router.get("/models/{model_name}/drift", response_model=List[ModelDriftResponse])
async def get_model_drift_history(
    model_name: str,
    days: int = 30,
    db: Session = Depends(get_db)
):
    """Get model drift history"""
    start_date = datetime.now() - timedelta(days=days)
    
    drift_records = db.query(ModelDrift)\
        .filter(ModelDrift.model_name == model_name)\
        .filter(ModelDrift.timestamp >= start_date)\
        .order_by(ModelDrift.timestamp.desc())\
        .all()
    
    return [
        ModelDriftResponse(
            id=drift.id,
            model_name=drift.model_name,
            model_version=drift.model_version,
            drift_type=drift.drift_type,
            drift_score=drift.drift_score,
            threshold=drift.threshold,
            is_drift_detected=drift.is_drift_detected,
            feature_name=drift.feature_name,
            timestamp=drift.timestamp
        ) for drift in drift_records
    ]

@router.get("/summary", response_model=ModelSummary)
async def get_model_summary(db: Session = Depends(get_db)):
    """Get overall model monitoring summary"""
    # Get recent performance metrics
    recent_performance = db.query(ModelPerformance)\
        .order_by(ModelPerformance.timestamp.desc())\
        .limit(100)\
        .all()
    
    # Get recent drift checks
    recent_drift = db.query(ModelDrift)\
        .order_by(ModelDrift.timestamp.desc())\
        .limit(50)\
        .all()
    
    # Calculate summary metrics
    total_models = len(set(p.model_name for p in recent_performance))
    
    if recent_performance:
        avg_accuracy = sum(p.metric_value for p in recent_performance if p.metric_name == "accuracy") / max(1, len([p for p in recent_performance if p.metric_name == "accuracy"]))
    else:
        avg_accuracy = 0
    
    drift_alerts = sum(1 for d in recent_drift if d.is_drift_detected)
    
    return ModelSummary(
        total_models=total_models,
        average_accuracy=round(avg_accuracy, 3),
        drift_alerts=drift_alerts,
        last_check=recent_drift[0].timestamp if recent_drift else None
    ) 