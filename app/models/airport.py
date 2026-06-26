import uuid

from sqlalchemy import String
from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base


class Airport(Base):

    __tablename__ = "airports"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    airport_code: Mapped[str] = mapped_column(
        String(10),
        unique=True,
        nullable=False
    )

    airport_name: Mapped[str] = mapped_column(
        String(255),
        nullable=False
    )

    city: Mapped[str] = mapped_column(
        String(100)
    )

    country: Mapped[str] = mapped_column(
        String(100)
    )

    terminals = relationship(
        "Terminal",
        back_populates="airport"
    )