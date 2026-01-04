from typing import Any, Dict, List, Optional

from pydantic import BaseModel, Field


class BirthDetails(BaseModel):
    year: int = Field(..., description="Year of birth")
    month: int = Field(..., description="Month of birth (1-12)")
    day: int = Field(..., description="Day of birth (1-31)")
    hour: int = Field(..., description="Hour of birth (0-23)")
    minute: int = Field(..., description="Minute of birth (0-59)")
    second: int = Field(0, description="Second of birth (0-59)")
    latitude: float = Field(..., description="Latitude of birth place")
    longitude: float = Field(..., description="Longitude of birth place")
    utc: str = Field("+5:30", description="Timezone offset (e.g. '+5:30')")
    ayanamsa: str = Field("Lahiri", description="Ayanamsa system")
    house_system: str = Field("whole_sign", description="House system")

    model_config = {
        "json_schema_extra": {
            "example": {
                "year": 2003,
                "month": 8,
                "day": 19,
                "hour": 11,
                "minute": 55,
                "second": 0,
                "latitude": 13.0827,
                "longitude": 80.2707,
                "utc": "+5:30",
                "ayanamsa": "Lahiri",
                "house_system": "whole_sign",
            }
        }
    }


class ChartRequest(BirthDetails):
    division: int = Field(
        1, description="Divisional chart (e.g. 1 for Rasi, 9 for Navamsa)"
    )


class YogaRequest(BirthDetails):
    pass


class DashaRequest(BirthDetails):
    date: Optional[str] = Field(
        None, description="Date for current dasha calculation (DD-MM-YYYY)"
    )


class ChartOut(BaseModel):
    id: int
    user_id: int
    division: int
    chart_data: Dict[str, Any]

    class Config:
        from_attributes = True


class DashaOut(BaseModel):
    id: int
    user_id: int
    dasha_data: Dict[str, Any]

    class Config:
        from_attributes = True


class UserOut(BaseModel):
    id: int
    year: int
    month: int
    day: int
    hour: int
    minute: int
    second: int
    latitude: float
    longitude: float
    utc: str
    ayanamsa: str
    house_system: str
    charts: List[ChartOut] = []
    dasha: Optional[DashaOut] = None

    class Config:
        from_attributes = True


class UserCreationOut(BirthDetails):
    id: int = Field(..., description="The unique ID of the created user")

    class Config:
        from_attributes = True


class ChartResponse(BaseModel):
    division: int
    chart: Dict[int, Any]


class YogaResponse(BaseModel):
    yogas: List[Dict[str, Any]]


class DashaResponse(BaseModel):
    timeline: List[Dict[str, Any]]
    current: Optional[Dict[str, Any]] = None
