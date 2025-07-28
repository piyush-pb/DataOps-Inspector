import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from typing import Optional
import os

from app.core.config import settings
from app.models.alerts import Alert

class AlertService:
    """Service for managing alerts and notifications"""
    
    def __init__(self):
        self.smtp_host = settings.SMTP_HOST
        self.smtp_port = settings.SMTP_PORT
        self.smtp_user = settings.SMTP_USER
        self.smtp_password = settings.SMTP_PASSWORD
        self.smtp_use_tls = settings.SMTP_USE_TLS
    
    def send_notification(self, alert: Alert) -> bool:
        """Send notification for an alert"""
        try:
            # Send email notification
            if self.smtp_user and self.smtp_password:
                self._send_email_notification(alert)
            
            # Log notification (in production, you might also send to Slack, etc.)
            print(f"Alert notification sent: {alert.title} - {alert.severity}")
            
            return True
        except Exception as e:
            print(f"Error sending notification: {e}")
            return False
    
    def _send_email_notification(self, alert: Alert) -> None:
        """Send email notification for an alert"""
        if not all([self.smtp_host, self.smtp_user, self.smtp_password]):
            print("SMTP configuration incomplete, skipping email notification")
            return
        
        # Create message
        msg = MIMEMultipart()
        msg['From'] = self.smtp_user
        msg['To'] = ", ".join(settings.ALERT_EMAIL_RECIPIENTS)
        msg['Subject'] = f"[{alert.severity.upper()}] {alert.title}"
        
        # Create email body
        body = f"""
        Alert Details:
        --------------
        Type: {alert.alert_type}
        Severity: {alert.severity}
        Source: {alert.source or 'Unknown'}
        Time: {alert.created_at}
        
        Message:
        {alert.message}
        
        ---
        This is an automated alert from DataOps Inspector.
        """
        
        msg.attach(MIMEText(body, 'plain'))
        
        # Send email
        with smtplib.SMTP(self.smtp_host, self.smtp_port) as server:
            if self.smtp_use_tls:
                server.starttls()
            server.login(self.smtp_user, self.smtp_password)
            server.send_message(msg)
    
    def create_data_quality_alert(self, source_name: str, issue_type: str, details: str, severity: str = "medium") -> Alert:
        """Create a data quality alert"""
        alert = Alert(
            alert_type="data_quality",
            severity=severity,
            title=f"Data Quality Issue: {issue_type}",
            message=f"Data quality issue detected in {source_name}: {details}",
            source=source_name,
            metadata={"issue_type": issue_type}
        )
        return alert
    
    def create_model_drift_alert(self, model_name: str, drift_type: str, drift_score: float, threshold: float) -> Alert:
        """Create a model drift alert"""
        severity = "high" if drift_score > threshold * 1.5 else "medium"
        
        alert = Alert(
            alert_type="model_drift",
            severity=severity,
            title=f"Model Drift Detected: {drift_type}",
            message=f"Model drift detected in {model_name}. Drift score: {drift_score:.3f} (threshold: {threshold:.3f})",
            source=model_name,
            metadata={
                "drift_type": drift_type,
                "drift_score": drift_score,
                "threshold": threshold
            }
        )
        return alert
    
    def create_system_alert(self, title: str, message: str, severity: str = "medium") -> Alert:
        """Create a system alert"""
        alert = Alert(
            alert_type="system",
            severity=severity,
            title=title,
            message=message,
            source="system",
            metadata={"system_alert": True}
        )
        return alert 