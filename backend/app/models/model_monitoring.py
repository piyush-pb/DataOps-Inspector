from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class ModelPerformance(Base):
    __tablename__ = "model_performance"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(255), nullable=False)
    model_version = Column(String(50), nullable=False)
    metric_name = Column(String(100), nullable=False)  # accuracy, f1_score, precision, recall
    metric_value = Column(Float, nullable=False)
    sample_size = Column(Integer)
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    metadata = Column(JSON)  # Additional model metadata
    
    def __repr__(self):
        return f"<ModelPerformance(id={self.id}, model='{self.model_name}', metric='{self.metric_name}')>"

class ModelDrift(Base):
    __tablename__ = "model_drift"
    
    id = Column(Integer, primary_key=True, index=True)
    model_name = Column(String(255), nullable=False)
    model_version = Column(String(50), nullable=False)
    drift_type = Column(String(100), nullable=False)  # feature_drift, prediction_drift, data_drift
    drift_score = Column(Float, nullable=False)  # Drift detection score
    threshold = Column(Float, nullable=False)  # Threshold for drift detection
    is_drift_detected = Column(Boolean, nullable=False)
    feature_name = Column(String(255))  # For feature-specific drift
    details = Column(JSON)  # Detailed drift information
    timestamp = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<ModelDrift(id={self.id}, model='{self.model_name}', type='{self.drift_type}')>" 