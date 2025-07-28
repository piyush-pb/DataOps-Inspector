from fastapi import APIRouter, Depends, HTTPException, UploadFile, File
from sqlalchemy.orm import Session
from typing import List, Optional
import pandas as pd
import json
from datetime import datetime

from app.core.database import get_db
from app.models.data_quality import DataSource, DataQualityCheck
from app.services.data_quality_service import DataQualityService
from app.schemas.data_quality import (
    DataSourceCreate, DataSourceResponse, 
    QualityCheckResponse, QualityCheckCreate
)

router = APIRouter()
data_quality_service = DataQualityService()

@router.post("/upload", response_model=DataSourceResponse)
async def upload_data_source(
    file: UploadFile = File(...),
    name: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """Upload a CSV file and create a data source"""
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    try:
        # Read CSV file
        df = pd.read_csv(file.file)
        
        # Create data source
        source_name = name or file.filename.replace('.csv', '')
        data_source = DataSource(
            name=source_name,
            source_type="csv",
            source_path=f"uploads/{file.filename}",
            schema=df.dtypes.to_dict()
        )
        
        db.add(data_source)
        db.commit()
        db.refresh(data_source)
        
        # Run initial quality checks
        quality_results = data_quality_service.run_quality_checks(df, data_source.id)
        
        for result in quality_results:
            quality_check = DataQualityCheck(
                data_source_id=data_source.id,
                check_type=result["check_type"],
                check_result=result["result"],
                status=result["status"],
                score=result["score"],
                details=result["details"]
            )
            db.add(quality_check)
        
        db.commit()
        
        return DataSourceResponse(
            id=data_source.id,
            name=data_source.name,
            source_type=data_source.source_type,
            created_at=data_source.created_at,
            quality_score=sum(r["score"] for r in quality_results) / len(quality_results)
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")

@router.get("/sources", response_model=List[DataSourceResponse])
async def get_data_sources(db: Session = Depends(get_db)):
    """Get all data sources"""
    sources = db.query(DataSource).filter(DataSource.is_active == True).all()
    return [
        DataSourceResponse(
            id=source.id,
            name=source.name,
            source_type=source.source_type,
            created_at=source.created_at
        ) for source in sources
    ]

@router.get("/sources/{source_id}/quality", response_model=List[QualityCheckResponse])
async def get_quality_checks(
    source_id: int,
    limit: int = 10,
    db: Session = Depends(get_db)
):
    """Get quality checks for a specific data source"""
    checks = db.query(DataQualityCheck)\
        .filter(DataQualityCheck.data_source_id == source_id)\
        .order_by(DataQualityCheck.created_at.desc())\
        .limit(limit)\
        .all()
    
    return [
        QualityCheckResponse(
            id=check.id,
            check_type=check.check_type,
            status=check.status,
            score=check.score,
            details=check.details,
            created_at=check.created_at
        ) for check in checks
    ]

@router.post("/sources/{source_id}/check", response_model=List[QualityCheckResponse])
async def run_quality_check(
    source_id: int,
    db: Session = Depends(get_db)
):
    """Run quality checks on a data source"""
    # Get data source
    data_source = db.query(DataSource).filter(DataSource.id == source_id).first()
    if not data_source:
        raise HTTPException(status_code=404, detail="Data source not found")
    
    try:
        # Read data (in production, this would be more sophisticated)
        df = pd.read_csv(data_source.source_path)
        
        # Run quality checks
        quality_results = data_quality_service.run_quality_checks(df, source_id)
        
        # Save results
        checks = []
        for result in quality_results:
            quality_check = DataQualityCheck(
                data_source_id=source_id,
                check_type=result["check_type"],
                check_result=result["result"],
                status=result["status"],
                score=result["score"],
                details=result["details"]
            )
            db.add(quality_check)
            checks.append(quality_check)
        
        db.commit()
        
        return [
            QualityCheckResponse(
                id=check.id,
                check_type=check.check_type,
                status=check.status,
                score=check.score,
                details=check.details,
                created_at=check.created_at
            ) for check in checks
        ]
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error running quality checks: {str(e)}")

@router.get("/summary")
async def get_quality_summary(db: Session = Depends(get_db)):
    """Get overall data quality summary"""
    total_sources = db.query(DataSource).filter(DataSource.is_active == True).count()
    
    # Get recent quality checks
    recent_checks = db.query(DataQualityCheck)\
        .order_by(DataQualityCheck.created_at.desc())\
        .limit(100)\
        .all()
    
    if not recent_checks:
        return {
            "total_sources": total_sources,
            "average_quality_score": 0,
            "issues_count": 0,
            "last_check": None
        }
    
    avg_score = sum(check.score for check in recent_checks) / len(recent_checks)
    issues_count = sum(1 for check in recent_checks if check.status in ["failed", "warning"])
    
    return {
        "total_sources": total_sources,
        "average_quality_score": round(avg_score, 3),
        "issues_count": issues_count,
        "last_check": recent_checks[0].created_at
    } 