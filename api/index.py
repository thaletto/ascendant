"""Public Streamable HTTP MCP server for the Ascendant Python library."""

from typing import Annotated, Any

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastmcp import FastMCP
from pydantic import Field

from ascendant import Ascendant
from ascendant.const import ALLOWED_DIVISIONS

BirthYear = Annotated[int, Field(ge=1, le=9999, description="Four-digit year of birth.")]
BirthMonth = Annotated[int, Field(ge=1, le=12, description="Month of birth.")]
BirthDay = Annotated[int, Field(ge=1, le=31, description="Day of birth.")]
BirthHour = Annotated[int, Field(ge=0, le=23, description="Hour of birth in 24-hour time.")]
BirthMinute = Annotated[int, Field(ge=0, le=59, description="Minute of birth.")]
BirthSecond = Annotated[int, Field(ge=0, le=59, description="Second of birth.")]
Latitude = Annotated[float, Field(ge=-90, le=90, description="Birthplace latitude in decimal degrees.")]
Longitude = Annotated[
    float, Field(ge=-180, le=180, description="Birthplace longitude in decimal degrees.")
]
UtcOffset = Annotated[str, Field(pattern=r"^[+-](?:0\d|1[0-4]):[0-5]\d$", description="UTC offset, for example +05:30.")]
Division = Annotated[int, Field(description="Varga division; supported values are 1, 2, 3, 4, 7, 9, 10, 12, 16, 20, 24, 27, 30, 40, 45, and 60.")]

mcp = FastMCP(
    "Ascendant",
    instructions=(
        "Use these tools to calculate Vedic astrology charts, dashas, and yogas with the "
        "Ascendant Python library. Treat results as astrological calculations, not medical, "
        "legal, or financial advice."
    ),
)


def create_ascendant(
    year: BirthYear,
    month: BirthMonth,
    day: BirthDay,
    hour: BirthHour,
    minute: BirthMinute,
    second: BirthSecond,
    latitude: Latitude,
    longitude: Longitude,
    utc: UtcOffset,
    ayanamsa: str = "Lahiri",
    house_system: str = "Whole Sign",
) -> Ascendant:
    return Ascendant(
        year=year,
        month=month,
        day=day,
        hour=hour,
        minute=minute,
        second=second,
        latitude=latitude,
        longitude=longitude,
        utc=utc,
        ayanamsa=ayanamsa,
        house_system=house_system,
    )


@mcp.tool
def calculate_chart(
    year: BirthYear,
    month: BirthMonth,
    day: BirthDay,
    hour: BirthHour,
    minute: BirthMinute,
    second: BirthSecond,
    latitude: Latitude,
    longitude: Longitude,
    utc: UtcOffset,
    division: Division = 1,
    ayanamsa: str = "Lahiri",
    house_system: str = "Whole Sign",
) -> dict[int, Any]:
    """Calculate a divisional Vedic birth chart for a person and birthplace."""
    if division not in ALLOWED_DIVISIONS:
        raise ValueError(f"Unsupported division {division}. Supported values: {ALLOWED_DIVISIONS}.")

    return create_ascendant(
        year, month, day, hour, minute, second, latitude, longitude, utc, ayanamsa, house_system
    ).get_chart(division)


@mcp.tool
def get_dasha_timeline(
    year: BirthYear,
    month: BirthMonth,
    day: BirthDay,
    hour: BirthHour,
    minute: BirthMinute,
    second: BirthSecond,
    latitude: Latitude,
    longitude: Longitude,
    utc: UtcOffset,
    ayanamsa: str = "Lahiri",
    house_system: str = "Whole Sign",
) -> list[dict[str, Any]]:
    """Return the Vimshottari Mahadasha and Antardasha timeline for a birth chart."""
    return create_ascendant(
        year, month, day, hour, minute, second, latitude, longitude, utc, ayanamsa, house_system
    ).get_dasha_timeline()


@mcp.tool
def get_current_dasha(
    year: BirthYear,
    month: BirthMonth,
    day: BirthDay,
    hour: BirthHour,
    minute: BirthMinute,
    second: BirthSecond,
    latitude: Latitude,
    longitude: Longitude,
    utc: UtcOffset,
    date: str | None = None,
    ayanamsa: str = "Lahiri",
    house_system: str = "Whole Sign",
) -> dict[str, Any]:
    """Return the active Mahadasha and Antardasha, optionally for an ISO date (YYYY-MM-DD)."""
    return create_ascendant(
        year, month, day, hour, minute, second, latitude, longitude, utc, ayanamsa, house_system
    ).get_current_dasha(date)


@mcp.tool
def get_yogas(
    year: BirthYear,
    month: BirthMonth,
    day: BirthDay,
    hour: BirthHour,
    minute: BirthMinute,
    second: BirthSecond,
    latitude: Latitude,
    longitude: Longitude,
    utc: UtcOffset,
    ayanamsa: str = "Lahiri",
    house_system: str = "Whole Sign",
) -> list[dict[str, Any]]:
    """Calculate the yogas present in a person's Vedic birth chart."""
    return create_ascendant(
        year, month, day, hour, minute, second, latitude, longitude, utc, ayanamsa, house_system
    ).get_yogas()


mcp_app = mcp.http_app(path="/")
app = FastAPI(title="Ascendant MCP Server", lifespan=mcp_app.lifespan)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["GET", "POST", "DELETE", "OPTIONS"],
    allow_headers=["Content-Type", "Mcp-Session-Id", "MCP-Protocol-Version", "Last-Event-ID"],
    expose_headers=["Mcp-Session-Id", "MCP-Protocol-Version"],
)


@app.get("/api/health")
def health() -> dict[str, str]:
    """Vercel health check endpoint; MCP clients should connect to /api/mcp instead."""
    return {"status": "ok", "mcp_endpoint": "/api/mcp"}


app.mount("/api/mcp", mcp_app)
