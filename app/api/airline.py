from fastapi import APIRouter
from fastapi import Depends

from sqlalchemy.orm import Session

from app.core.database import get_db

from app.models.airline import Airline

from app.schemas.airline import AirlineCreate


router = APIRouter(
    prefix="/airlines",
    tags=["Airlines"]
)


@router.post("/")
def create_airline(
    airline: AirlineCreate,
    db: Session = Depends(get_db)
):

    obj = Airline(
        airline_code=airline.airline_code,
        airline_name=airline.airline_name,
        country=airline.country
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)

    return obj


@router.get("/")
def get_airlines(
    db: Session = Depends(get_db)
):
    return db.query(Airline).all()