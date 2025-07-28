from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
import uvicorn
import os

from app.core.config import settings
from app.api.routes import data_quality, model_monitoring, alerts, dashboard
from app.core.database import engine, Base

# Create database tables
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="DataOps Inspector API",
    description="Automated Data Quality & Model Drift Monitoring Platform",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(data_quality.router, prefix="/api/v1/data-quality", tags=["Data Quality"])
app.include_router(model_monitoring.router, prefix="/api/v1/model-monitoring", tags=["Model Monitoring"])
app.include_router(alerts.router, prefix="/api/v1/alerts", tags=["Alerts"])
app.include_router(dashboard.router, prefix="/api/v1/dashboard", tags=["Dashboard"])

# Health check endpoint
@app.get("/health")
async def health_check():
    return {"status": "healthy", "service": "DataOps Inspector API"}

# Root endpoint
@app.get("/")
async def root():
    return {
        "message": "DataOps Inspector API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    ) 