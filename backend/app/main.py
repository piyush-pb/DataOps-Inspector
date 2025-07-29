from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import uvicorn
import os

from app.core.config import settings

app = FastAPI(
    title=settings.project_name,
    description="Automated Data Quality & Model Drift Monitoring Platform",
    version=settings.version,
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": settings.project_name}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": settings.project_name,
        "version": settings.version,
        "docs": "/docs",
        "health": "/health"
    }

# Simple dashboard endpoint for testing
@app.get("/api/v1/dashboard/overview")
async def dashboard_overview():
    return {
        "status": "success",
        "data": {
            "total_datasets": 0,
            "active_models": 0,
            "alerts_count": 0,
            "data_quality_score": 0
        }
    }

@app.get("/api/v1/dashboard/system-status")
async def system_status():
    return {
        "status": "success",
        "data": {
            "database": "disconnected",
            "api": "running",
            "frontend": "connected"
        }
    }

# Try to import and include API routes if database is available
try:
    from app.core.database import engine, Base
    from app.api.routes import data_quality, model_monitoring, alerts, dashboard
    
    # Create database tables
    Base.metadata.create_all(bind=engine)
    
    # Include API routes
    app.include_router(data_quality.router, prefix=f"{settings.api_v1_prefix}/data-quality", tags=["Data Quality"])
    app.include_router(model_monitoring.router, prefix=f"{settings.api_v1_prefix}/model-monitoring", tags=["Model Monitoring"])
    app.include_router(alerts.router, prefix=f"{settings.api_v1_prefix}/alerts", tags=["Alerts"])
    app.include_router(dashboard.router, prefix=f"{settings.api_v1_prefix}/dashboard", tags=["Dashboard"])
    
except Exception as e:
    print(f"Database or routes not available: {e}")
    # Continue without database-dependent routes

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", 8000)),
        reload=True
    ) 