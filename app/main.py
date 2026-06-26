from app.core.database import Base
from app.core.database import engine

import app.models


Base.metadata.create_all(bind=engine)

from fastapi import FastAPI

from app.core.config import settings

from app.api.health import router as health_router
from app.api.airport import router as airport_router
from app.api.terminal import router as terminal_router
from app.api.gate import router as gate_router
from app.api.airline import router as airline_router
from app.api.flight import router as flight_router
from app.api.event import router as event_router
from app.api.websocket import router as websocket_router
from app.api.display import router as display_router
from app.services.scheduler_service import start_scheduler
from app.api.debug import router as debug_router
app = FastAPI(
    title=settings.APP_NAME,
    version="1.0.0"
)


app.include_router(health_router)
app.include_router(airport_router)
app.include_router(terminal_router)
app.include_router(gate_router)
app.include_router(airline_router)
app.include_router(flight_router)
app.include_router(event_router)
app.include_router(websocket_router)
app.include_router(display_router)
app.include_router(debug_router)
@app.get("/")
def root():

    return {
        "message": "Airport Terminal Management System"
    }

@app.on_event("startup")
async def startup():

    start_scheduler()