"""
Tests for the generic alert_block component.
"""

from datetime import datetime
from dash_bootstrap_components import Alert
from src.components.alert_block import create_alert_block, AlertSeverity


def test_create_info_alert():
    """
    Tests the creation of an info alert.
    """
    alert_id = "test-info"
    title = "Info Alert"
    message = "This is an informational message."
    timestamp = datetime.now()
    component = create_alert_block(alert_id, title, AlertSeverity.INFO, message, timestamp)

    assert isinstance(component, Alert)
    assert "Info Alert" in str(component)
    assert "informational message" in str(component)
    assert component.color == "info"
    assert component.dismissable is True


def test_create_danger_alert():
    """
    Tests the creation of a danger alert.
    """
    alert_id = "test-danger"
    title = "Critical Alert"
    message = "Something went wrong!"
    component = create_alert_block(alert_id, title, AlertSeverity.DANGER, message, dismissable=False)

    assert isinstance(component, Alert)
    assert "Critical Alert" in str(component)
    assert "Something went wrong!" in str(component)
    assert component.color == "danger"
    assert component.dismissable is False
