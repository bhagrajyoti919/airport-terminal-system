import uuid

from datetime import datetime

from sqlalchemy import String
from sqlalchemy import DateTime
from sqlalchemy import ForeignKey
from sqlalchemy import Text

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column

from app.core.database import Base


class FlightEvent(Base):

    __tablename__ = "flight_events"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    flight_id: Mapped[str] = mapped_column(
        ForeignKey("flights.id")
    )

    event_type: Mapped[str] = mapped_column(
        String(100)
    )

    old_value: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    new_value: Mapped[str] = mapped_column(
        Text,
        nullable=True
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime,
        default=datetime.utcnow
    )