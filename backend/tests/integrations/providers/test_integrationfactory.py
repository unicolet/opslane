import pytest
from app.integrations.providers.factory import IntegrationSourceFactory
from app.integrations.providers.datadog import DatadogIntegration
from app.integrations.providers.alertmanager import AlertmanagerIntegration
from app.schemas.alert import AlertSource

def test_get_integration_datadog():
    integration = IntegrationSourceFactory.get_integration(AlertSource.DATADOG.value)
    assert isinstance(integration, DatadogIntegration)
def test_get_integration_alertmanager():
    integration = IntegrationSourceFactory.get_integration(AlertSource.ALERTMANAGER.value)
    assert isinstance(integration, AlertmanagerIntegration)
def test_get_integration_invalid_source():
    with pytest.raises(ValueError):
        IntegrationSourceFactory.get_integration("InvalidSource")