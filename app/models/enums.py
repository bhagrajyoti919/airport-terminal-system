from enum import Enum


class FlightStatus(str, Enum):
    SCHEDULED = "SCHEDULED"
    CHECK_IN_OPEN = "CHECK_IN_OPEN"
    BOARDING = "BOARDING"
    FINAL_CALL = "FINAL_CALL"
    DEPARTED = "DEPARTED"
    ARRIVED = "ARRIVED"
    DELAYED = "DELAYED"
    CANCELLED = "CANCELLED"


class GateStatus(str, Enum):
    AVAILABLE = "AVAILABLE"
    OCCUPIED = "OCCUPIED"
    MAINTENANCE = "MAINTENANCE"


class TerminalStatus(str, Enum):
    ACTIVE = "ACTIVE"
    INACTIVE = "INACTIVE"