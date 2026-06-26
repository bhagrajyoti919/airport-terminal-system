from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.event import FlightEvent


router = APIRouter(
    prefix="/events",
    tags=["Events"]
)


@router.get("/")
def get_events(
    db: Session = Depends(get_db)
):
    return (
        db.query(FlightEvent)
        .order_by(
            FlightEvent.created_at.desc()
        )
        .all()
    )