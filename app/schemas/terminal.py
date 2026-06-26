from pydantic import BaseModel


class TerminalCreate(BaseModel):
    airport_id: str
    terminal_name: str
    terminal_code: str


class TerminalResponse(TerminalCreate):
    id: str

    class Config:
        from_attributes = True