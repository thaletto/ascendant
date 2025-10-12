"""
Pydantic models for Birth Data in astrology analysis
"""

from typing import Optional, Dict, Any
from pydantic import BaseModel, Field, field_validator


class BirthDataBase(BaseModel):
    """Base model for birth data with common fields."""

    name: str = Field(
        ..., min_length=1, max_length=200, description="Person's full name"
    )
    birth_year: int = Field(..., ge=1800, le=2100, description="Birth year")
    birth_month: int = Field(..., ge=1, le=12, description="Birth month (1-12)")
    birth_day: int = Field(..., ge=1, le=31, description="Birth day (1-31)")
    birth_hour: int = Field(..., ge=0, le=23, description="Birth hour (0-23)")
    birth_minute: int = Field(..., ge=0, le=59, description="Birth minute (0-59)")
    birth_second: int = Field(default=0, ge=0, le=59, description="Birth second (0-59)")
    latitude: float = Field(
        ..., ge=-90.0, le=90.0, description="Birth latitude in decimal degrees"
    )
    longitude: float = Field(
        ..., ge=-180.0, le=180.0, description="Birth longitude in decimal degrees"
    )
    utc: str = Field(..., description="UTC timezone offset (e.g., '+05:30', '-08:00')")

    @field_validator("birth_day")
    def validate_birth_day(cls, v, values):
        """Validate birth day based on month."""
        month = values.get("birth_month")
        if month in [4, 6, 9, 11] and v > 30:
            raise ValueError(f"Day {v} is invalid for month {month}")
        elif month == 2 and v > 29:
            raise ValueError(f"Day {v} is invalid for February")
        return v

    @field_validator("utc")
    def validate_utc_format(cls, v):
        """Validate UTC timezone format."""
        if not (v.startswith(("+", "-")) and len(v) == 6 and v[3] == ":"):
            raise ValueError("UTC must be in format +/-HH:MM (e.g., +05:30)")
        return v


class BirthDataCreate(BirthDataBase):
    """Model for creating birth data."""

    pass


class BirthDataUpdate(BaseModel):
    """Model for updating birth data."""

    name: Optional[str] = Field(None, min_length=1, max_length=200)
    birth_year: Optional[int] = Field(None, ge=1800, le=2100)
    birth_month: Optional[int] = Field(None, ge=1, le=12)
    birth_day: Optional[int] = Field(None, ge=1, le=31)
    birth_hour: Optional[int] = Field(None, ge=0, le=23)
    birth_minute: Optional[int] = Field(None, ge=0, le=59)
    birth_second: Optional[int] = Field(None, ge=0, le=59)
    latitude: Optional[float] = Field(None, ge=-90.0, le=90.0)
    longitude: Optional[float] = Field(None, ge=-180.0, le=180.0)
    utc: Optional[str] = Field(None)


class BirthData(BirthDataBase):
    """Complete birth data model with astrology-specific fields."""

    ayanamsa: str = Field(
        default="Lahiri", description="Ayanamsa system used for calculations"
    )
    house_system: str = Field(
        default="Whole Sign", description="House system for chart calculations"
    )

    class Config:
        """Pydantic configuration."""

        from_attributes = True
        json_encoders = {
            # Add any custom encoders if needed
        }

    def to_dict(self) -> Dict[str, Any]:
        """Convert to dictionary format expected by astrology tools."""
        return {
            "name": self.name,
            "birth_year": self.birth_year,
            "birth_month": self.birth_month,
            "birth_day": self.birth_day,
            "birth_hour": self.birth_hour,
            "birth_minute": self.birth_minute,
            "birth_second": self.birth_second,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "utc": self.utc,
            "ayanamsa": self.ayanamsa,
            "house_system": self.house_system,
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "BirthData":
        """Create BirthData from dictionary."""
        return cls(**data)


class BirthDataResponse(BirthData):
    """Model for birth data response."""

    id: Optional[int] = Field(None, description="Database ID if stored")
    created_at: Optional[str] = Field(None, description="Creation timestamp")

    class Config:
        from_attributes = True


class BirthDataValidation(BaseModel):
    """Model for birth data validation response."""

    is_valid: bool = Field(..., description="Whether the birth data is valid")
    errors: Optional[list[str]] = Field(
        default=None, description="List of validation errors"
    )
    warnings: Optional[list[str]] = Field(
        default=None, description="List of validation warnings"
    )
    birth_data: Optional[BirthData] = Field(
        default=None, description="Validated birth data"
    )
