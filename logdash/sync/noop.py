"""No-operation log synchronization implementation."""

from logdash.sync.base import LogSync
from logdash.constants import LogLevel


class NoopLogSync(LogSync):
    """
    No-operation log synchronization implementation.
    
    This implementation does nothing when logs are sent to it.
    Useful for testing or when no remote logging is needed.
    """
    
    def send(self, message: str, level: LogLevel, created_at: str) -> None:
        """
        Do nothing with the log message.
        
        Args:
            message: The log message content
            level: The log level
            created_at: ISO-formatted timestamp when the log was created
        """
        pass 