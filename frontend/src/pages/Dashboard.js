import React, { useState, useEffect } from 'react';
import {
  Grid,
  Card,
  CardContent,
  Typography,
  Box,
  CircularProgress,
  Alert,
} from '@mui/material';
import {
  DataUsage as DataQualityIcon,
  Psychology as ModelIcon,
  Notifications as AlertsIcon,
  TrendingUp as TrendingUpIcon,
} from '@mui/icons-material';
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, ResponsiveContainer } from 'recharts';

import MetricCard from '../components/MetricCard';
import RecentActivity from '../components/RecentActivity';

function Dashboard() {
  const [overview, setOverview] = useState(null);
  const [trends, setTrends] = useState(null);
  const [recentActivity, setRecentActivity] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDashboardData();
  }, []);

  const fetchDashboardData = async () => {
    try {
      setLoading(true);
      
      // Fetch overview data
      const overviewResponse = await fetch('/api/v1/dashboard/overview');
      const overviewData = await overviewResponse.json();
      setOverview(overviewData);
      
      // Fetch trends data
      const trendsResponse = await fetch('/api/v1/dashboard/trends');
      const trendsData = await trendsResponse.json();
      setTrends(trendsData);
      
      // Fetch recent activity
      const activityResponse = await fetch('/api/v1/dashboard/recent-activity');
      const activityData = await activityResponse.json();
      setRecentActivity(activityData);
      
    } catch (err) {
      setError('Failed to load dashboard data');
      console.error('Error fetching dashboard data:', err);
    } finally {
      setLoading(false);
    }
  };

  if (loading) {
    return (
      <Box display="flex" justifyContent="center" alignItems="center" minHeight="400px">
        <CircularProgress />
      </Box>
    );
  }

  if (error) {
    return (
      <Alert severity="error" sx={{ mb: 2 }}>
        {error}
      </Alert>
    );
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard Overview
      </Typography>
      
      {/* Overview Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Data Quality Score"
            value={overview?.data_quality?.average_quality_score || 0}
            icon={<DataQualityIcon />}
            color="primary"
            unit="%"
            formatValue={(value) => (value * 100).toFixed(1)}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Model Accuracy"
            value={overview?.model_monitoring?.average_accuracy || 0}
            icon={<ModelIcon />}
            color="secondary"
            unit="%"
            formatValue={(value) => (value * 100).toFixed(1)}
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Active Alerts"
            value={overview?.alerts?.unresolved_alerts || 0}
            icon={<AlertsIcon />}
            color="warning"
          />
        </Grid>
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Data Sources"
            value={overview?.data_quality?.total_sources || 0}
            icon={<TrendingUpIcon />}
            color="success"
          />
        </Grid>
      </Grid>

      {/* Charts */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Data Quality Trends
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={trends?.quality_trends || []}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="average_score"
                    stroke="#1976d2"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
        
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Model Performance Trends
              </Typography>
              <ResponsiveContainer width="100%" height={300}>
                <LineChart data={trends?.performance_trends || []}>
                  <CartesianGrid strokeDasharray="3 3" />
                  <XAxis dataKey="date" />
                  <YAxis />
                  <Tooltip />
                  <Line
                    type="monotone"
                    dataKey="average_accuracy"
                    stroke="#dc004e"
                    strokeWidth={2}
                  />
                </LineChart>
              </ResponsiveContainer>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Recent Activity */}
      <Grid container spacing={3}>
        <Grid item xs={12}>
          <RecentActivity activities={recentActivity} />
        </Grid>
      </Grid>
    </Box>
  );
}

export default Dashboard; 