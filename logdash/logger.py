from datetime import datetime
import json
from typing import Any, Callable, Optional, Tuple

from colorama import init  # For Windows compatibility
from logdash.constants import LogLevel, LOG_LEVEL_COLORS

# Initialize colorama for cross-platform terminal colors
init()

class Logger:
    def __init__(
        self,
        log_method: Callable = print,
        prefix: Optional[Callable[[LogLevel], str]] = None,
        on_log: Optional[Callable[[LogLevel, str], None]] = None,
    ):
        self.log_method = log_method
        self.prefix = prefix or (lambda level: f"{level.value.upper()} ")
        self.on_log = on_log

    def _format_item(self, item: Any) -> str:
        """Format an item for logging, converting to JSON if possible."""
        try:
            # Check if the item is a dict, list, or other JSON-serializable object
            if isinstance(item, (dict, list)) or hasattr(item, "__dict__"):
                return json.dumps(item, default=lambda o: o.__dict__ if hasattr(o, "__dict__") else str(o))
            return str(item)
        except (TypeError, ValueError):
            # Fallback to string representation if JSON serialization fails
            return str(item)

    def error(self, *data: Any) -> None:
        """Log an error message."""
        self._log(LogLevel.ERROR, " ".join(self._format_item(item) for item in data))

    def warn(self, *data: Any) -> None:
        """Log a warning message."""
        self._log(LogLevel.WARN, " ".join(self._format_item(item) for item in data))

    def info(self, *data: Any) -> None:
        """Log an info message."""
        self._log(LogLevel.INFO, " ".join(self._format_item(item) for item in data))

    def log(self, *data: Any) -> None:
        """Alias for info()."""
        self.info(*data)

    def http(self, *data: Any) -> None:
        """Log an HTTP-related message."""
        self._log(LogLevel.HTTP, " ".join(self._format_item(item) for item in data))

    def verbose(self, *data: Any) -> None:
        """Log a verbose message."""
        self._log(LogLevel.VERBOSE, " ".join(self._format_item(item) for item in data))

    def debug(self, *data: Any) -> None:
        """Log a debug message."""
        self._log(LogLevel.DEBUG, " ".join(self._format_item(item) for item in data))

    def silly(self, *data: Any) -> None:
        """Log a silly message (lowest priority)."""
        self._log(LogLevel.SILLY, " ".join(self._format_item(item) for item in data))
    
    def _rgb_to_ansi(self, rgb: Tuple[int, int, int]) -> str:
        r, g, b = rgb
        return f"\033[38;2;{r};{g};{b}m"

    def _log(self, level: LogLevel, message: str) -> None:
        # Get RGB values and convert to ANSI color
        rgb_color = LOG_LEVEL_COLORS[level]
        color_code = self._rgb_to_ansi(rgb_color)
        timestamp = datetime.now().isoformat()
        
        # Format the message with timestamp and level prefix
        formatted_message = (
            f"\033[38;2;150;150;150m[{timestamp}]\033[0m "
            f"{color_code}{self.prefix(level)}\033[0m"
            f"{message}"
        )

        # Output to configured log method
        self.log_method(formatted_message)
        
        # Call the callback if configured
        if self.on_log:
            self.on_log(level, message) 