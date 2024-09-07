from typing import Protocol


class SeedDataResolver(Protocol):
    def get_seed_data(self) -> dict:
        pass