from enum import Enum


class SearchState(str, Enum):
    FAILED = "FAILED"
    RUNNING = "RUNNING"
    STATE_UNSPECIFIED = "STATE_UNSPECIFIED"
    SUCCEEDED = "SUCCEEDED"

    def __str__(self) -> str:
        return str(self.value)
