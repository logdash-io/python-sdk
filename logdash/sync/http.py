"""HTTP-based log synchronization implementation."""

import requests

from logdash.sync.base import LogSync
from logdash.constants import LogLevel


class HttpLogSync(LogSync):
    """
    HTTP-based log synchronization implementation.
    
    Sends logs to the logdash API via HTTP.
    """
    
    def __init__(self, api_key: str, host: str, verbose: bool = False):
        """
        Initialize an HTTP log sync instance.
        
        Args:
            api_key: logdash API key
            host: logdash API host
            verbose: Enable verbose mode
        """
        self.api_key = api_key
        self.host = host
        self.verbose = verbose
        self.sequence_number = 0

    def send(self, message: str, level: LogLevel, created_at: str) -> None:
        """
        Send a log message to the logdash API.
        
        Args:
            message: The log message content
            level: The log level
            created_at: ISO-formatted timestamp when the log was created
            
        Todo:
            - Implement queue for offline support
            - Add retry mechanism
            - Implement batching for better performance
        """
        # Skip if no API key is provided
        if not self.api_key:
            return
            
        try:
            requests.post(
                f"{self.host}/logs",
                headers={
                    "Content-Type": "application/json",
                    "project-api-key": self.api_key,
                },
                json={
                    "message": message,
                    "level": level,
                    "createdAt": created_at,
                    "sequenceNumber": self.sequence_number,
                },
                timeout=5,  # Add timeout to prevent blocking
            )
            self.sequence_number += 1
        except requests.RequestException:
            # Silently fail for now - future: add retry queue
            pass 