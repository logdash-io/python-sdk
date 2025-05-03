from logdash.sync.base import LogSync
from logdash.sync.http import HttpLogSync
from logdash.sync.noop import NoopLogSync
from logdash.internal import internal_logger


def create_log_sync(api_key: str, host: str, verbose: bool = False) -> LogSync:
    if not api_key:
        if verbose:
            internal_logger.warn("No API key provided, using NoopLogSync")
        return NoopLogSync()
    
    if verbose:
        internal_logger.verbose(f"Creating HttpLogSync with host {host}")
    
    return HttpLogSync(api_key, host, verbose) 