from logdash.sync.base import LogSync
from logdash.constants import LogLevel


class NoopLogSync(LogSync):
    def send(self, message: str, level: LogLevel, created_at: str) -> None:
        pass 