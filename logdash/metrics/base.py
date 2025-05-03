from abc import ABC, abstractmethod


class BaseMetrics(ABC):
    @abstractmethod
    def set(self, name: str, value: float) -> None:
        """
        Set a metric to an absolute value.
        
        Args:
            name: The metric name
            value: The value to set
        """
        pass
    
    @abstractmethod
    def mutate(self, name: str, value: float) -> None:
        """
        Change a metric by a relative value.
        
        Args:
            name: The metric name
            value: The amount to change by
        """
        pass 