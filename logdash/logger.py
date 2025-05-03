"""Logger implementation for LogDash."""

from datetime import datetime
from typing import Any, Callable, Optional

from colorama import Style, init

from logdash.constants import LogLevel, LOG_LEVEL_COLORS

# Initialize colorama for cross-platform terminal colors
init()


class Logger:
    """
    A flexible logger for terminal output and remote logging.
    
    The Logger provides methods for different log levels and can 
    both print locally and send logs to a remote service.
    """
    
    def __init__(
        self,
        log_method: Callable = print,
        prefix: Optional[Callable[[LogLevel], str]] = None,
        on_log: Optional[Callable[[LogLevel, str], None]] = None,
    ):
        """
        Initialize a new Logger instance.
        
        Args:
            log_method: Function to use for local logging (default: print)
            prefix: Optional function to generate log level prefix
            on_log: Optional callback for when logs are generated
        """
        self.log_method = log_method
        self.prefix = prefix or (lambda level: f"{level.value.upper()} ")
        self.on_log = on_log

    def error(self, *data: Any) -> None:
        """Log an error message."""
        self._log(LogLevel.ERROR, " ".join(str(item) for item in data))

    def warn(self, *data: Any) -> None:
        """Log a warning message."""
        self._log(LogLevel.WARN, " ".join(str(item) for item in data))

    def info(self, *data: Any) -> None:
        """Log an info message."""
        self._log(LogLevel.INFO, " ".join(str(item) for item in data))

    def log(self, *data: Any) -> None:
        """Alias for info()."""
        self.info(*data)

    def http(self, *data: Any) -> None:
        """Log an HTTP-related message."""
        self._log(LogLevel.HTTP, " ".join(str(item) for item in data))

    def verbose(self, *data: Any) -> None:
        """Log a verbose message."""
        self._log(LogLevel.VERBOSE, " ".join(str(item) for item in data))

    def debug(self, *data: Any) -> None:
        """Log a debug message."""
        self._log(LogLevel.DEBUG, " ".join(str(item) for item in data))

    def silly(self, *data: Any) -> None:
        """Log a silly message (lowest priority)."""
        self._log(LogLevel.SILLY, " ".join(str(item) for item in data))

    def _log(self, level: LogLevel, message: str) -> None:
        """
        Internal method to format and output a log message.
        
        Args:
            level: The log level
            message: The message to log
        """
        # Format with color
        color = LOG_LEVEL_COLORS[level]
        timestamp = datetime.now().isoformat()
        
        # Format the message with timestamp and level prefix
        formatted_message = (
            f"\033[90m[{timestamp}]\033[0m "
            f"{color}{self.prefix(level)}\033[0m"
            f"{message}"
        )

        # Output to configured log method
        self.log_method(formatted_message)
        
        # Call the callback if configured
        if self.on_log:
            self.on_log(level, message) 