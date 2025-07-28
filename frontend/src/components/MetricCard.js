import React from 'react';
import PropTypes from 'prop-types';
import { Card, CardContent, Typography, Box } from '@mui/material';

function MetricCard({ title, value, icon, color = 'primary', unit = '', formatValue }) {
  const displayValue = formatValue ? formatValue(value) : value;
  
  return (
    <Card sx={{ height: '100%' }} aria-label={`Metric card for ${title}`}>
      <CardContent>
        <Box display="flex" alignItems="center" justifyContent="space-between">
          <Box>
            <Typography color="textSecondary" gutterBottom variant="body2">
              {title}
            </Typography>
            <Typography variant="h4" component="div" color={color} aria-label={`Value: ${displayValue}${unit}`}>
              {displayValue}{unit}
            </Typography>
          </Box>
          <Box color={color} aria-hidden="true">
            {icon}
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
}

MetricCard.propTypes = {
  title: PropTypes.string.isRequired,
  value: PropTypes.oneOfType([PropTypes.string, PropTypes.number]).isRequired,
  icon: PropTypes.node,
  color: PropTypes.string,
  unit: PropTypes.string,
  formatValue: PropTypes.func,
};

MetricCard.defaultProps = {
  color: 'primary',
  unit: '',
};

export default MetricCard; 