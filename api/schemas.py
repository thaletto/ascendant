import json
from typing import Any

from sqlalchemy import DateTime, ForeignKey, String, func
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.types import TEXT, TypeDecorator

from api.database import Base


class JSONEncodedDict(TypeDecorator[Any]):
    impl = TEXT
    cache_ok = True

    def process_bind_param(self, value: Any, dialect):
        return json.dumps(value) if value is not None else None

    def process_result_value(self, value: Any, dialect):
        return json.loads(value) if value is not None else None


class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)

    year: Mapped[int]
    month: Mapped[int]
    day: Mapped[int]
    hour: Mapped[int]
    minute: Mapped[int]
    second: Mapped[int] = mapped_column(default=0)

    latitude: Mapped[float]
    longitude: Mapped[float]

    utc: Mapped[str | None] = mapped_column(String, default="+05:30")

    ayanamsa: Mapped[str] = mapped_column(default="Lahiri")
    house_system: Mapped[str] = mapped_column(default="whole_sign")

    created_at: Mapped[Any] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
    )

    updated_at: Mapped[Any] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
    )

    charts: Mapped[list["Chart"]] = relationship(
        back_populates="owner", cascade="all, delete-orphan"
    )

    dasha: Mapped["Dasha | None"] = relationship(
        back_populates="owner", uselist=False, cascade="all, delete-orphan"
    )


class Chart(Base):
    __tablename__ = "charts"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    division: Mapped[int]
    chart_data: Mapped[dict] = mapped_column(JSONEncodedDict, nullable=False)

    owner: Mapped["User"] = relationship(back_populates="charts")


class Dasha(Base):
    __tablename__ = "dashas"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    user_id: Mapped[int] = mapped_column(
        ForeignKey("users.id"), nullable=False, unique=True
    )
    dasha_data: Mapped[dict] = mapped_column(JSONEncodedDict, nullable=False)

    owner: Mapped["User"] = relationship(back_populates="dasha")
