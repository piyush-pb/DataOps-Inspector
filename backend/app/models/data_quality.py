from sqlalchemy import Column, Integer, String, DateTime, Float, Text, Boolean, JSON
from sqlalchemy.sql import func
from app.core.database import Base

class DataSource(Base):
    __tablename__ = "data_sources"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    source_type = Column(String(50), nullable=False)  # csv, api, database
    source_path = Column(String(500), nullable=False)
    schema = Column(JSON)  # Store column definitions
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())
    is_active = Column(Boolean, default=True)
    
    def __repr__(self):
        return f"<DataSource(id={self.id}, name='{self.name}', type='{self.source_type}')>"

class DataQualityCheck(Base):
    __tablename__ = "data_quality_checks"
    
    id = Column(Integer, primary_key=True, index=True)
    data_source_id = Column(Integer, nullable=False)
    check_type = Column(String(100), nullable=False)  # missing_values, duplicates, schema_drift, etc.
    check_result = Column(JSON, nullable=False)  # Store detailed results
    status = Column(String(20), nullable=False)  # passed, failed, warning
    score = Column(Float)  # Quality score 0-1
    details = Column(Text)  # Additional details
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    def __repr__(self):
        return f"<DataQualityCheck(id={self.id}, type='{self.check_type}', status='{self.status}')>" 