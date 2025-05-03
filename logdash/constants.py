from enum import Enum


class LogLevel(str, Enum):
    ERROR = "error"
    WARN = "warning"
    INFO = "info"
    HTTP = "http"
    VERBOSE = "verbose"
    DEBUG = "debug"
    SILLY = "silly"


class MetricOperation(str, Enum):
    SET = "set"
    CHANGE = "change"


LOG_LEVEL_COLORS = {
    LogLevel.ERROR: (231, 0, 11),      # Red
    LogLevel.WARN: (254, 154, 0),      # Orange
    LogLevel.INFO: (21, 93, 252),      # Blue
    LogLevel.HTTP: (0, 166, 166),      # Teal
    LogLevel.VERBOSE: (0, 166, 0),     # Green
    LogLevel.DEBUG: (0, 166, 62),      # Light Green
    LogLevel.SILLY: (80, 80, 80),      # Gray
} 