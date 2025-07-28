from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class DataSourceCreate(BaseModel):
    name: str
    source_type: str
    source_path: str

class DataSourceResponse(BaseModel):
    id: int
    name: str
    source_type: str
    created_at: datetime
    quality_score: Optional[float] = None

    class Config:
        from_attributes = True

class QualityCheckCreate(BaseModel):
    data_source_id: int
    check_type: str
    check_result: Dict[str, Any]
    status: str
    score: float
    details: Optional[str] = None

class QualityCheckResponse(BaseModel):
    id: int
    check_type: str
    status: str
    score: float
    details: Optional[str] = None
    created_at: datetime

    class Config:
        from_attributes = True

class QualitySummary(BaseModel):
    total_sources: int
    average_quality_score: float
    issues_count: int
    last_check: Optional[datetime] = None 