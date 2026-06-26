import uuid

from sqlalchemy import String

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base


class Airline(Base):

    __tablename__ = "airlines"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    airline_code: Mapped[str] = mapped_column(
        String(10),
        unique=True
    )

    airline_name: Mapped[str] = mapped_column(
        String(255)
    )

    country: Mapped[str] = mapped_column(
        String(100)
    )

    flights = relationship(
        "Flight",
        back_populates="airline"
    )