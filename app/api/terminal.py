from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.terminal import Terminal

from app.schemas.terminal import TerminalCreate


router = APIRouter(
    prefix="/terminals",
    tags=["Terminals"]
)


@router.post("/")
def create_terminal(
    terminal: TerminalCreate,
    db: Session = Depends(get_db)
):

    obj = Terminal(
        airport_id=terminal.airport_id,
        terminal_name=terminal.terminal_name,
        terminal_code=terminal.terminal_code
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


@router.get("/")
def get_terminals(
    db: Session = Depends(get_db)
):
    return db.query(Terminal).all()