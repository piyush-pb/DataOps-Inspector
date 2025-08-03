from flask import Flask, jsonify
from flask_cors import CORS
import os

app = Flask(__name__)

# Configure CORS to allow requests from the frontend
CORS(app, origins=[
    "http://localhost:3000",
    "http://localhost:3001", 
    "http://localhost:3002",
    "http://localhost:3003",
    "http://localhost:3004",
    "http://localhost:3005",
    "http://127.0.0.1:3000",
    "http://127.0.0.1:3004",
    "http://172.20.10.7:3004"
], supports_credentials=True)

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "DataOps Inspector"})

@app.route('/')
def root():
    return jsonify({
        "message": "DataOps Inspector",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    })

@app.route('/api/v1/dashboard/overview')
def dashboard_overview():
    return jsonify({
        "status": "success",
        "data": {
            "total_datasets": 5,
            "active_models": 3,
            "alerts_count": 2,
            "data_quality_score": 85.5
        }
    })

@app.route('/api/v1/dashboard/system-status')
def system_status():
    return jsonify({
        "status": "success",
        "data": {
            "database": "connected",
            "api": "running",
            "frontend": "connected",
            "overall_status": "operational"
        }
    })

@app.route('/api/v1/dashboard/metrics')
def dashboard_metrics():
    return jsonify({
        "status": "success",
        "data": {
            "data_quality_score": 85.5,
            "model_accuracy": 92.3,
            "active_alerts": 2,
            "total_datasets": 5,
            "drift_score": 0.15,
            "performance_score": 88.7
        }
    })

@app.route('/api/v1/dashboard/recent-activity')
def recent_activity():
    return jsonify({
        "status": "success",
        "data": [
            {
                "id": 1,
                "type": "data_quality_check",
                "message": "Data quality check completed for dataset 'sales_data'",
                "timestamp": "2024-01-15T10:30:00Z",
                "status": "success"
            },
            {
                "id": 2,
                "type": "model_drift",
                "message": "Model drift detected in 'customer_churn_model'",
                "timestamp": "2024-01-15T09:15:00Z",
                "status": "warning"
            },
            {
                "id": 3,
                "type": "alert",
                "message": "New alert: Data quality score dropped below threshold",
                "timestamp": "2024-01-15T08:45:00Z",
                "status": "error"
            }
        ]
    })

@app.route('/api/v1/dashboard/trends')
def dashboard_trends():
    return jsonify({
        "status": "success",
        "data": {
            "data_quality_trend": [85, 87, 86, 88, 85.5],
            "model_performance_trend": [90, 91, 92, 91.5, 92.3],
            "alert_frequency": [2, 1, 3, 2, 2]
        }
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000, debug=True) 