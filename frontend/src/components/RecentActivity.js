import React from 'react';
import PropTypes from 'prop-types';
import {
  Card,
  CardContent,
  Typography,
  List,
  ListItem,
  ListItemText,
  ListItemIcon,
  Chip,
  Box,
} from '@mui/material';
import {
  DataUsage as DataQualityIcon,
  Psychology as ModelIcon,
  Notifications as AlertIcon,
} from '@mui/icons-material';

function RecentActivity({ activities }) {
  const getActivityIcon = (type, status) => {
    switch (type) {
      case 'data_quality':
        return <DataQualityIcon />;
      case 'model_performance':
        return <ModelIcon />;
      case 'alert':
        return <AlertIcon />;
      default:
        return <DataQualityIcon />;
    }
  };

  const getStatusColor = (status) => {
    switch (status) {
      case 'passed':
      case 'success':
        return 'success';
      case 'warning':
        return 'warning';
      case 'failed':
      case 'critical':
        return 'error';
      default:
        return 'default';
    }
  };

  const formatTimestamp = (timestamp) => {
    const date = new Date(timestamp);
    return date.toLocaleString();
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom id="recent-activity-title">
          Recent Activity
        </Typography>
        <List aria-labelledby="recent-activity-title">
          {activities.map((activity, index) => (
            <ListItem 
              key={index} 
              divider={index < activities.length - 1}
              aria-label={`Activity ${index + 1}: ${activity.title}`}
            >
              <ListItemIcon>
                {getActivityIcon(activity.type, activity.status)}
              </ListItemIcon>
              <ListItemText
                primary={
                  <Box display="flex" alignItems="center" gap={1}>
                    <Typography variant="body1">
                      {activity.title}
                    </Typography>
                    <Chip
                      label={activity.status}
                      color={getStatusColor(activity.status)}
                      size="small"
                      aria-label={`Status: ${activity.status}`}
                    />
                  </Box>
                }
                secondary={
                  <Box>
                    <Typography variant="body2" color="textSecondary">
                      {activity.description}
                    </Typography>
                    <Typography variant="caption" color="textSecondary">
                      {formatTimestamp(activity.timestamp)}
                    </Typography>
                  </Box>
                }
              />
            </ListItem>
          ))}
        </List>
      </CardContent>
    </Card>
  );
}

RecentActivity.propTypes = {
  activities: PropTypes.arrayOf(
    PropTypes.shape({
      type: PropTypes.oneOf(['data_quality', 'model_performance', 'alert']).isRequired,
      status: PropTypes.string.isRequired,
      title: PropTypes.string.isRequired,
      description: PropTypes.string.isRequired,
      timestamp: PropTypes.string.isRequired,
    })
  ).isRequired,
};

export default RecentActivity; 