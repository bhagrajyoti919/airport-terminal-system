from pydantic import BaseModel


class AirlineCreate(BaseModel):
    airline_code: str
    airline_name: str
    country: str


class AirlineResponse(AirlineCreate):
    id: str

    class Config:
        from_attributes = True