"""Pydantic Schemas for the alert model.""" ""

import enum
from datetime import datetime
from typing import Optional, Union

from pydantic import BaseModel, ConfigDict


class SeverityLevel(str, enum.Enum):
    """Severity levels for the alert."""

    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    CRITICAL = "critical"


class AlertSource(str, enum.Enum):
    """Source of the alert."""

    DATADOG = "Datadog"
    ALERTMANAGER = "Alertmanager"


class AlertStatus(str, enum.Enum):
    """Status of the alert."""

    OPEN = "open"
    RESOLVED = "resolved"
    ACKNOWLEDGED = "acknowledged"
    SUPPRESSED = "suppressed"


class AlertConfigurationSchema(BaseModel):
    """Schema for alert configuration.

    Alert configurations are analogous to Datadog's Monitors.
    """

    name: str
    description: Optional[str] = None
    query: str
    provider: AlertSource
    provider_id: str
    is_noisy: bool = False
    noisy_reason: Optional[str] = None


class AlertSchema(BaseModel):
    """Schema for alert data.

    An Alert is a normalized representation of an alert from various monitoring systems.
    """

    title: str
    description: str
    severity: SeverityLevel
    status: AlertStatus
    alert_source: AlertSource
    tags: dict = {}
    service: Optional[str] = None
    env: Optional[str] = None
    additional_data: dict = {}
    provider_event_id: str
    provider_aggregation_key: Optional[str] = None
    provider_cycle_key: Optional[str] = None
    configuration_id: Optional[str] = None
    host: Optional[str] = None
    created_at: Optional[Union[str, datetime]] = None
    duration_seconds: Optional[int] = None

    model_config = ConfigDict(from_attributes=True)

    @classmethod
    def model_validate(cls, obj, *args, **kwargs):
        if (
            isinstance(obj, dict)
            and "created_at" in obj
            and isinstance(obj["created_at"], datetime)
        ):
            obj["created_at"] = obj["created_at"].isoformat()
        return super().model_validate(obj, *args, **kwargs)
