import React from 'react';
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  TextField,
  Button,
  Switch,
  FormControlLabel,
  Divider,
} from '@mui/material';

function Settings() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>

      <Grid container spacing={3}>
        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Email Notifications
              </Typography>
              <TextField
                fullWidth
                label="SMTP Host"
                defaultValue="smtp.gmail.com"
                margin="normal"
              />
              <TextField
                fullWidth
                label="SMTP Port"
                defaultValue="587"
                margin="normal"
              />
              <TextField
                fullWidth
                label="Email"
                defaultValue="your-email@gmail.com"
                margin="normal"
              />
              <TextField
                fullWidth
                label="Password"
                type="password"
                margin="normal"
              />
              <FormControlLabel
                control={<Switch defaultChecked />}
                label="Enable Email Notifications"
                sx={{ mt: 2 }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12} md={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Alert Thresholds
              </Typography>
              <TextField
                fullWidth
                label="Data Quality Threshold (%)"
                defaultValue="80"
                margin="normal"
              />
              <TextField
                fullWidth
                label="Model Drift Threshold"
                defaultValue="0.2"
                margin="normal"
              />
              <TextField
                fullWidth
                label="Performance Threshold (%)"
                defaultValue="85"
                margin="normal"
              />
              <FormControlLabel
                control={<Switch defaultChecked />}
                label="Enable Real-time Monitoring"
                sx={{ mt: 2 }}
              />
            </CardContent>
          </Card>
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                System Configuration
              </Typography>
              <Grid container spacing={2}>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="Database URL"
                    defaultValue="postgresql://dataops_user:dataops_password@localhost:5432/dataops_db"
                    margin="normal"
                  />
                </Grid>
                <Grid item xs={12} sm={6}>
                  <TextField
                    fullWidth
                    label="API Base URL"
                    defaultValue="http://localhost:8000"
                    margin="normal"
                  />
                </Grid>
              </Grid>
              <Divider sx={{ my: 2 }} />
              <Box display="flex" gap={2}>
                <Button variant="contained" color="primary">
                  Save Settings
                </Button>
                <Button variant="outlined">
                  Reset to Defaults
                </Button>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  );
}

export default Settings; 