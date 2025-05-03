"""Factory function for creating log sync instances."""

from logdash.sync.base import LogSync
from logdash.sync.http import HttpLogSync
from logdash.sync.noop import NoopLogSync
from logdash.internal import internal_logger


def create_log_sync(api_key: str, host: str, verbose: bool = False) -> LogSync:
    """
    Create a log sync instance based on the provided parameters.
    
    Args:
        api_key: LogDash API key
        host: LogDash API host
        verbose: Enable verbose mode
        
    Returns:
        A LogSync instance
    """
    if not api_key:
        if verbose:
            internal_logger.warn("No API key provided, using NoopLogSync")
        return NoopLogSync()
    
    if verbose:
        internal_logger.verbose(f"Creating HttpLogSync with host {host}")
    
    return HttpLogSync(api_key, host, verbose) 