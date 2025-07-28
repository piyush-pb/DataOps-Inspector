import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  CircularProgress,
  Alert,
  Chip,
  Button,
} from '@mui/material';

function Alerts() {
  const [alerts, setAlerts] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchAlertsData();
  }, []);

  const fetchAlertsData = async () => {
    try {
      setLoading(true);
      
      // Fetch alerts
      const alertsResponse = await fetch('/api/v1/alerts/');
      const alertsData = await alertsResponse.json();
      setAlerts(alertsData);
      
      // Fetch alert summary
      const summaryResponse = await fetch('/api/v1/alerts/summary');
      const summaryData = await summaryResponse.json();
      setSummary(summaryData);
      
    } catch (err) {
      setError('Failed to load alerts data');
      console.error('Error fetching alerts data:', err);
    } finally {
      setLoading(false);
    }
  };

  const resolveAlert = async (alertId) => {
    try {
      const response = await fetch(`/api/v1/alerts/${alertId}/resolve`, {
        method: 'PUT',
      });

      if (response.ok) {
        fetchAlertsData(); // Refresh data
      }
    } catch (err) {
      console.error('Error resolving alert:', err);
    }
  };

  const getSeverityColor = (severity) => {
    switch (severity) {
      case 'critical':
        return 'error';
      case 'high':
        return 'warning';
      case 'medium':
        return 'info';
      default:
        return 'default';
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
        Alerts & Notifications
      </Typography>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Alerts
              </Typography>
              <Typography variant="h4">
                {summary?.total_alerts || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Unresolved
              </Typography>
              <Typography variant="h4">
                {summary?.unresolved_alerts || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Critical
              </Typography>
              <Typography variant="h4">
                {summary?.critical_alerts || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={3}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Last 24h
              </Typography>
              <Typography variant="h4">
                {summary?.recent_alerts_24h || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Alerts Table */}
      <Card>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Recent Alerts
          </Typography>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Type</TableCell>
                  <TableCell>Severity</TableCell>
                  <TableCell>Title</TableCell>
                  <TableCell>Source</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {alerts.map((alert) => (
                  <TableRow key={alert.id}>
                    <TableCell>
                      <Chip label={alert.alert_type} size="small" />
                    </TableCell>
                    <TableCell>
                      <Chip
                        label={alert.severity}
                        color={getSeverityColor(alert.severity)}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>{alert.title}</TableCell>
                    <TableCell>{alert.source || 'N/A'}</TableCell>
                    <TableCell>
                      <Chip
                        label={alert.is_resolved ? 'Resolved' : 'Active'}
                        color={alert.is_resolved ? 'success' : 'warning'}
                        size="small"
                      />
                    </TableCell>
                    <TableCell>
                      {new Date(alert.created_at).toLocaleString()}
                    </TableCell>
                    <TableCell>
                      {!alert.is_resolved && (
                        <Button
                          size="small"
                          variant="outlined"
                          onClick={() => resolveAlert(alert.id)}
                        >
                          Resolve
                        </Button>
                      )}
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>
    </Box>
  );
}

export default Alerts; 