from flask import Flask, request, jsonify
from flask_cors import CORS
import requests
import os

app = Flask(__name__)
CORS(app, origins=["*"])  # Allow all origins for development

# Backend API base URL
API_BASE_URL = "http://localhost:8000"

@app.route('/health')
def health_check():
    return jsonify({"status": "healthy", "service": "DataOps Inspector Proxy"})

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

# Proxy all other API requests
@app.route('/api/<path:path>', methods=['GET', 'POST', 'PUT', 'DELETE'])
def proxy_api(path):
    try:
        url = f"{API_BASE_URL}/api/{path}"
        response = requests.request(
            method=request.method,
            url=url,
            headers={key: value for key, value in request.headers if key != 'Host'},
            data=request.get_data(),
            cookies=request.cookies,
            allow_redirects=False
        )
        
        return response.content, response.status_code, response.headers.items()
    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"Proxy error: {str(e)}"}), 500

if __name__ == '__main__':
    print("🚀 Starting DataOps Inspector Proxy Server...")
    print("📍 Proxy Server: http://localhost:3002")
    print("🔗 Backend API: http://localhost:8000")
    print("🌐 Frontend: http://localhost:3004")
    app.run(host='0.0.0.0', port=3002, debug=True) 