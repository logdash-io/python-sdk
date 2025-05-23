from datetime import datetime, timezone
from typing import Dict, Optional, Any

from logdash.logger import Logger
from logdash.metrics.base import BaseMetrics
from logdash.metrics.factory import create_metrics
from logdash.sync.factory import create_log_sync
from logdash.constants import LogLevel


class logdash:
    def __init__(self, api_key: Optional[str] = None, host: str = "https://api.logdash.io", verbose: bool = False):
        # Ensure we have an API key (or empty string)
        self._api_key = api_key or ""
        self._host = host
        self._verbose = verbose
        
        # Create log sync and metrics instances
        self._log_sync = create_log_sync(self._api_key, self._host, self._verbose)
        self._metrics_instance = create_metrics(self._api_key, self._host, self._verbose)

        # Initialize logger
        def on_log(level: LogLevel, message: str) -> None:
            self._log_sync.send(message, level, datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
)
            
        self._logger_instance = Logger(log_method=print, on_log=on_log)
    
    @property
    def logger(self) -> Logger:
        """Get the logger instance."""
        return self._logger_instance
    
    @property
    def metrics(self) -> BaseMetrics:
        """Get the metrics instance."""
        return self._metrics_instance


def create_logdash(params: Optional[Dict[str, Any]] = None) -> logdash:
    """
    Create a new logdash instance with logger and metrics.
    
    Args:
        params: Optional dictionary with configuration parameters:
               - api_key: Your logdash API key
               - host: logdash API host (defaults to https://api.logdash.io)
               - verbose: Enable verbose mode
               
    Returns:
        A logdash instance with logger and metrics properties
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
    
    return logdash(api_key, host, verbose) 