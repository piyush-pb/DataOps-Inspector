# DataOps Inspector - Quick Start Guide

## 🚀 Getting Started

### Prerequisites
- Docker and Docker Compose installed
- Git (optional)

### Quick Start

1. **Clone or download the project**
   ```bash
   git clone <repository-url>
   cd DataOpsInspector
   ```

2. **Start the platform**
   ```bash
   # On Windows
   start.bat
   
   # On Linux/Mac
   docker-compose up --build -d
   ```

3. **Access the application**
   - Frontend Dashboard: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

## 📊 Demo Walkthrough

### 1. Data Quality Monitoring
1. Navigate to "Data Quality" in the sidebar
2. Click "Upload CSV" and select the `sample_data.csv` file
3. View the quality metrics and issues detected
4. Run additional quality checks on the uploaded data

### 2. Model Monitoring
1. Go to "Model Monitoring" section
2. Click "Deploy Model" to deploy a sample ML model
3. Use the "Check Drift" button to simulate drift detection
4. View model performance metrics and drift alerts

### 3. Alerts & Notifications
1. Visit the "Alerts" page to see system notifications
2. Test the alert system using the test endpoint
3. Configure email notifications in Settings

### 4. Dashboard Overview
1. The main dashboard shows:
   - Data quality score
   - Model accuracy
   - Active alerts
   - Recent activity
   - Trend charts

## 🔧 Configuration

### Environment Variables
Copy `.env.example` to `.env` and configure:
```bash
# Database
DATABASE_URL=postgresql://dataops_user:dataops_password@localhost:5432/dataops_db

# Email Notifications
SMTP_HOST=smtp.gmail.com
SMTP_USER=your-email@gmail.com
SMTP_PASSWORD=your-app-password

# ML Configuration
DRIFT_THRESHOLD=0.1
PERFORMANCE_THRESHOLD=0.8
```

### Sample Data
The platform includes `sample_data.csv` with employee data for testing:
- 10 records with various data quality issues
- Missing values, duplicates, and outliers
- Perfect for testing quality checks

## 🛠️ Development

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

### Database Access
```bash
# Connect to PostgreSQL
psql -h localhost -U dataops_user -d dataops_db
# Password: dataops_password
```

## 📈 Features Demonstrated

### Data Quality Checks
- Missing value detection
- Duplicate record identification
- Data type validation
- Outlier detection
- Schema drift monitoring

### ML Model Monitoring
- Model deployment and serving
- Performance tracking
- Drift detection (feature, prediction, data)
- Automated alerts

### Alert System
- Email notifications
- Web dashboard alerts
- Configurable thresholds
- Alert resolution workflow

### Dashboard & Visualization
- Real-time metrics
- Trend analysis
- Interactive charts
- System health monitoring

## 🚨 Troubleshooting

### Common Issues

1. **Port conflicts**
   - Ensure ports 3000, 8000, and 5432 are available
   - Modify ports in `docker-compose.yml` if needed

2. **Database connection issues**
   - Wait for PostgreSQL to fully start (30-60 seconds)
   - Check database logs: `docker-compose logs postgres`

3. **Frontend not loading**
   - Check if backend is running: `docker-compose ps`
   - View logs: `docker-compose logs frontend`

4. **File upload issues**
   - Ensure CSV files are properly formatted
   - Check file size limits (100MB max)

### Useful Commands

```bash
# View all logs
docker-compose logs -f

# Restart specific service
docker-compose restart backend

# Stop all services
docker-compose down

# Clean up volumes
docker-compose down -v
```

## 📚 Next Steps

1. **Customize Data Quality Rules**
   - Modify `backend/app/services/data_quality_service.py`
   - Add custom validation logic

2. **Deploy Your Own Models**
   - Replace sample models in `backend/app/services/model_monitoring_service.py`
   - Integrate with your ML pipeline

3. **Configure Real Email Notifications**
   - Set up SMTP credentials in `.env`
   - Test email alerts

4. **Scale the Platform**
   - Add authentication
   - Implement multi-tenancy
   - Add more data sources

## 🆘 Support

- Check the main README.md for detailed documentation
- Review API documentation at http://localhost:8000/docs
- Create issues in the repository for bugs or feature requests

---

**DataOps Inspector** - Your complete solution for data quality and ML model monitoring! 🎯 