from enum import StrEnum


class Transmissions(StrEnum):
    MANUAL = "Manual"
    AUTOMATIC = "Automatic"

def map_transmission(transmission: str) -> Transmissions:
    if transmission == "Manualna":
        return Transmissions.MANUAL
    
    if transmission == "Automatyczna":
        return Transmissions.AUTOMATIC
    
    raise ValueError(f"Unknown transmission: {transmission}")