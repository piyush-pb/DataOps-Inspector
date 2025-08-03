import React, { useState, useEffect } from 'react';
import { Routes, Route } from 'react-router-dom';
import { Box, Container } from '@mui/material';
import { styled } from '@mui/material/styles';

import Header from './components/Header';
import Sidebar from './components/Sidebar';
import Dashboard from './pages/Dashboard';
import DataQuality from './pages/DataQuality';
import ModelMonitoring from './pages/ModelMonitoring';
import Alerts from './pages/Alerts';
import Settings from './pages/Settings';
import RetoolDashboard from './components/RetoolDashboard';

const drawerWidth = 240;

const Main = styled('main', { shouldForwardProp: (prop) => prop !== 'open' })(
  ({ theme, open }) => ({
    flexGrow: 1,
    padding: theme.spacing(3),
    transition: theme.transitions.create('margin', {
      easing: theme.transitions.easing.sharp,
      duration: theme.transitions.duration.leavingScreen,
    }),
    marginLeft: `-${drawerWidth}px`,
    ...(open && {
      transition: theme.transitions.create('margin', {
        easing: theme.transitions.easing.easeOut,
        duration: theme.transitions.duration.enteringScreen,
      }),
      marginLeft: 0,
    }),
  }),
);

const DrawerHeader = styled('div')(({ theme }) => ({
  display: 'flex',
  alignItems: 'center',
  padding: theme.spacing(0, 1),
  ...theme.mixins.toolbar,
  justifyContent: 'flex-end',
}));

function App() {
  const [open, setOpen] = useState(true);
  const [systemStatus, setSystemStatus] = useState('loading');

  useEffect(() => {
    // Check system status on app load
    checkSystemStatus();
  }, []);

  const checkSystemStatus = async () => {
    try {
      const response = await fetch('/api/v1/dashboard/system-status');
      const data = await response.json();
      // Fix: Access the correct nested structure
      setSystemStatus(data.data?.overall_status || 'operational');
    } catch (error) {
      console.error('Error checking system status:', error);
      setSystemStatus('error');
    }
  };

  const handleDrawerToggle = () => {
    setOpen(!open);
  };

  return (
    <Box sx={{ display: 'flex' }}>
      <Header open={open} onDrawerToggle={handleDrawerToggle} systemStatus={systemStatus} />
      <Sidebar open={open} onDrawerToggle={handleDrawerToggle} />
      
      <Main open={open}>
        <DrawerHeader />
        <Container maxWidth="xl">
          <Routes>
            <Route path="/" element={<Dashboard />} />
            <Route path="/data-quality" element={<DataQuality />} />
            <Route path="/model-monitoring" element={<ModelMonitoring />} />
            <Route path="/alerts" element={<Alerts />} />
            <Route path="/settings" element={<Settings />} />
            <Route path="/retool-dashboard" element={<RetoolDashboard />} />
          </Routes>
        </Container>
      </Main>
    </Box>
  );
}

export default App; 