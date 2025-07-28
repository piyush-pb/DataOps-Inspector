# DataOps Inspector: Automated Data Quality & Model Drift Platform

A comprehensive platform for monitoring data quality, detecting model drift, and providing automated alerts for data and ML operations.

## 🚀 Features

### Data Pipeline & Quality Monitoring
- Upload/connect to CSV files or public datasets
- Automated ETL pipeline with Python/Pandas
- Real-time data quality checks (missing values, duplicates, schema drift)
- PostgreSQL storage for logs and results

### Data Quality Dashboard
- Interactive React dashboard with real-time metrics
- Data summary visualizations (row count, unique values)
- Issue tracking (nulls, duplicates, schema changes)
- Historical trend charts

### ML Model Deployment & Drift Monitoring
- Sample ML pipeline with scikit-learn
- Real-time performance tracking (accuracy, F1 score)
- Model drift detection using Evidently AI
- Automated alerts for performance degradation

### Notifications
- Email alerts for critical issues
- Web dashboard notifications
- Configurable alert thresholds

## 🏗️ Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Frontend      │    │   Backend API   │    │   Database      │
│   (React)       │◄──►│   (FastAPI)     │◄──►│   (PostgreSQL)  │
└─────────────────┘    └─────────────────┘    └─────────────────┘
         │                       │                       │
         │              ┌─────────────────┐              │
         └──────────────►│   ML Pipeline   │◄─────────────┘
                        │   (scikit-learn)│
                        └─────────────────┘
```

## 🛠️ Tech Stack

- **Backend**: Python, FastAPI, Pandas, SQLAlchemy, scikit-learn, Evidently AI
- **Frontend**: React, Chart.js, Material-UI
- **Database**: PostgreSQL
- **Deployment**: Docker, Docker Compose
- **Notifications**: SMTP Email

## 🚀 Quick Start

### Prerequisites
- Docker and Docker Compose
- Git

### Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd DataOpsInspector
```

2. Start the platform:
```bash
docker-compose up -d
```

3. Access the application:
- Frontend: http://localhost:3000
- Backend API: http://localhost:8000
- API Documentation: http://localhost:8000/docs

### Environment Variables

Copy `.env.example` to `.env` and configure:
```bash
cp .env.example .env
```

## 📊 Usage

### 1. Data Upload & Monitoring
- Navigate to the Data Quality section
- Upload a CSV file or connect to a data source
- View real-time quality metrics and issues

### 2. ML Model Deployment
- Go to the Model Monitoring section
- Deploy a sample model or upload your own
- Monitor performance and drift detection

### 3. Alerts & Notifications
- Configure alert thresholds in Settings
- Receive email notifications for critical issues
- View alerts in the dashboard

## 📁 Project Structure

```
DataOpsInspector/
├── backend/                 # FastAPI backend
│   ├── app/
│   │   ├── api/            # API routes
│   │   ├── core/           # Core configurations
│   │   ├── models/         # Database models
│   │   ├── services/       # Business logic
│   │   └── utils/          # Utilities
│   ├── requirements.txt
│   └── Dockerfile
├── frontend/               # React frontend
│   ├── src/
│   │   ├── components/     # React components
│   │   ├── pages/          # Page components
│   │   ├── services/       # API services
│   │   └── utils/          # Utilities
│   ├── package.json
│   └── Dockerfile
├── ml_pipeline/           # ML pipeline components
│   ├── models/            # ML models
│   ├── drift_detection/   # Drift detection logic
│   └── requirements.txt
├── docker-compose.yml     # Docker orchestration
├── .env.example          # Environment variables template
└── README.md             # This file
```

## 🔧 Development

### Backend Development
```bash
cd backend
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend Development
```bash
cd frontend
npm install
npm start
```

### Database
```bash
# Using Docker
docker-compose up postgres

# Or connect directly
psql -h localhost -U dataops_user -d dataops_db
```

## 📈 Monitoring & Metrics

### Data Quality Metrics
- Missing value percentage
- Duplicate record count
- Schema change detection
- Data type validation
- Outlier detection

### Model Performance Metrics
- Accuracy, Precision, Recall, F1-Score
- Feature distribution drift
- Prediction drift
- Model performance trends

## 🚨 Alerting

### Alert Types
- **Data Quality Alerts**: High missing values, schema changes
- **Model Drift Alerts**: Performance degradation, feature drift
- **System Alerts**: Pipeline failures, connection issues

### Alert Channels
- Email notifications
- Dashboard notifications
- Webhook support (future)

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

## 🆘 Support

For support and questions:
- Create an issue in the repository
- Check the documentation at `/docs`
- Review the API documentation at `http://localhost:8000/docs`

## 🎯 Roadmap

- [ ] Advanced ML model support (TensorFlow, PyTorch)
- [ ] Real-time streaming data support
- [ ] Advanced visualization options
- [ ] Multi-tenant architecture
- [ ] REST API for external integrations
- [ ] Advanced alerting rules engine
- [ ] Data lineage tracking
- [ ] Automated model retraining 