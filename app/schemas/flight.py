from datetime import datetime

from pydantic import BaseModel


class FlightCreate(BaseModel):

    airline_id: str
    terminal_id: str
    gate_id: str

    flight_number: str

    origin: str
    destination: str

    scheduled_departure: datetime
    scheduled_arrival: datetime


class FlightResponse(FlightCreate):

    id: str

    class Config:
        from_attributes = True