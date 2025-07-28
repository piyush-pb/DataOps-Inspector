import React from 'react';
import PropTypes from 'prop-types';
import {
  Box,
  CircularProgress,
  Typography,
} from '@mui/material';

function LoadingSpinner({ message = 'Loading...', size = 'large' }) {
  return (
    <Box 
      display="flex" 
      flexDirection="column"
      justifyContent="center" 
      alignItems="center" 
      minHeight="400px"
      gap={2}
    >
      <CircularProgress size={size === 'large' ? 60 : 40} />
      <Typography variant="body1" color="textSecondary">
        {message}
      </Typography>
    </Box>
  );
}

LoadingSpinner.propTypes = {
  message: PropTypes.string,
  size: PropTypes.oneOf(['small', 'large']),
};

export default LoadingSpinner; 