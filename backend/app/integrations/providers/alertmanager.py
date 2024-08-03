from app.integrations.providers.base import BaseIntegration
from app.schemas.alert import AlertSchema, AlertSource, AlertStatus, SeverityLevel
from datetime import datetime

class AlertmanagerIntegration(BaseIntegration):
    """
    Handle Prometheus Alertmanager alerts.
    For now it does nothing, will be implemented in upcoming commits.
    """

    SEVERITY_MAP = {
        "critical": SeverityLevel.CRITICAL,
        "high": SeverityLevel.HIGH,
        "medium": SeverityLevel.MEDIUM,
        "low": SeverityLevel.LOW,
    }
    STATUS_MAP = {
        "firing": AlertStatus.OPEN,
        "resolved": AlertStatus.RESOLVED,
    }

    def normalize_alert(self, alert: dict) -> AlertSchema:
        '''
        Normalize Alertmanager alert to AlertSchema format.
        Args:
            alert (dict): Raw alert data from Alertmanager.
        Returns:
            AlertSchema: Normalized alert object.
        '''
        labels = alert.get("labels", {})
        annotations = alert.get("annotations", {})
        severity = self.SEVERITY_MAP.get(labels.get("severity", "low").lower(), SeverityLevel.LOW)
        status = self.STATUS_MAP.get(alert.get("status", "firing").lower(), AlertStatus.OPEN)
        created_at = datetime.strptime(alert["startsAt"], "%Y-%m-%dT%H:%M:%S.%fZ")
        normalized_alert = AlertSchema(
            title=annotations.get("summary", "No title"),
            description=annotations.get("description", "No description"),
            severity=severity,
            status=status,
            alert_source=AlertSource.ALERTMANAGER,
            tags=labels,
            service=labels.get("service"),
            env=labels.get("env"),
            additional_data=annotations,
            provider_event_id=alert.get("fingerprint"),
            provider_aggregation_key=alert.get("groupKey"),
            provider_cycle_key=alert.get("generatorURL"),
            configuration_id=labels.get("alertname"),
            host=labels.get("instance"),
            created_at=created_at.isoformat(),
            duration_seconds=None,  # Duration can be calculated if needed
        )
        return normalized_alert

    def get_alerts(self):
        # Implement logic to fetch alerts
        pass
