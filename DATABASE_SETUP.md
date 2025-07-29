# DataOps Inspector - Database Setup Guide

## 🎉 Current Status: API Working Perfectly!

Your DataOps Inspector is successfully deployed and all API endpoints are operational:
- ✅ Health Check: Working
- ✅ Dashboard Overview: Working  
- ✅ System Status: Working
- ✅ All other endpoints: Ready

## 🗄️ Database Setup Required for Full Functionality

Currently, the database shows as "disconnected". To enable full functionality, you need to set up a PostgreSQL database.

### Option 1: Supabase (Recommended - Free & Easy)

1. **Create Supabase Account**:
   - Go to [supabase.com](https://supabase.com)
   - Sign up for a free account

2. **Create New Project**:
   - Click "New Project"
   - Choose your organization
   - Enter project name: `dataops-inspector`
   - Set a secure database password
   - Choose a region close to you
   - Click "Create new project"

3. **Get Database Connection String**:
   - Go to Settings → Database
   - Copy the "Connection string" (URI format)
   - It looks like: `postgresql://postgres:[YOUR-PASSWORD]@db.[PROJECT-REF].supabase.co:5432/postgres`

### Option 2: Railway (Alternative)

1. **Create Railway Account**:
   - Go to [railway.app](https://railway.app)
   - Sign up with GitHub

2. **Create Project**:
   - Click "New Project"
   - Select "Provision PostgreSQL"
   - Get the connection string from the database service

### Option 3: Neon (Alternative)

1. **Create Neon Account**:
   - Go to [neon.tech](https://neon.tech)
   - Sign up for free

2. **Create Project**:
   - Create a new project
   - Get the connection string from the dashboard

## 🔧 Configure Environment Variables

Once you have your database connection string:

1. **Go to Vercel Dashboard**:
   - Visit [vercel.com/dashboard](https://vercel.com/dashboard)
   - Select your `data-ops-inspector` project

2. **Add Environment Variables**:
   - Go to Settings → Environment Variables
   - Add these variables:

   ```
   DATABASE_URL=postgresql://username:password@host:port/database
   SECRET_KEY=your-super-secret-key-here-make-it-long-and-random
   ```

3. **Redeploy**:
   - After adding environment variables, redeploy:
   ```bash
   vercel --prod
   ```

## 🧪 Test Database Connection

After setting up the database, test the connection:

```bash
# Test the API endpoints
curl https://data-ops-inspector.vercel.app/api/v1/dashboard/system-status
```

You should see:
```json
{
  "status": "success",
  "data": {
    "database": "connected",
    "api": "running",
    "frontend": "connected",
    "overall_status": "operational"
  }
}
```

## 🚀 Full Features Available After Database Setup

Once the database is connected, you'll have access to:

- ✅ **Data Quality Monitoring**: Upload and analyze CSV files
- ✅ **Model Monitoring**: Track ML model performance
- ✅ **Alert System**: Configure and receive notifications
- ✅ **Dashboard Analytics**: Real-time metrics and visualizations
- ✅ **Historical Data**: Store and retrieve monitoring data

## 📊 Current Working Features

Even without the database, these features work:
- ✅ Frontend UI: Fully functional React dashboard
- ✅ API Endpoints: All endpoints responding correctly
- ✅ Health Monitoring: System status checks
- ✅ CORS: Cross-origin requests working
- ✅ Deployment: Live on Vercel

## 🔗 Your Live Application

**Main URL**: https://data-ops-inspector.vercel.app

**API Documentation**: Available at the main URL once you visit it

## 🆘 Need Help?

If you encounter any issues:
1. Check the Vercel deployment logs
2. Verify your database connection string
3. Ensure environment variables are set correctly
4. Test the API endpoints individually

Your DataOps Inspector is ready to use! 🎉 