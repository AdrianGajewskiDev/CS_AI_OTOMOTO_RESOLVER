from enum import StrEnum

class FuelType(StrEnum):
    Petrol = "Petrol"
    Petrol_CNG = "Petrol_CNG"
    Petrol_LPG = "Petrol_LPG"
    Diesel = "Diesel"
    Electric = "Electric"
    Etanol = "Etanol"
    Hybrid = "Hybrid"
    Plugin_Hybrid = "Hybrid_Plug-in"
    Hydrogen = "Hydrogen"

def map_fuel_type(fuel_type: str) -> FuelType:
    if fuel_type == "Benzyna":
        return FuelType.Petrol

    if fuel_type == "Benzyna+CNG":
        return FuelType.Petrol_CNG

    if fuel_type == "Benzyna+LPG":
        return FuelType.Petrol_LPG

    if fuel_type == "Diesel":
        return FuelType.Diesel

    if fuel_type == "Elektryczny":
        return FuelType.Electric

    if fuel_type == "Etanol":
        return FuelType.Etanol

    if fuel_type == "Hybryda":
        return FuelType.Hybrid

    if fuel_type == "Hybryda Plug-in":
        return FuelType.Plugin_Hybrid

    if fuel_type == "Wodór":
        return FuelType.Hydrogen

    raise ValueError(f"Unknown fuel type: {fuel_type}")