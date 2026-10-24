import math
import os
import threading
from typing import Callable, Dict, Optional, Tuple

import requests

from logdash.metrics.base import BaseMetrics
from logdash.constants import MetricOperation
from logdash.internal import internal_logger


class Metrics(BaseMetrics):
    def __init__(self, api_key: str, host: str, verbose: bool = False, app: Optional[str] = None, *, send_in_background: Callable[..., bool]):
        self.api_key = api_key
        self.host = host
        self.verbose = verbose
        self.app = app
        self._send_in_background = send_in_background
        self._reset()

    def set(self, name: str, value: float) -> None:
        """
        Set a metric to an absolute value.

        Args:
            name: The metric name
            value: The value to set
        """
        if self.verbose:
            internal_logger.verbose(f"Setting metric {name} to {value}")

        self._queue(name, value, MetricOperation.SET)

    def mutate(self, name: str, value: float) -> None:
        """
        Change a metric by a relative value.

        Args:
            name: The metric name
            value: The amount to change by
        """
        if self.verbose:
            internal_logger.verbose(f"Mutating metric {name} by {value}")

        self._queue(name, value, MetricOperation.CHANGE)

    def _reset(self) -> None:
        self._pid = os.getpid()
        # One operation per metric not sent yet, merged the way the server merges them
        self._pending: Dict[str, Tuple[float, MetricOperation]] = {}
        self._lock = threading.Lock()
        # A sender is started and has not taken the pending operations yet
        self._waiting = False
        # One batch on the wire at a time, so the server gets each metric's operations in order
        self._send_lock = threading.Lock()

    def _queue(self, name: str, value: float, operation: MetricOperation) -> None:
        try:
            value = float(value)
        except (TypeError, ValueError, OverflowError):
            value = math.nan
        if not math.isfinite(value):
            internal_logger.warn(f"Dropping metric {name!r}: its value must be a finite number")
            return

        if self._pid != os.getpid():
            # A forked child: the parent's sender is gone and its locks may be held forever
            self._reset()

        with self._lock:
            pending = self._pending.get(name)
            if pending is not None and operation == MetricOperation.CHANGE:
                # A change adds to the pending operation, while a set replaces it
                value, operation = pending[0] + value, pending[1]
            self._pending[name] = (value, operation)
            if not self._waiting:
                self._waiting = self._send_in_background(self._send_pending)

    def _send_pending(self) -> None:
        with self._send_lock:
            with self._lock:
                pending, self._pending, self._waiting = self._pending, {}, False
            for name, (value, operation) in pending.items():
                self._send_metric(name, value, operation)

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
                    **({"app": self.app} if self.app else {}),
                },
                timeout=5,  # Add timeout to prevent blocking
            )
        except requests.RequestException:
            # Silently fail for now - future: add retry queue
            pass
