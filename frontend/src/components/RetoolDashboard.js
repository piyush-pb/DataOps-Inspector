import React, { useState, useEffect } from 'react';
import { Box, Card, CardContent, Typography, Button, Chip, Alert, CircularProgress } from '@mui/material';
import { styled } from '@mui/material/styles';
import { DataUsage, Analytics, Settings, Refresh } from '@mui/icons-material';

const RetoolContainer = styled('div')(({ theme }) => ({
  width: '100%',
  height: '600px',
  border: `1px solid ${theme.palette.divider}`,
  borderRadius: theme.shape.borderRadius,
  overflow: 'hidden',
  position: 'relative',
  backgroundColor: '#f5f5f5',
}));

const RetoolPlaceholder = styled('div')(({ theme }) => ({
  width: '100%',
  height: '100%',
  display: 'flex',
  flexDirection: 'column',
  alignItems: 'center',
  justifyContent: 'center',
  backgroundColor: '#ffffff',
  color: theme.palette.text.secondary,
  '& .retool-icon': {
    fontSize: '48px',
    marginBottom: theme.spacing(2),
    color: '#6366f1',
  },
  '& .retool-title': {
    fontSize: '24px',
    fontWeight: 600,
    marginBottom: theme.spacing(1),
    color: theme.palette.text.primary,
  },
  '& .retool-description': {
    textAlign: 'center',
    maxWidth: '400px',
    marginBottom: theme.spacing(3),
  },
}));

const RetoolDashboard = () => {
  const [isLoading, setIsLoading] = useState(true);
  const [retoolStatus, setRetoolStatus] = useState('connecting');
  const [dashboardData, setDashboardData] = useState({
    dataSources: 12,
    activePipelines: 8,
    alerts: 3,
    lastSync: new Date().toISOString(),
  });

  useEffect(() => {
    // Simulate Retool app loading
    const timer = setTimeout(() => {
      setIsLoading(false);
      setRetoolStatus('connected');
    }, 2000);

    return () => clearTimeout(timer);
  }, []);

  const handleRefresh = () => {
    setIsLoading(true);
    setRetoolStatus('refreshing');
    
    setTimeout(() => {
      setDashboardData(prev => ({
        ...prev,
        lastSync: new Date().toISOString(),
        alerts: Math.floor(Math.random() * 5) + 1,
      }));
      setIsLoading(false);
      setRetoolStatus('connected');
    }, 1500);
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'connected': return 'success';
      case 'connecting': return 'warning';
      case 'refreshing': return 'info';
      default: return 'error';
    }
  };

  const getStatusText = (status) => {
    switch (status) {
      case 'connected': return 'Connected';
      case 'connecting': return 'Connecting...';
      case 'refreshing': return 'Refreshing...';
      default: return 'Disconnected';
    }
  };

  return (
    <Box sx={{ p: 3 }}>
      <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 3 }}>
        <Typography variant="h4" component="h1" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
          <DataUsage sx={{ color: 'primary.main' }} />
          Retool DataOps Dashboard
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Chip
            label={getStatusText(retoolStatus)}
            color={getStatusColor(retoolStatus)}
            size="small"
          />
          <Button
            variant="outlined"
            startIcon={<Refresh />}
            onClick={handleRefresh}
            disabled={isLoading}
          >
            Refresh
          </Button>
        </Box>
      </Box>

      {/* Quick Stats */}
      <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: 2, mb: 3 }}>
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Data Sources
            </Typography>
            <Typography variant="h4" component="div">
              {dashboardData.dataSources}
            </Typography>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Active Pipelines
            </Typography>
            <Typography variant="h4" component="div">
              {dashboardData.activePipelines}
            </Typography>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Active Alerts
            </Typography>
            <Typography variant="h4" component="div" color="error">
              {dashboardData.alerts}
            </Typography>
          </CardContent>
        </Card>
        
        <Card>
          <CardContent>
            <Typography color="textSecondary" gutterBottom>
              Last Sync
            </Typography>
            <Typography variant="body2" component="div">
              {new Date(dashboardData.lastSync).toLocaleString()}
            </Typography>
          </CardContent>
        </Card>
      </Box>

      {/* Retool App Embed */}
      <Card sx={{ mb: 3 }}>
        <CardContent sx={{ p: 0 }}>
          <Box sx={{ p: 2, borderBottom: 1, borderColor: 'divider' }}>
            <Typography variant="h6" sx={{ display: 'flex', alignItems: 'center', gap: 1 }}>
              <Analytics sx={{ fontSize: 20 }} />
              Data Operations Management
            </Typography>
            <Typography variant="body2" color="textSecondary">
              Interactive dashboard for managing data pipelines, monitoring quality, and handling alerts
            </Typography>
          </Box>
          
          <RetoolContainer>
            {isLoading ? (
              <Box sx={{ 
                display: 'flex', 
                flexDirection: 'column', 
                alignItems: 'center', 
                justifyContent: 'center', 
                height: '100%',
                gap: 2
              }}>
                <CircularProgress size={40} />
                <Typography>Loading Retool Dashboard...</Typography>
              </Box>
            ) : (
              <RetoolPlaceholder>
                <div className="retool-icon">📊</div>
                <Typography className="retool-title">
                  Retool DataOps Dashboard
                </Typography>
                <Typography className="retool-description">
                  This is where your Retool app would be embedded. The app would include:
                </Typography>
                
                <Box sx={{ textAlign: 'left', maxWidth: '400px' }}>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    • <strong>Data Pipeline Management:</strong> Create, monitor, and manage ETL pipelines
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    • <strong>Quality Monitoring:</strong> Real-time data quality checks and alerts
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    • <strong>Alert Management:</strong> Configure and respond to data issues
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    • <strong>Performance Analytics:</strong> Track pipeline performance and metrics
                  </Typography>
                  <Typography variant="body2" sx={{ mb: 1 }}>
                    • <strong>User Management:</strong> Control access and permissions
                  </Typography>
                </Box>
                
                <Box sx={{ mt: 3, display: 'flex', gap: 2 }}>
                  <Button variant="contained" startIcon={<Settings />}>
                    Configure Retool
                  </Button>
                  <Button variant="outlined">
                    View Documentation
                  </Button>
                </Box>
              </RetoolPlaceholder>
            )}
          </RetoolContainer>
        </CardContent>
      </Card>

      {/* Integration Info */}
      <Alert severity="info" sx={{ mb: 2 }}>
        <Typography variant="body2">
          <strong>Retool Integration:</strong> This dashboard demonstrates how Retool can be embedded 
          into your DataOps application for advanced data management capabilities.
        </Typography>
      </Alert>

      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Integration Features
          </Typography>
          <Box sx={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: 2 }}>
            <Box>
              <Typography variant="subtitle2" color="primary" gutterBottom>
                🔗 API Integration
              </Typography>
              <Typography variant="body2">
                Connect to your existing APIs and data sources through Retool's built-in connectors
              </Typography>
            </Box>
            
            <Box>
              <Typography variant="subtitle2" color="primary" gutterBottom>
                📊 Custom Dashboards
              </Typography>
              <Typography variant="body2">
                Build interactive dashboards with drag-and-drop components and real-time data
              </Typography>
            </Box>
            
            <Box>
              <Typography variant="subtitle2" color="primary" gutterBottom>
                🔄 Workflow Automation
              </Typography>
              <Typography variant="body2">
                Automate data operations with custom workflows and scheduled tasks
              </Typography>
            </Box>
            
            <Box>
              <Typography variant="subtitle2" color="primary" gutterBottom>
                👥 Team Collaboration
              </Typography>
              <Typography variant="body2">
                Share dashboards and workflows with your team with role-based access control
              </Typography>
            </Box>
          </Box>
        </CardContent>
      </Card>
    </Box>
  );
};

export default RetoolDashboard; 