import uuid

from datetime import datetime

from sqlalchemy import String
from sqlalchemy import Integer
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Enum

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base

from app.models.enums import FlightStatus


class Flight(Base):

    __tablename__ = "flights"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    airline_id: Mapped[str] = mapped_column(
        ForeignKey("airlines.id")
    )

    terminal_id: Mapped[str] = mapped_column(
        ForeignKey("terminals.id")
    )

    gate_id: Mapped[str] = mapped_column(
        ForeignKey("gates.id")
    )

    flight_number: Mapped[str] = mapped_column(
        String(30),
        unique=True
    )

    origin: Mapped[str] = mapped_column(
        String(100)
    )

    destination: Mapped[str] = mapped_column(
        String(100)
    )

    scheduled_departure: Mapped[datetime] = mapped_column(
        DateTime
    )

    scheduled_arrival: Mapped[datetime] = mapped_column(
        DateTime
    )

    delay_minutes: Mapped[int] = mapped_column(
        Integer,
        default=0
    )

    status: Mapped[FlightStatus] = mapped_column(
        Enum(FlightStatus),
        default=FlightStatus.SCHEDULED
    )

    airline = relationship(
        "Airline",
        back_populates="flights"
    )

    terminal = relationship(
        "Terminal"
    )

    gate = relationship(
        "Gate",
        back_populates="flights"
    )