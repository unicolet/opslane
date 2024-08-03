from app.integrations.providers.base import BaseIntegration
from app.schemas.alert import AlertSchema, AlertSource
class AlertmanagerIntegration(BaseIntegration):
    """
    Handle Prometheus Alertmanager alerts.
    For now it does nothing, will be implemented in upcoming commits.
    """
    def normalize_alert(self, alert: dict) -> AlertSchema:
        # Implement normalization logic
        pass
    def get_alerts(self):
        # Implement logic to fetch alerts
        pass
