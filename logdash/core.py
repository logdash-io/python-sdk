"""Core functionality for the LogDash SDK."""

from datetime import datetime
from typing import Dict, Optional, Any, TypedDict

from logdash.logger import Logger
from logdash.metrics.base import BaseMetrics
from logdash.metrics.factory import create_metrics
from logdash.sync.factory import create_log_sync
from logdash.constants import LogLevel


class LogdashInstance(TypedDict):
    """Return type for create_logdash containing logger and metrics instances."""
    logger: Logger
    metrics: BaseMetrics


def create_logdash(params: Optional[Dict[str, Any]] = None) -> LogdashInstance:
    """
    Create a new LogDash instance with logger and metrics.
    
    Args:
        params: Optional dictionary with configuration parameters:
               - api_key: Your LogDash API key
               - host: LogDash API host (defaults to https://api.logdash.io)
               - verbose: Enable verbose mode
               
    Returns:
        A dictionary containing logger and metrics instances
    """
    # Initialize with default values
    api_key = None
    host = "https://api.logdash.io"
    verbose = False
    
    # Override with provided params if any
    if params is not None:
        api_key = params.get("api_key", api_key)
        host = params.get("host", host)
        verbose = params.get("verbose", verbose)
    
    # Ensure we have an API key
    api_key = api_key or ""
    
    # Create log sync and metrics instances
    log_sync = create_log_sync(api_key, host, verbose)
    metrics = create_metrics(api_key, host, verbose)

    # Callback for logging
    def on_log(level: LogLevel, message: str) -> None:
        log_sync.send(message, level, datetime.now().isoformat())

    return {
        "logger": Logger(log_method=print, on_log=on_log),
        "metrics": metrics,
    } 