import React, { useState, useEffect } from 'react';
import {
  Box,
  Typography,
  Grid,
  Card,
  CardContent,
  Button,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Alert,
  Chip,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  Snackbar,
} from '@mui/material';
import { Add as AddIcon } from '@mui/icons-material';
import LoadingSpinner from '../components/LoadingSpinner';

function ModelMonitoring() {
  const [models, setModels] = useState([]);
  const [drift, setDrift] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [deployDialogOpen, setDeployDialogOpen] = useState(false);
  const [newModelName, setNewModelName] = useState('');
  const [snackbar, setSnackbar] = useState({ open: false, message: '', severity: 'success' });

  useEffect(() => {
    fetchModelData();
  }, []);

  const fetchModelData = async () => {
    try {
      setLoading(true);
      
      // Fetch deployed models
      const modelsResponse = await fetch('/api/v1/model-monitoring/models');
      const modelsData = await modelsResponse.json();
      setModels(modelsData);
      
      // Fetch model summary
      const summaryResponse = await fetch('/api/v1/model-monitoring/summary');
      const summaryData = await summaryResponse.json();
      setSummary(summaryData);
      
    } catch (err) {
      setError('Failed to load model monitoring data');
      console.error('Error fetching model data:', err);
    } finally {
      setLoading(false);
    }
  };

  const deployModel = async () => {
    try {
      const response = await fetch('/api/v1/model-monitoring/deploy', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          model_name: newModelName,
          model_type: 'classification',
        }),
      });

      if (response.ok) {
        setDeployDialogOpen(false);
        setNewModelName('');
        fetchModelData();
        setSnackbar({ open: true, message: 'Model deployed successfully!', severity: 'success' });
      } else {
        setSnackbar({ open: true, message: 'Failed to deploy model', severity: 'error' });
      }
    } catch (err) {
      console.error('Error deploying model:', err);
      setSnackbar({ open: true, message: 'Error deploying model', severity: 'error' });
    }
  };

  const checkDrift = async (modelName) => {
    try {
      const response = await fetch(`/api/v1/model-monitoring/models/${modelName}/drift-check`, {
        method: 'POST',
      });

      if (response.ok) {
        const driftData = await response.json();
        setDrift(driftData);
        setSnackbar({ open: true, message: 'Drift check completed', severity: 'success' });
      } else {
        setSnackbar({ open: true, message: 'Failed to check drift', severity: 'error' });
      }
    } catch (err) {
      console.error('Error checking drift:', err);
      setSnackbar({ open: true, message: 'Error checking drift', severity: 'error' });
    }
  };

  if (loading) {
    return <LoadingSpinner message="Loading model monitoring data..." />;
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
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          Model Monitoring
        </Typography>
        <Button
          variant="contained"
          startIcon={<AddIcon />}
          onClick={() => setDeployDialogOpen(true)}
        >
          Deploy Model
        </Button>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Models
              </Typography>
              <Typography variant="h4">
                {summary?.total_models || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Average Accuracy
              </Typography>
              <Typography variant="h4">
                {summary?.average_accuracy ? (summary.average_accuracy * 100).toFixed(1) : 0}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Drift Alerts
              </Typography>
              <Typography variant="h4">
                {summary?.drift_alerts || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Models Table */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Deployed Models
          </Typography>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Model Name</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Version</TableCell>
                  <TableCell>Status</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {models.map((model, index) => (
                  <TableRow key={index}>
                    <TableCell>{model}</TableCell>
                    <TableCell>
                      <Chip label="Classification" size="small" />
                    </TableCell>
                    <TableCell>1.0</TableCell>
                    <TableCell>
                      <Chip label="Active" color="success" size="small" />
                    </TableCell>
                    <TableCell>
                      <Button
                        size="small"
                        variant="outlined"
                        onClick={() => checkDrift(model)}
                        sx={{ mr: 1 }}
                      >
                        Check Drift
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Drift Results */}
      {drift.length > 0 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Drift Detection Results
            </Typography>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Drift Type</TableCell>
                    <TableCell>Feature</TableCell>
                    <TableCell>Drift Score</TableCell>
                    <TableCell>Threshold</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Timestamp</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {drift.map((driftItem) => (
                    <TableRow key={driftItem.id}>
                      <TableCell>{driftItem.drift_type}</TableCell>
                      <TableCell>{driftItem.feature_name || 'N/A'}</TableCell>
                      <TableCell>{driftItem.drift_score.toFixed(3)}</TableCell>
                      <TableCell>{driftItem.threshold.toFixed(3)}</TableCell>
                      <TableCell>
                        <Chip
                          label={driftItem.is_drift_detected ? 'Drift Detected' : 'No Drift'}
                          color={driftItem.is_drift_detected ? 'error' : 'success'}
                          size="small"
                        />
                      </TableCell>
                      <TableCell>
                        {new Date(driftItem.timestamp).toLocaleString()}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      )}

      {/* Deploy Model Dialog */}
      <Dialog open={deployDialogOpen} onClose={() => setDeployDialogOpen(false)}>
        <DialogTitle>Deploy New Model</DialogTitle>
        <DialogContent>
          <TextField
            autoFocus
            margin="dense"
            label="Model Name"
            fullWidth
            variant="outlined"
            value={newModelName}
            onChange={(e) => setNewModelName(e.target.value)}
            aria-label="Model name input"
          />
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeployDialogOpen(false)}>Cancel</Button>
          <Button onClick={deployModel} variant="contained">
            Deploy
          </Button>
        </DialogActions>
      </Dialog>

      {/* Snackbar for notifications */}
      <Snackbar
        open={snackbar.open}
        autoHideDuration={6000}
        onClose={() => setSnackbar({ ...snackbar, open: false })}
        anchorOrigin={{ vertical: 'bottom', horizontal: 'right' }}
      >
        <Alert 
          onClose={() => setSnackbar({ ...snackbar, open: false })} 
          severity={snackbar.severity}
          sx={{ width: '100%' }}
        >
          {snackbar.message}
        </Alert>
      </Snackbar>
    </Box>
  );
}



export default ModelMonitoring; 