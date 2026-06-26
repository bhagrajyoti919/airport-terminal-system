from pydantic import BaseModel


class GateCreate(BaseModel):
    terminal_id: str
    gate_number: str


class GateResponse(GateCreate):
    id: str

    class Config:
        from_attributes = True