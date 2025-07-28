from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from datetime import datetime, timedelta
from typing import Dict, Any

from app.core.database import get_db
from app.models.data_quality import DataSource, DataQualityCheck
from app.models.model_monitoring import ModelPerformance, ModelDrift
from app.models.alerts import Alert

router = APIRouter()

@router.get("/overview")
async def get_dashboard_overview(db: Session = Depends(get_db)):
    """Get comprehensive dashboard overview"""
    
    # Data Quality Summary
    total_sources = db.query(DataSource).filter(DataSource.is_active == True).count()
    recent_quality_checks = db.query(DataQualityCheck)\
        .order_by(DataQualityCheck.created_at.desc())\
        .limit(100)\
        .all()
    
    avg_quality_score = 0
    if recent_quality_checks:
        avg_quality_score = sum(check.score for check in recent_quality_checks) / len(recent_quality_checks)
    
    # Model Monitoring Summary
    recent_performance = db.query(ModelPerformance)\
        .order_by(ModelPerformance.timestamp.desc())\
        .limit(100)\
        .all()
    
    total_models = len(set(p.model_name for p in recent_performance))
    avg_accuracy = 0
    if recent_performance:
        accuracy_metrics = [p.metric_value for p in recent_performance if p.metric_name == "accuracy"]
        if accuracy_metrics:
            avg_accuracy = sum(accuracy_metrics) / len(accuracy_metrics)
    
    # Drift Summary
    recent_drift = db.query(ModelDrift)\
        .order_by(ModelDrift.timestamp.desc())\
        .limit(50)\
        .all()
    
    drift_alerts = sum(1 for d in recent_drift if d.is_drift_detected)
    
    # Alert Summary
    total_alerts = db.query(Alert).count()
    unresolved_alerts = db.query(Alert).filter(Alert.is_resolved == False).count()
    critical_alerts = db.query(Alert).filter(
        Alert.severity == "critical",
        Alert.is_resolved == False
    ).count()
    
    return {
        "data_quality": {
            "total_sources": total_sources,
            "average_quality_score": round(avg_quality_score, 3),
            "recent_checks": len(recent_quality_checks)
        },
        "model_monitoring": {
            "total_models": total_models,
            "average_accuracy": round(avg_accuracy, 3),
            "drift_alerts": drift_alerts
        },
        "alerts": {
            "total_alerts": total_alerts,
            "unresolved_alerts": unresolved_alerts,
            "critical_alerts": critical_alerts
        },
        "system_health": {
            "overall_status": "healthy" if critical_alerts == 0 else "warning",
            "last_updated": datetime.now()
        }
    }

@router.get("/trends")
async def get_dashboard_trends(db: Session = Depends(get_db)):
    """Get trend data for dashboard charts"""
    
    # Get data for last 30 days
    start_date = datetime.now() - timedelta(days=30)
    
    # Data Quality Trends
    quality_trends = db.query(DataQualityCheck)\
        .filter(DataQualityCheck.created_at >= start_date)\
        .order_by(DataQualityCheck.created_at)\
        .all()
    
    # Group by date
    quality_by_date = {}
    for check in quality_trends:
        date_str = check.created_at.strftime("%Y-%m-%d")
        if date_str not in quality_by_date:
            quality_by_date[date_str] = []
        quality_by_date[date_str].append(check.score)
    
    # Calculate daily averages
    quality_trend_data = [
        {
            "date": date,
            "average_score": sum(scores) / len(scores)
        }
        for date, scores in quality_by_date.items()
    ]
    
    # Model Performance Trends
    performance_trends = db.query(ModelPerformance)\
        .filter(ModelPerformance.timestamp >= start_date)\
        .filter(ModelPerformance.metric_name == "accuracy")\
        .order_by(ModelPerformance.timestamp)\
        .all()
    
    performance_by_date = {}
    for perf in performance_trends:
        date_str = perf.timestamp.strftime("%Y-%m-%d")
        if date_str not in performance_by_date:
            performance_by_date[date_str] = []
        performance_by_date[date_str].append(perf.metric_value)
    
    performance_trend_data = [
        {
            "date": date,
            "average_accuracy": sum(values) / len(values)
        }
        for date, values in performance_by_date.items()
    ]
    
    # Alert Trends
    alert_trends = db.query(Alert)\
        .filter(Alert.created_at >= start_date)\
        .order_by(Alert.created_at)\
        .all()
    
    alert_by_date = {}
    for alert in alert_trends:
        date_str = alert.created_at.strftime("%Y-%m-%d")
        if date_str not in alert_by_date:
            alert_by_date[date_str] = 0
        alert_by_date[date_str] += 1
    
    alert_trend_data = [
        {
            "date": date,
            "alert_count": count
        }
        for date, count in alert_by_date.items()
    ]
    
    return {
        "quality_trends": quality_trend_data,
        "performance_trends": performance_trend_data,
        "alert_trends": alert_trend_data
    }

@router.get("/recent-activity")
async def get_recent_activity(db: Session = Depends(get_db), limit: int = 20):
    """Get recent activity across all systems"""
    
    activities = []
    
    # Recent quality checks
    recent_checks = db.query(DataQualityCheck)\
        .order_by(DataQualityCheck.created_at.desc())\
        .limit(limit // 3)\
        .all()
    
    for check in recent_checks:
        activities.append({
            "type": "data_quality",
            "timestamp": check.created_at,
            "title": f"Quality check: {check.check_type}",
            "description": check.details,
            "status": check.status,
            "score": check.score
        })
    
    # Recent model performance
    recent_performance = db.query(ModelPerformance)\
        .order_by(ModelPerformance.timestamp.desc())\
        .limit(limit // 3)\
        .all()
    
    for perf in recent_performance:
        activities.append({
            "type": "model_performance",
            "timestamp": perf.timestamp,
            "title": f"Model performance: {perf.metric_name}",
            "description": f"{perf.model_name} - {perf.metric_value:.3f}",
            "status": "success",
            "score": perf.metric_value
        })
    
    # Recent alerts
    recent_alerts = db.query(Alert)\
        .order_by(Alert.created_at.desc())\
        .limit(limit // 3)\
        .all()
    
    for alert in recent_alerts:
        activities.append({
            "type": "alert",
            "timestamp": alert.created_at,
            "title": alert.title,
            "description": alert.message,
            "status": alert.severity,
            "score": None
        })
    
    # Sort all activities by timestamp
    activities.sort(key=lambda x: x["timestamp"], reverse=True)
    
    return activities[:limit]

@router.get("/system-status")
async def get_system_status(db: Session = Depends(get_db)):
    """Get overall system status"""
    
    # Check data quality status
    recent_quality_checks = db.query(DataQualityCheck)\
        .order_by(DataQualityCheck.created_at.desc())\
        .limit(10)\
        .all()
    
    quality_status = "healthy"
    if recent_quality_checks:
        failed_checks = sum(1 for check in recent_quality_checks if check.status == "failed")
        if failed_checks > 0:
            quality_status = "warning" if failed_checks < 3 else "critical"
    
    # Check model monitoring status
    recent_drift = db.query(ModelDrift)\
        .order_by(ModelDrift.timestamp.desc())\
        .limit(10)\
        .all()
    
    model_status = "healthy"
    if recent_drift:
        drift_detected = sum(1 for d in recent_drift if d.is_drift_detected)
        if drift_detected > 0:
            model_status = "warning" if drift_detected < 3 else "critical"
    
    # Check alert status
    critical_alerts = db.query(Alert)\
        .filter(Alert.severity == "critical", Alert.is_resolved == False)\
        .count()
    
    alert_status = "healthy" if critical_alerts == 0 else "critical"
    
    # Overall status
    if any(status == "critical" for status in [quality_status, model_status, alert_status]):
        overall_status = "critical"
    elif any(status == "warning" for status in [quality_status, model_status, alert_status]):
        overall_status = "warning"
    else:
        overall_status = "healthy"
    
    return {
        "overall_status": overall_status,
        "components": {
            "data_quality": quality_status,
            "model_monitoring": model_status,
            "alerts": alert_status
        },
        "last_updated": datetime.now()
    } 