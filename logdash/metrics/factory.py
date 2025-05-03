from logdash.metrics.base import BaseMetrics
from logdash.metrics.impl import Metrics
from logdash.metrics.noop import NoopMetrics
from logdash.internal import internal_logger


def create_metrics(api_key: str, host: str, verbose: bool = False) -> BaseMetrics:
    if not api_key:
        if verbose:
            internal_logger.warn("No API key provided, using NoopMetrics")
        return NoopMetrics()
    
    if verbose:
        internal_logger.verbose(f"Creating Metrics with host {host}")
    
    return Metrics(api_key, host, verbose) 