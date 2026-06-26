from pydantic import BaseModel


class AirportCreate(BaseModel):
    airport_code: str
    airport_name: str
    city: str
    country: str


class AirportResponse(AirportCreate):
    id: str

    class Config:
        from_attributes = True