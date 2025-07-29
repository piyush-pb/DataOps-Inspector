from flask import Flask, jsonify
from flask_cors import CORS
import os

# Create Flask app
app = Flask(__name__)
CORS(app)

# Health check endpoint
@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "DataOps Inspector API"})

# Root endpoint
@app.route('/')
def root():
    return jsonify({
        "message": "DataOps Inspector API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/health"
    })

# Dashboard endpoints
@app.route('/api/v1/dashboard/overview')
def dashboard_overview():
    return jsonify({
        "status": "success",
        "data": {
            "total_datasets": 5,
            "active_models": 3,
            "alerts_count": 2,
            "data_quality_score": 0.85,
            "system_status": "operational"
        }
    })

@app.route('/api/v1/dashboard/trends')
def dashboard_trends():
    return jsonify({
        "status": "success",
        "data": {
            "quality_trends": [
                {
                    "date": "2024-01-01",
                    "average_score": 85.5
                },
                {
                    "date": "2024-01-02", 
                    "average_score": 87.2
                },
                {
                    "date": "2024-01-03",
                    "average_score": 89.1
                }
            ],
            "performance_trends": [
                {
                    "date": "2024-01-01",
                    "average_accuracy": 92.1
                },
                {
                    "date": "2024-01-02",
                    "average_accuracy": 91.8
                },
                {
                    "date": "2024-01-03",
                    "average_accuracy": 93.2
                }
            ],
            "alert_trends": [
                {
                    "date": "2024-01-01",
                    "alert_count": 2
                },
                {
                    "date": "2024-01-02",
                    "alert_count": 1
                },
                {
                    "date": "2024-01-03",
                    "alert_count": 0
                }
            ]
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
            "data_quality_score": 85,
            "model_accuracy": 92.5,
            "system_uptime": 99.8,
            "active_alerts": 2
        }
    })

@app.route('/api/v1/dashboard/recent-activity')
def recent_activity():
    return jsonify({
        "status": "success",
        "data": [
            {
                "id": 1,
                "type": "data_quality",
                "title": "Data Quality Check Completed",
                "description": "Quality check for dataset 'customer_data.csv' completed successfully",
                "timestamp": "2024-01-03T10:30:00Z",
                "status": "success"
            },
            {
                "id": 2,
                "type": "model_performance",
                "title": "Model Performance Update",
                "description": "Model 'fraud_detection_v2' accuracy maintained at 92.5%",
                "timestamp": "2024-01-03T09:15:00Z",
                "status": "success"
            },
            {
                "id": 3,
                "type": "alert",
                "title": "Data Drift Detected",
                "description": "Significant drift detected in feature 'transaction_amount'",
                "timestamp": "2024-01-03T08:45:00Z",
                "status": "warning"
            },
            {
                "id": 4,
                "type": "data_quality",
                "title": "Missing Values Alert",
                "description": "High number of missing values detected in 'email' field",
                "timestamp": "2024-01-03T07:20:00Z",
                "status": "warning"
            }
        ]
    })

# Data Quality endpoints
@app.route('/api/v1/data-quality/metrics')
def data_quality_metrics():
    return jsonify({
        "status": "success",
        "data": {
            "total_records": 15000,
            "missing_values": 150,
            "duplicates": 25,
            "quality_score": 85
        }
    })

@app.route('/api/v1/data-quality/issues')
def data_quality_issues():
    return jsonify({
        "status": "success",
        "data": [
            {
                "id": 1,
                "type": "missing_values",
                "field": "email",
                "count": 150,
                "severity": "medium"
            },
            {
                "id": 2,
                "type": "duplicates",
                "field": "customer_id",
                "count": 25,
                "severity": "high"
            }
        ]
    })

# Model Monitoring endpoints
@app.route('/api/v1/model-monitoring/models')
def get_models():
    return jsonify({
        "status": "success",
        "data": [
            {
                "id": 1,
                "name": "fraud_detection_v2",
                "version": "2.1.0",
                "accuracy": 92.5,
                "status": "active"
            },
            {
                "id": 2,
                "name": "customer_churn_v1",
                "version": "1.0.0",
                "accuracy": 88.3,
                "status": "active"
            }
        ]
    })

# Alerts endpoints
@app.route('/api/v1/alerts')
def get_alerts():
    return jsonify({
        "status": "success",
        "data": [
            {
                "id": 1,
                "type": "data_drift",
                "title": "Data Drift Detected",
                "message": "Significant drift in transaction_amount feature",
                "severity": "warning",
                "timestamp": "2024-01-03T08:45:00Z",
                "status": "open"
            },
            {
                "id": 2,
                "type": "quality_issue",
                "title": "Missing Values Alert",
                "message": "High number of missing values in email field",
                "severity": "medium",
                "timestamp": "2024-01-03T07:20:00Z",
                "status": "open"
            }
        ]
    })

if __name__ == '__main__':
    print("🚀 Starting DataOps Inspector Local API Server...")
    print("📍 Server will be available at: http://localhost:8000")
    print("🔗 API endpoints available at: http://localhost:8000/api/v1/")
    print("💚 Health check at: http://localhost:8000/health")
    print("\nPress Ctrl+C to stop the server\n")
    
    app.run(host='0.0.0.0', port=8000, debug=True) 