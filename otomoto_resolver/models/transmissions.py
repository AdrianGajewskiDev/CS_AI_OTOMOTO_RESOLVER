from enum import StrEnum


class Transmissions(StrEnum):
    MANUAL = "Manual"
    AUTOMATIC = "Automatic"

def map_transmission(transmission: str) -> Transmissions:
    if transmission == "manual":
        return Transmissions.MANUAL
    
    if transmission == "automatic":
        return Transmissions.AUTOMATIC
    
    raise ValueError(f"Unknown transmission: {transmission}")