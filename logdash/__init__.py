"""
logdash Python SDK for logging and metrics.

This package provides utilities for logging and metrics collection.
"""

from logdash.core import create_logdash
from logdash.logger import Logger
from logdash.metrics import MetricOperation

__all__ = ["create_logdash", "Logger", "MetricOperation"]
__version__ = "0.2.0" 