from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import datetime, timedelta

from app.core.database import get_db
from app.models.alerts import Alert
from app.services.alert_service import AlertService
from app.schemas.alerts import AlertCreate, AlertResponse, AlertUpdate

router = APIRouter()
alert_service = AlertService()

@router.get("/", response_model=List[AlertResponse])
async def get_alerts(
    severity: Optional[str] = None,
    alert_type: Optional[str] = None,
    is_resolved: Optional[bool] = None,
    limit: int = 50,
    db: Session = Depends(get_db)
):
    """Get all alerts with optional filtering"""
    query = db.query(Alert)
    
    if severity:
        query = query.filter(Alert.severity == severity)
    if alert_type:
        query = query.filter(Alert.alert_type == alert_type)
    if is_resolved is not None:
        query = query.filter(Alert.is_resolved == is_resolved)
    
    alerts = query.order_by(Alert.created_at.desc()).limit(limit).all()
    
    return [
        AlertResponse(
            id=alert.id,
            alert_type=alert.alert_type,
            severity=alert.severity,
            title=alert.title,
            message=alert.message,
            source=alert.source,
            is_resolved=alert.is_resolved,
            created_at=alert.created_at
        ) for alert in alerts
    ]

@router.post("/", response_model=AlertResponse)
async def create_alert(
    alert_data: AlertCreate,
    db: Session = Depends(get_db)
):
    """Create a new alert"""
    alert = Alert(
        alert_type=alert_data.alert_type,
        severity=alert_data.severity,
        title=alert_data.title,
        message=alert_data.message,
        source=alert_data.source,
        metadata=alert_data.metadata
    )
    
    db.add(alert)
    db.commit()
    db.refresh(alert)
    
    # Send notification
    try:
        alert_service.send_notification(alert)
    except Exception as e:
        # Log error but don't fail the request
        print(f"Error sending notification: {e}")
    
    return AlertResponse(
        id=alert.id,
        alert_type=alert.alert_type,
        severity=alert.severity,
        title=alert.title,
        message=alert.message,
        source=alert.source,
        is_resolved=alert.is_resolved,
        created_at=alert.created_at
    )

@router.put("/{alert_id}/resolve", response_model=AlertResponse)
async def resolve_alert(
    alert_id: int,
    resolved_by: str = "system",
    db: Session = Depends(get_db)
):
    """Resolve an alert"""
    alert = db.query(Alert).filter(Alert.id == alert_id).first()
    if not alert:
        raise HTTPException(status_code=404, detail="Alert not found")
    
    alert.is_resolved = True
    alert.resolved_at = datetime.now()
    alert.resolved_by = resolved_by
    
    db.commit()
    db.refresh(alert)
    
    return AlertResponse(
        id=alert.id,
        alert_type=alert.alert_type,
        severity=alert.severity,
        title=alert.title,
        message=alert.message,
        source=alert.source,
        is_resolved=alert.is_resolved,
        created_at=alert.created_at
    )

@router.get("/summary")
async def get_alert_summary(db: Session = Depends(get_db)):
    """Get alert summary statistics"""
    total_alerts = db.query(Alert).count()
    unresolved_alerts = db.query(Alert).filter(Alert.is_resolved == False).count()
    
    # Get alerts by severity
    critical_alerts = db.query(Alert).filter(
        Alert.severity == "critical",
        Alert.is_resolved == False
    ).count()
    
    high_alerts = db.query(Alert).filter(
        Alert.severity == "high",
        Alert.is_resolved == False
    ).count()
    
    # Get recent alerts (last 24 hours)
    yesterday = datetime.now() - timedelta(days=1)
    recent_alerts = db.query(Alert).filter(Alert.created_at >= yesterday).count()
    
    return {
        "total_alerts": total_alerts,
        "unresolved_alerts": unresolved_alerts,
        "critical_alerts": critical_alerts,
        "high_alerts": high_alerts,
        "recent_alerts_24h": recent_alerts
    }

@router.post("/test")
async def test_alert_system(db: Session = Depends(get_db)):
    """Test the alert system by creating a sample alert"""
    test_alert = Alert(
        alert_type="system",
        severity="medium",
        title="Test Alert",
        message="This is a test alert to verify the alerting system is working correctly.",
        source="test_system",
        metadata={"test": True}
    )
    
    db.add(test_alert)
    db.commit()
    db.refresh(test_alert)
    
    # Send test notification
    try:
        alert_service.send_notification(test_alert)
        notification_sent = True
    except Exception as e:
        notification_sent = False
        print(f"Error sending test notification: {e}")
    
    return {
        "message": "Test alert created successfully",
        "alert_id": test_alert.id,
        "notification_sent": notification_sent
    } 