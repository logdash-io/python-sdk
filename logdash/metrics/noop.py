from logdash.metrics.base import BaseMetrics


class NoopMetrics(BaseMetrics):
    def set(self, name: str, value: float) -> None:
        pass
    
    def mutate(self, name: str, value: float) -> None:
        pass 