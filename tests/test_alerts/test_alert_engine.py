"""
Tests for the alert_engine module.
"""

import pytest
from src.alerts.alert_engine import AlertEngine, AlertRule
from src.components.alert_block import AlertSeverity
from unittest.mock import patch
import yaml


@pytest.fixture
def mock_alert_rules_file(tmp_path):
    """
    Creates a temporary alert_rules.yaml file for testing.
    """
    rules_content = """
rules:
  - id: test-high-value
    title: High Value Alert
    column: test_metric
    condition: gt
    threshold: 100
    severity: danger
    message_template: "Test metric is high: {value}"
  - id: test-low-value
    title: Low Value Alert
    column: another_metric
    condition: lt
    threshold: 10
    severity: warning
    message_template: "Another metric is low: {value}"
"""
    file_path = tmp_path / "alert_rules.yaml"
    file_path.write_text(rules_content)
    return str(file_path)


def test_alert_engine_loads_rules(mock_alert_rules_file):
    """
    Tests that the AlertEngine loads rules from a file.
    """
    engine = AlertEngine(rules_path=mock_alert_rules_file)
    assert len(engine.rules) == 2
    assert engine.rules[0].id == "test-high-value"
    assert engine.rules[1].condition == "lt"


def test_alert_engine_evaluates_high_value(mock_alert_rules_file):
    """
    Tests alert evaluation for a high value condition.
    """
    engine = AlertEngine(rules_path=mock_alert_rules_file)
    metrics = {"test_metric": 150, "another_metric": 50}
    alerts = engine.evaluate(metrics)
    
    assert len(alerts) == 1
    assert alerts[0]["id"] == "test-high-value"
    assert alerts[0]["severity"] == AlertSeverity.DANGER
    assert "150" in alerts[0]["message"]


def test_alert_engine_evaluates_low_value(mock_alert_rules_file):
    """
    Tests alert evaluation for a low value condition.
    """
    engine = AlertEngine(rules_path=mock_alert_rules_file)
    metrics = {"test_metric": 50, "another_metric": 5}
    alerts = engine.evaluate(metrics)
    
    assert len(alerts) == 1
    assert alerts[0]["id"] == "test-low-value"
    assert alerts[0]["severity"] == AlertSeverity.WARNING
    assert "5" in alerts[0]["message"]


def test_alert_engine_no_alerts_triggered(mock_alert_rules_file):
    """
    Tests when no alerts are triggered.
    """
    engine = AlertEngine(rules_path=mock_alert_rules_file)
    metrics = {"test_metric": 50, "another_metric": 50}
    alerts = engine.evaluate(metrics)
    assert len(alerts) == 0


def test_alert_engine_missing_metric(mock_alert_rules_file):
    """
    Tests alert engine with a missing metric.
    """
    engine = AlertEngine(rules_path=mock_alert_rules_file)
    metrics = {"another_metric": 5} # test_metric is missing
    alerts = engine.evaluate(metrics)
    
    assert len(alerts) == 1
    assert alerts[0]["id"] == "test-low-value"
