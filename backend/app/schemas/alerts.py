from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime

class AlertCreate(BaseModel):
    alert_type: str
    severity: str
    title: str
    message: str
    source: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None

class AlertResponse(BaseModel):
    id: int
    alert_type: str
    severity: str
    title: str
    message: str
    source: Optional[str] = None
    is_resolved: bool
    created_at: datetime

    class Config:
        from_attributes = True

class AlertUpdate(BaseModel):
    is_resolved: Optional[bool] = None
    resolved_by: Optional[str] = None 