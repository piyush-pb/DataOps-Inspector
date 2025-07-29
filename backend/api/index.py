from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os

# Create FastAPI app
app = FastAPI(
    title="DataOps Inspector API",
    description="Automated Data Quality & Model Drift Monitoring Platform",
    version="1.0.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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

# Dashboard endpoints
@app.get("/api/v1/dashboard/overview")
async def dashboard_overview():
    return {
        "status": "success",
        "data": {
            "total_datasets": 0,
            "active_models": 0,
            "alerts_count": 0,
            "data_quality_score": 0,
            "system_status": "operational"
        }
    }

@app.get("/api/v1/dashboard/system-status")
async def system_status():
    return {
        "status": "success",
        "data": {
            "database": "disconnected",
            "api": "running",
            "frontend": "connected",
            "overall_status": "operational"
        }
    }

@app.get("/api/v1/dashboard/metrics")
async def dashboard_metrics():
    return {
        "status": "success",
        "data": {
            "data_quality_score": 0,
            "model_accuracy": 0,
            "system_uptime": 100,
            "active_alerts": 0
        }
    }

@app.get("/api/v1/dashboard/recent-activity")
async def recent_activity():
    return {
        "status": "success",
        "data": [
            {
                "id": 1,
                "type": "system",
                "message": "Application deployed successfully",
                "timestamp": "2024-01-01T00:00:00Z",
                "status": "info"
            }
        ]
    }

# Data Quality endpoints
@app.get("/api/v1/data-quality/metrics")
async def data_quality_metrics():
    return {
        "status": "success",
        "data": {
            "total_records": 0,
            "missing_values": 0,
            "duplicates": 0,
            "quality_score": 0
        }
    }

@app.get("/api/v1/data-quality/issues")
async def data_quality_issues():
    return {
        "status": "success",
        "data": []
    }

# Model Monitoring endpoints
@app.get("/api/v1/model-monitoring/models")
async def get_models():
    return {
        "status": "success",
        "data": []
    }

# Alerts endpoints
@app.get("/api/v1/alerts")
async def get_alerts():
    return {
        "status": "success",
        "data": []
    }

# This is the entry point for Vercel serverless functions
handler = app 