from typing import Optional
from pydantic import BaseModel

class ResolverResponse(BaseModel): 
    Price: Optional[str] = None
    PriceCurrency: Optional[str] = None
    Mileage: Optional[str] = None
    ProductionYear: Optional[str] = None
    FuelType: Optional[str] = None
    Transmision: Optional[str] = None
    HorsePower: Optional[str] = None
    Capacity: Optional[str] = None