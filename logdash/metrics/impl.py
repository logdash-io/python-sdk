import requests

from logdash.metrics.base import BaseMetrics
from logdash.constants import MetricOperation
from logdash.internal import internal_logger


class Metrics(BaseMetrics):
    def __init__(self, api_key: str, host: str, verbose: bool = False):
        self.api_key = api_key
        self.host = host
        self.verbose = verbose

    def set(self, name: str, value: float) -> None:
        """
        Set a metric to an absolute value.
        
        Args:
            name: The metric name
            value: The value to set
        """
        if self.verbose:
            internal_logger.verbose(f"Setting metric {name} to {value}")

        self._send_metric(name, value, MetricOperation.SET)

    def mutate(self, name: str, value: float) -> None:
        """
        Change a metric by a relative value.
        
        Args:
            name: The metric name
            value: The amount to change by
        """
        if self.verbose:
            internal_logger.verbose(f"Mutating metric {name} by {value}")

        self._send_metric(name, value, MetricOperation.CHANGE)
        
    def _send_metric(self, name: str, value: float, operation: MetricOperation) -> None:
        # Skip if no API key is provided
        if not self.api_key:
            return
            
        try:
            requests.put(
                f"{self.host}/metrics",
                headers={
                    "Content-Type": "application/json",
                    "project-api-key": self.api_key,
                },
                json={
                    "name": name,
                    "value": value,
                    "operation": operation,
                },
                timeout=5,  # Add timeout to prevent blocking
            )
        except requests.RequestException:
            # Silently fail for now - future: add retry queue
            pass 