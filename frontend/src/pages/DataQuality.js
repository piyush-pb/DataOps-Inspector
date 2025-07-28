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
  CircularProgress,
  Alert,
  Chip,
} from '@mui/material';
import { CloudUpload as UploadIcon } from '@mui/icons-material';

function DataQuality() {
  const [dataSources, setDataSources] = useState([]);
  const [qualityChecks, setQualityChecks] = useState([]);
  const [summary, setSummary] = useState(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    fetchDataQualityData();
  }, []);

  const fetchDataQualityData = async () => {
    try {
      setLoading(true);
      
      // Fetch data sources
      const sourcesResponse = await fetch('/api/v1/data-quality/sources');
      const sourcesData = await sourcesResponse.json();
      setDataSources(sourcesData);
      
      // Fetch quality summary
      const summaryResponse = await fetch('/api/v1/data-quality/summary');
      const summaryData = await summaryResponse.json();
      setSummary(summaryData);
      
    } catch (err) {
      setError('Failed to load data quality data');
      console.error('Error fetching data quality data:', err);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('/api/v1/data-quality/upload', {
        method: 'POST',
        body: formData,
      });

      if (response.ok) {
        fetchDataQualityData(); // Refresh data
      } else {
        setError('Failed to upload file');
      }
    } catch (err) {
      setError('Error uploading file');
      console.error('Error uploading file:', err);
    }
  };

  const runQualityCheck = async (sourceId) => {
    try {
      const response = await fetch(`/api/v1/data-quality/sources/${sourceId}/check`, {
        method: 'POST',
      });

      if (response.ok) {
        const checks = await response.json();
        setQualityChecks(checks);
      }
    } catch (err) {
      console.error('Error running quality check:', err);
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
      <Box display="flex" justifyContent="space-between" alignItems="center" mb={3}>
        <Typography variant="h4">
          Data Quality Monitoring
        </Typography>
        <Button
          variant="contained"
          component="label"
          startIcon={<UploadIcon />}
          onChange={handleFileUpload}
        >
          Upload CSV
          <input type="file" hidden accept=".csv" />
        </Button>
      </Box>

      {/* Summary Cards */}
      <Grid container spacing={3} sx={{ mb: 4 }}>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Total Data Sources
              </Typography>
              <Typography variant="h4">
                {summary?.total_sources || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Average Quality Score
              </Typography>
              <Typography variant="h4">
                {summary?.average_quality_score ? (summary.average_quality_score * 100).toFixed(1) : 0}%
              </Typography>
            </CardContent>
          </Card>
        </Grid>
        <Grid item xs={12} sm={4}>
          <Card>
            <CardContent>
              <Typography color="textSecondary" gutterBottom>
                Issues Detected
              </Typography>
              <Typography variant="h4">
                {summary?.issues_count || 0}
              </Typography>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* Data Sources Table */}
      <Card sx={{ mb: 4 }}>
        <CardContent>
          <Typography variant="h6" gutterBottom>
            Data Sources
          </Typography>
          <TableContainer component={Paper}>
            <Table>
              <TableHead>
                <TableRow>
                  <TableCell>Name</TableCell>
                  <TableCell>Type</TableCell>
                  <TableCell>Created</TableCell>
                  <TableCell>Quality Score</TableCell>
                  <TableCell>Actions</TableCell>
                </TableRow>
              </TableHead>
              <TableBody>
                {dataSources.map((source) => (
                  <TableRow key={source.id}>
                    <TableCell>{source.name}</TableCell>
                    <TableCell>
                      <Chip label={source.source_type} size="small" />
                    </TableCell>
                    <TableCell>
                      {new Date(source.created_at).toLocaleDateString()}
                    </TableCell>
                    <TableCell>
                      {source.quality_score ? (source.quality_score * 100).toFixed(1) : 'N/A'}%
                    </TableCell>
                    <TableCell>
                      <Button
                        size="small"
                        variant="outlined"
                        onClick={() => runQualityCheck(source.id)}
                      >
                        Run Check
                      </Button>
                    </TableCell>
                  </TableRow>
                ))}
              </TableBody>
            </Table>
          </TableContainer>
        </CardContent>
      </Card>

      {/* Quality Checks Results */}
      {qualityChecks.length > 0 && (
        <Card>
          <CardContent>
            <Typography variant="h6" gutterBottom>
              Recent Quality Checks
            </Typography>
            <TableContainer component={Paper}>
              <Table>
                <TableHead>
                  <TableRow>
                    <TableCell>Check Type</TableCell>
                    <TableCell>Status</TableCell>
                    <TableCell>Score</TableCell>
                    <TableCell>Details</TableCell>
                    <TableCell>Timestamp</TableCell>
                  </TableRow>
                </TableHead>
                <TableBody>
                  {qualityChecks.map((check) => (
                    <TableRow key={check.id}>
                      <TableCell>{check.check_type}</TableCell>
                      <TableCell>
                        <Chip
                          label={check.status}
                          color={
                            check.status === 'passed' ? 'success' :
                            check.status === 'warning' ? 'warning' : 'error'
                          }
                          size="small"
                        />
                      </TableCell>
                      <TableCell>{(check.score * 100).toFixed(1)}%</TableCell>
                      <TableCell>{check.details}</TableCell>
                      <TableCell>
                        {new Date(check.created_at).toLocaleString()}
                      </TableCell>
                    </TableRow>
                  ))}
                </TableBody>
              </Table>
            </TableContainer>
          </CardContent>
        </Card>
      )}
    </Box>
  );
}

export default DataQuality; 