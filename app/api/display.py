from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.flight import Flight


router = APIRouter(
    prefix="/display",
    tags=["Display Boards"]
)


@router.get("/departures")
def departures(
    db: Session = Depends(get_db)
):

    flights = db.query(
        Flight
    ).all()

    data = []

    for flight in flights:

        data.append(
            {
                "flight": flight.flight_number,
                "destination": flight.destination,
                "status": flight.status,
                "delay": flight.delay_minutes
            }
        )

    return data