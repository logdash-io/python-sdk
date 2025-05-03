"""No-operation metrics implementation."""

from logdash.metrics.base import BaseMetrics


class NoopMetrics(BaseMetrics):
    """
    No-operation metrics implementation.
    
    This implementation does nothing when metrics are set or mutated.
    Useful for testing or when no remote metrics collection is needed.
    """
    
    def set(self, name: str, value: float) -> None:
        """
        Do nothing with the metric.
        
        Args:
            name: The metric name
            value: The value to set
        """
        pass
    
    def mutate(self, name: str, value: float) -> None:
        """
        Do nothing with the metric.
        
        Args:
            name: The metric name
            value: The amount to change by
        """
        pass 