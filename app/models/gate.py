import uuid

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Enum

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base

from app.models.enums import GateStatus


class Gate(Base):

    __tablename__ = "gates"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    terminal_id: Mapped[str] = mapped_column(
        ForeignKey("terminals.id")
    )

    gate_number: Mapped[str] = mapped_column(
        String(20),
        unique=True
    )

    status: Mapped[GateStatus] = mapped_column(
        Enum(GateStatus),
        default=GateStatus.AVAILABLE
    )

    terminal = relationship(
        "Terminal",
        back_populates="gates"
    )

    flights = relationship(
        "Flight",
        back_populates="gate"
    )