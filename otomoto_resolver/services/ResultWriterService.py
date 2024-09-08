from typing import Protocol


class ResultWriterService(Protocol):
    def write_result(self, content: dict, key: str) -> None:
        pass