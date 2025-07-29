from flask import Flask, jsonify
from flask_cors import CORS

# Create Flask app
app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})

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
            "total_datasets": 0,
            "active_models": 0,
            "alerts_count": 0,
            "data_quality_score": 0,
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
                }
            ]
        }
    })

@app.route('/api/v1/dashboard/system-status')
def system_status():
    return jsonify({
        "status": "success",
        "data": {
            "database": "disconnected",
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
            "data_quality_score": 0,
            "model_accuracy": 0,
            "system_uptime": 100,
            "active_alerts": 0
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
                "description": "Application deployed successfully",
                "timestamp": "2024-01-01T00:00:00Z",
                "status": "success"
            },
            {
                "id": 2,
                "type": "model_performance",
                "title": "Model Performance Update",
                "description": "Model accuracy maintained at 92%",
                "timestamp": "2024-01-01T12:00:00Z",
                "status": "success"
            },
            {
                "id": 3,
                "type": "alert",
                "title": "System Alert",
                "description": "Database connection restored",
                "timestamp": "2024-01-02T00:00:00Z",
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
            "total_records": 0,
            "missing_values": 0,
            "duplicates": 0,
            "quality_score": 0
        }
    })

@app.route('/api/v1/data-quality/issues')
def data_quality_issues():
    return jsonify({
        "status": "success",
        "data": []
    })

# Model Monitoring endpoints
@app.route('/api/v1/model-monitoring/models')
def get_models():
    return jsonify({
        "status": "success",
        "data": []
    })

# Alerts endpoints
@app.route('/api/v1/alerts')
def get_alerts():
    return jsonify({
        "status": "success",
        "data": []
    })

# This is the entry point for Vercel serverless functions
if __name__ == '__main__':
    app.run(debug=True) 