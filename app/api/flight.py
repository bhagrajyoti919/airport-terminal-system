from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import timedelta
from pydantic import BaseModel

from app.core.database import get_db
from app.models.flight import Flight
from app.schemas.flight import FlightCreate
from app.models.event_types import EventType
from app.services.event_service import create_event
from app.services.announcement_service import create_announcement
from app.services.notification_service import create_notification
from app.services.broadcast_service import publish_event
from app.scheduler.flight_scheduler import schedule_flight
from app.scheduler.flight_scheduler import (
    reschedule_flight
)

class DelayRequest(BaseModel):
    delay_minutes: int


router = APIRouter(
    prefix="/flights",
    tags=["Flights"]
)


@router.post("/")
def create_flight(
    flight: FlightCreate,
    db: Session = Depends(get_db)
):
    obj = Flight(
        airline_id=flight.airline_id,
        terminal_id=flight.terminal_id,
        gate_id=flight.gate_id,
        flight_number=flight.flight_number,
        origin=flight.origin,
        destination=flight.destination,
        scheduled_departure=flight.scheduled_departure,
        scheduled_arrival=flight.scheduled_arrival
    )

    db.add(obj)
    db.commit()
    db.refresh(obj)
    schedule_flight(db=db, flight=obj)

    return obj


@router.get("/")
def get_flights(
    db: Session = Depends(get_db)
):
    return db.query(Flight).all()


@router.post("/{flight_id}/delay")
async def delay_flight(
    flight_id: str,
    payload: DelayRequest,
    db: Session = Depends(get_db)
):
    flight = db.query(Flight).filter(
        Flight.id == flight_id
    ).first()

    if not flight:
        raise HTTPException(
            status_code=404,
            detail="Flight not found"
        )

    old_delay = flight.delay_minutes
    old_departure = flight.scheduled_departure

    flight.delay_minutes += payload.delay_minutes
    flight.scheduled_departure += timedelta(minutes=payload.delay_minutes)
    # Also update scheduled arrival to maintain flight duration
    flight.scheduled_arrival += timedelta(minutes=payload.delay_minutes)
    flight.status = "DELAYED"

    db.commit()
    reschedule_flight(
    db=db,
    flight=flight
)

    create_event(
        db=db,
        flight_id=flight.id,
        event_type=EventType.FLIGHT_DELAYED.value,
        old_value=str(old_delay),
        new_value=str(flight.delay_minutes)
    )

    message = (
        f"Flight {flight.flight_number} "
        f"has been delayed by "
        f"{payload.delay_minutes} minutes."
    )

    create_announcement(
        db=db,
        flight_id=flight.id,
        message=message
    )

    create_notification(
        db=db,
        flight_id=flight.id,
        recipient="all_passengers",
        message=message
    )

    await publish_event(
        event_type="FLIGHT_DELAYED",
        payload={
            "flight_id": flight.id,
            "flight_number": flight.flight_number,
            "origin": flight.origin,
            "destination": flight.destination,
            "status": flight.status,
            "delay_minutes": flight.delay_minutes,
            "new_scheduled_departure": flight.scheduled_departure.isoformat(),
            "new_scheduled_arrival": flight.scheduled_arrival.isoformat()
        }
    )

    return {
        "message": "Flight delayed",
        "delay": flight.delay_minutes,
        "new_scheduled_departure": flight.scheduled_departure,
        "new_scheduled_arrival": flight.scheduled_arrival
    }