"""Base class for log synchronization implementations."""

from abc import ABC, abstractmethod

from logdash.constants import LogLevel


class LogSync(ABC):
    """Abstract base class for log synchronization implementations."""
    
    @abstractmethod
    def send(self, message: str, level: LogLevel, created_at: str) -> None:
        """
        Send a log message to the remote service.
        
        Args:
            message: The log message content
            level: The log level
            created_at: ISO-formatted timestamp when the log was created
        """
        pass 