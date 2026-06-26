from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.gate import Gate

from app.schemas.gate import GateCreate


router = APIRouter(
    prefix="/gates",
    tags=["Gates"]
)


@router.post("/")
def create_gate(
    gate: GateCreate,
    db: Session = Depends(get_db)
):

    obj = Gate(
        terminal_id=gate.terminal_id,
        gate_number=gate.gate_number
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


@router.get("/")
def get_gates(
    db: Session = Depends(get_db)
):
    return db.query(Gate).all()