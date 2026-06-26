from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.airport import Airport

from app.schemas.airport import AirportCreate


router = APIRouter(
    prefix="/airports",
    tags=["Airports"]
)


@router.post("/")
def create_airport(
    airport: AirportCreate,
    db: Session = Depends(get_db)
):

    new_airport = Airport(
        airport_code=airport.airport_code,
        airport_name=airport.airport_name,
        city=airport.city,
        country=airport.country
    )

    db.add(new_airport)
    db.commit()
    db.refresh(new_airport)

    return new_airport


@router.get("/")
def get_airports(
    db: Session = Depends(get_db)
):
    return db.query(Airport).all()