import pytest
from app.integrations.providers.alertmanager import AlertmanagerIntegration
from app.schemas.alert import AlertSchema, AlertSource, AlertStatus, SeverityLevel

@pytest.fixture
def alertmanager_integration():
    return AlertmanagerIntegration()

def test_normalize_alert(alertmanager_integration):
    raw_alert = {
        "version": "4",
        "groupKey": "12345",
        "truncatedAlerts": 0,
        "status": "firing",
        "receiver": "webhook",
        "groupLabels": {"alertname": "TestAlert"},
        "commonLabels": {"severity": "critical", "service": "test-service", "env": "production"},
        "commonAnnotations": {"summary": "Test summary", "description": "Test description"},
        "externalURL": "http://alertmanager.example.com",
        "alerts": [
            {
                "status": "firing",
                "labels": {"severity": "critical", "service": "test-service", "env": "production"},
                "annotations": {"summary": "Test summary", "description": "Test description"},
                "startsAt": "2024-08-03T15:19:29.918800Z",
                "endsAt": "2024-08-03T16:19:29.918800Z",
                "generatorURL": "http://example.com",
                "fingerprint": "abc123"
            }
        ]
    }

    expected_alert = AlertSchema(
        title="Test summary",
        description="Test description",
        severity=SeverityLevel.CRITICAL,
        status=AlertStatus.OPEN,
        alert_source=AlertSource.ALERTMANAGER,
        tags={"severity": "critical", "service": "test-service", "env": "production"},
        service="test-service",
        env="production",
        additional_data={"summary": "Test summary", "description": "Test description"},
        provider_event_id="abc123",
        provider_aggregation_key="12345",
        provider_cycle_key="http://example.com",
        configuration_id="TestAlert",
        host=None,
        created_at="2024-08-03T15:19:29.918800",
        duration_seconds=None
    )

    normalized_alert = alertmanager_integration.normalize_alert(raw_alert["alerts"][0])

    assert normalized_alert == expected_alert

