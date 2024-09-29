from typing import List, Optional
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
    AdvertisementLink: Optional[str] = None
    Thumbnails: Optional[List[str]] = None
    Source: str = "https://www.otomoto.pl"