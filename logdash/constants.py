"""Constants used throughout the logdash SDK."""

from enum import Enum
from colorama import Fore


class LogLevel(str, Enum):
    """Log levels supported by logdash."""
    ERROR = "error"
    WARN = "warning"
    INFO = "info"
    HTTP = "http"
    VERBOSE = "verbose"
    DEBUG = "debug"
    SILLY = "silly"


class MetricOperation(str, Enum):
    """Metric operations supported by logdash."""
    SET = "set"
    CHANGE = "change"


# Color mapping for log levels in terminal output
LOG_LEVEL_COLORS = {
    LogLevel.ERROR: Fore.RED,
    LogLevel.WARN: Fore.YELLOW,
    LogLevel.INFO: Fore.BLUE,
    LogLevel.HTTP: Fore.CYAN,
    LogLevel.VERBOSE: Fore.GREEN,
    LogLevel.DEBUG: Fore.LIGHTGREEN_EX,
    LogLevel.SILLY: Fore.LIGHTBLACK_EX,
} 