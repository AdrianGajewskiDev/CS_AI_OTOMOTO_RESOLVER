from enum import Enum
from typing import List, Optional
from pydantic import BaseModel

class ResolverRule(BaseModel):
    Static: Optional[bool] = False
    Type: str
    Value: str

class TypedResolverRule(BaseModel):
    Field: str
    Rule: ResolverRule


class ResolverStrategy(BaseModel):
    Iterations: int
    Rules: List[ResolverRule]

class NamedFields(str, Enum):
    Base = "Base",
    Type = "Type",
    Make = "Make",
    Model = "Model",
    ProductionYearFrom = "ProductionYearFrom",
    ProductionYearTo = "ProductionYearTo",
    MileageFrom = "MileageFrom",
    MileageTo = "MileageTo",
    Generation = "Generation"

class FieldTypes(str, Enum):
    UrlPart = "UrlPart",
    QueryString = "QueryString"


class StrategyRuleType(str, Enum):
    AppendToQuery = "AppendToQuery"