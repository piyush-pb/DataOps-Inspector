import React from 'react';
import {
  AppBar,
  Toolbar,
  Typography,
  IconButton,
  Badge,
  Box,
  Chip,
} from '@mui/material';
import {
  Menu as MenuIcon,
  Notifications as NotificationsIcon,
  CheckCircle as CheckCircleIcon,
  Warning as WarningIcon,
  Error as ErrorIcon,
} from '@mui/icons-material';
import { styled } from '@mui/material/styles';

const drawerWidth = 240;

const StyledAppBar = styled(AppBar, {
  shouldForwardProp: (prop) => prop !== 'open',
})(({ theme, open }) => ({
  transition: theme.transitions.create(['margin', 'width'], {
    easing: theme.transitions.easing.sharp,
    duration: theme.transitions.duration.leavingScreen,
  }),
  ...(open && {
    width: `calc(100% - ${drawerWidth}px)`,
    marginLeft: `${drawerWidth}px`,
    transition: theme.transitions.create(['margin', 'width'], {
      easing: theme.transitions.easing.easeOut,
      duration: theme.transitions.duration.enteringScreen,
    }),
  }),
}));

const getStatusIcon = (status) => {
  switch (status) {
    case 'operational':
    case 'healthy':
      return <CheckCircleIcon sx={{ color: 'success.main' }} />;
    case 'warning':
      return <WarningIcon sx={{ color: 'warning.main' }} />;
    case 'critical':
    case 'error':
      return <ErrorIcon sx={{ color: 'error.main' }} />;
    case 'loading':
      return <CheckCircleIcon sx={{ color: 'grey.500' }} />;
    default:
      return <CheckCircleIcon sx={{ color: 'grey.500' }} />;
  }
};

const getStatusColor = (status) => {
  switch (status) {
    case 'operational':
    case 'healthy':
      return 'success';
    case 'warning':
      return 'warning';
    case 'critical':
    case 'error':
      return 'error';
    case 'loading':
      return 'default';
    default:
      return 'default';
  }
};

function Header({ open, onDrawerToggle, systemStatus }) {
  const displayStatus = systemStatus || 'operational';
  
  return (
    <StyledAppBar position="fixed" open={open}>
      <Toolbar>
        <IconButton
          color="inherit"
          aria-label="open drawer"
          onClick={onDrawerToggle}
          edge="start"
          sx={{ mr: 2, ...(open && { display: 'none' }) }}
        >
          <MenuIcon />
        </IconButton>
        
        <Typography variant="h6" noWrap component="div" sx={{ flexGrow: 1 }}>
          DataOps Inspector
        </Typography>
        
        <Box sx={{ display: 'flex', alignItems: 'center', gap: 2 }}>
          <Chip
            icon={getStatusIcon(displayStatus)}
            label={`System: ${displayStatus}`}
            color={getStatusColor(displayStatus)}
            variant="outlined"
            size="small"
          />
          
          <IconButton color="inherit">
            <Badge badgeContent={4} color="error">
              <NotificationsIcon />
            </Badge>
          </IconButton>
        </Box>
      </Toolbar>
    </StyledAppBar>
  );
}

export default Header; 