import json

from sqlalchemy import Column, DateTime, Float, ForeignKey, Integer, String, func
from sqlalchemy.orm import relationship
from sqlalchemy.types import TEXT, TypeDecorator

from api.database import Base


class JSONEncodedDict(TypeDecorator):
    """Enables JSON storage by encoding and decoding on the fly."""

    impl = TEXT

    def process_bind_param(self, value, dialect):
        if value is not None:
            return json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            return json.loads(value)
        return value


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    year = Column(Integer, nullable=False)
    month = Column(Integer, nullable=False)
    day = Column(Integer, nullable=False)
    hour = Column(Integer, nullable=False)
    minute = Column(Integer, nullable=False)
    second = Column(Integer, default=0)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    utc = Column(String, default="+5:30")
    ayanamsa = Column(String, default="Lahiri")
    house_system = Column(String, default="whole_sign")

    created_at = Column(DateTime(timezone=True), server_default=func.now())
    updated_at = Column(DateTime(timezone=True), onupdate=func.now())

    charts = relationship("Chart", back_populates="owner", cascade="all, delete-orphan")
    dasha = relationship(
        "Dasha", back_populates="owner", uselist=False, cascade="all, delete-orphan"
    )


class Chart(Base):
    __tablename__ = "charts"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    division = Column(Integer, nullable=False)  # Should be one of ALLOWED_DIVISIONS
    chart_data = Column(JSONEncodedDict, nullable=False)

    owner = relationship("User", back_populates="charts")


class Dasha(Base):
    __tablename__ = "dashas"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    dasha_data = Column(JSONEncodedDict, nullable=False)

    owner = relationship("User", back_populates="dasha")
