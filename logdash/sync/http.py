import requests

from logdash.sync.base import LogSync
from logdash.constants import LogLevel


class HttpLogSync(LogSync):
    
    def __init__(self, api_key: str, host: str, verbose: bool = False):
        self.api_key = api_key
        self.host = host
        self.verbose = verbose
        self.sequence_number = 0

    def send(self, message: str, level: LogLevel, created_at: str) -> None:
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