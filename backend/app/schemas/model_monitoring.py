from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class ModelPerformanceCreate(BaseModel):
    model_name: str
    model_version: str
    metric_name: str
    metric_value: float
    sample_size: Optional[int] = None
    metadata: Optional[Dict[str, Any]] = None

class ModelPerformanceResponse(BaseModel):
    id: int
    model_name: str
    model_version: str
    metric_name: str
    metric_value: float
    sample_size: Optional[int] = None
    timestamp: datetime

    class Config:
        from_attributes = True

class ModelDriftResponse(BaseModel):
    id: int
    model_name: str
    model_version: str
    drift_type: str
    drift_score: float
    threshold: float
    is_drift_detected: bool
    feature_name: Optional[str] = None
    timestamp: datetime

    class Config:
        from_attributes = True

class ModelSummary(BaseModel):
    total_models: int
    average_accuracy: float
    drift_alerts: int
    last_check: Optional[datetime] = None

class PredictionRequest(BaseModel):
    features: Dict[str, Any]

class PredictionResponse(BaseModel):
    prediction: Any
    confidence: float
    model_name: str
    model_version: str 