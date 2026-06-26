import uuid

from sqlalchemy import String
from sqlalchemy import ForeignKey
from sqlalchemy import Enum

from sqlalchemy.orm import Mapped
from sqlalchemy.orm import mapped_column
from sqlalchemy.orm import relationship

from app.core.database import Base

from app.models.enums import TerminalStatus


class Terminal(Base):

    __tablename__ = "terminals"

    id: Mapped[str] = mapped_column(
        String,
        primary_key=True,
        default=lambda: str(uuid.uuid4())
    )

    airport_id: Mapped[str] = mapped_column(
        ForeignKey("airports.id")
    )

    terminal_name: Mapped[str] = mapped_column(
        String(100)
    )

    terminal_code: Mapped[str] = mapped_column(
        String(20),
        unique=True
    )

    status: Mapped[TerminalStatus] = mapped_column(
        Enum(TerminalStatus),
        default=TerminalStatus.ACTIVE
    )

    airport = relationship(
        "Airport",
        back_populates="terminals"
    )

    gates = relationship(
        "Gate",
        back_populates="terminal"
    )