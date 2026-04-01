"""
Alert evaluation engine.
Evaluates configurable rules against data and produces alert instances.
"""

from dataclasses import dataclass
from datetime import datetime
from typing import Any, Dict, List, Optional
import yaml
import pandas as pd
from src.utils.logger import logger
from src.config import settings
from src.components.alert_block import AlertSeverity


@dataclass
class AlertRule:
    """
    Represents a single alert rule.
    """
    id: str
    title: str
    column: str
    condition: str  # 'gt', 'lt', 'eq'
    threshold: float
    severity: str
    message_template: str


class AlertEngine:
    """
    Engine for evaluating alert rules.
    """

    def __init__(self, rules_path: str = settings.ALERT_RULES_PATH):
        self.rules_path = rules_path
        self.rules: List[AlertRule] = []
        self._load_rules()

    def _load_rules(self) -> None:
        """
        Loads rules from a YAML file.
        """
        try:
            with open(self.rules_path, "r") as f:
                data = yaml.safe_load(f)
                for rule_data in data.get("rules", []):
                    self.rules.append(AlertRule(**rule_data))
            logger.info(f"Loaded {len(self.rules)} alert rules from {self.rules_path}")
        except Exception as e:
            logger.warning(f"Failed to load alert rules: {e}. Using default rules.")
            self._load_default_rules()

    def _load_default_rules(self) -> None:
        """
        Fallback to default rules if file is missing.
        """
        self.rules = [
            AlertRule(
                id="high-derogation",
                title="High Derogation Warning",
                column="derogation_pct",
                condition="gt",
                threshold=15.0,
                severity="warning",
                message_template="Average derogation percentage is high: {value:.1f}%",
            ),
            AlertRule(
                id="failed-calls-danger",
                title="Critical Failed Calls",
                column="failed_calls",
                condition="gt",
                threshold=100,
                severity="danger",
                message_template="System detected {value} failed calls in the current selection.",
            ),
        ]

    def evaluate(self, metrics: Dict[str, Any]) -> List[Dict[str, Any]]:
        """
        Evaluates metrics against rules.

        Args:
            metrics: Dictionary of current metric values.

        Returns:
            List[Dict[str, Any]]: List of triggered alerts.
        """
        triggered_alerts = []

        for rule in self.rules:
            value = metrics.get(rule.column)
            if value is None:
                continue

            triggered = False
            if rule.condition == "gt" and value > rule.threshold:
                triggered = True
            elif rule.condition == "lt" and value < rule.threshold:
                triggered = True
            elif rule.condition == "eq" and value == rule.threshold:
                triggered = True

            if triggered:
                triggered_alerts.append({
                    "id": rule.id,
                    "title": rule.title,
                    "severity": AlertSeverity(rule.severity),
                    "message": rule.message_template.format(value=value),
                    "timestamp": datetime.now(),
                })

        return triggered_alerts


# Global alert engine instance
alert_engine = AlertEngine()
