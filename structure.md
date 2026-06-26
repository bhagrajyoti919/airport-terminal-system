# Airport Terminal System - Architecture Documentation

## Overview

This project consists of two main systems:

1. **Airport Terminal Backend** - FastAPI + PostgreSQL
2. **Airport Operations Simulation Dashboard** - React + React Flow

---

## System 1: Airport Terminal Backend

### Purpose
- Manage flights
- Manage gates
- Manage terminals
- Generate announcements
- Trigger events
- Simulate delays
- Update flight statuses
- Expose APIs through Swagger UI

---

## System 2: Airport Operations Simulation Dashboard

### Purpose
- Visualize backend events
- Show event flow animations
- Show gate occupancy
- Show flight movement
- Show announcement generation
- Show notification generation
- Show event propagation

### Architecture Flow
```
                FASTAPI BACKEND
                       │
                       │
                 WebSocket API
                       │
                       ▼
         AIRPORT OPERATIONS SIMULATOR
```

---

## Final Project Structure

```
airport-terminal-system/
├── backend/
│   ├── app/
│   │   ├── core/
│   │   │   ├── config.py
│   │   │   ├── database.py
│   │   │   ├── websocket_manager.py
│   │   │   └── logger.py
│   │   ├── models/
│   │   │   ├── airport.py
│   │   │   ├── terminal.py
│   │   │   ├── gate.py
│   │   │   ├── flight.py
│   │   │   ├── passenger.py
│   │   │   ├── airline.py
│   │   │   ├── announcement.py
│   │   │   ├── notification.py
│   │   │   ├── event.py
│   │   │   └── simulation.py
│   │   ├── schemas/
│   │   ├── services/
│   │   │   ├── flight_service.py
│   │   │   ├── gate_service.py
│   │   │   ├── terminal_service.py
│   │   │   ├── event_service.py
│   │   │   ├── notification_service.py
│   │   │   ├── announcement_service.py
│   │   │   ├── display_service.py
│   │   │   └── scheduler_service.py
│   │   ├── api/
│   │   │   ├── airport.py
│   │   │   ├── terminals.py
│   │   │   ├── gates.py
│   │   │   ├── flights.py
│   │   │   ├── announcements.py
│   │   │   ├── notifications.py
│   │   │   ├── simulation.py
│   │   │   └── websocket.py
│   │   ├── json_store/
│   │   │   ├── live_display_cache.json
│   │   │   ├── terminal_map.json
│   │   │   ├── simulation_state.json
│   │   │   └── fake_passengers.json
│   │   ├── scheduler/
│   │   │   └── flight_scheduler.py
│   │   └── seed/
│   │       └── fake_data.py
│   ├── main.py
│   ├── requirements.txt
│   └── .env
└── simulation-ui/
    ├── React
    ├── React Flow
    ├── Tailwind
    ├── WebSocket Client
    └── Event Visualizer
```

---

## Database Design

### Database Selection
- **PostgreSQL** - Stores permanent business data
- **JSON Files** - Stores simulation data

### Data Allocation
| Storage | Data Type |
|---------|-----------|
| PostgreSQL | Flights, Gates, Terminals, Events, Announcements |
| JSON | Simulation States, Node Coordinates, Display Layouts, Fake Passengers, Live Cache |

---

## Database Tables

### airports
| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Primary key |
| airport_code | String | Airport code (e.g., DXB, DEL) |
| airport_name | String | Airport name |
| city | String | City |
| country | String | Country |
| created_at | DateTime | Creation timestamp |

### terminals
| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Primary key |
| airport_id | UUID FK | Foreign key to airports |
| terminal_name | String | Terminal name (e.g., Terminal 1) |
| terminal_code | String | Terminal code |
| status | String | Terminal status |
| created_at | DateTime | Creation timestamp |

### gates
| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Primary key |
| terminal_id | UUID FK | Foreign key to terminals |
| gate_number | String | Gate number (e.g., A1, B5) |
| gate_type | String | Gate type |
| status | String | Gate status |
| current_flight_id | UUID FK | Foreign key to current flight |
| created_at | DateTime | Creation timestamp |

### airlines
| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Primary key |
| airline_code | String | Airline code (e.g., AI, UK) |
| airline_name | String | Airline name |
| country | String | Country |
| status | String | Airline status |

### flights
| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Primary key |
| airline_id | UUID FK | Foreign key to airlines |
| flight_number | String | Flight number |
| origin | String | Origin airport |
| destination | String | Destination airport |
| terminal_id | UUID FK | Foreign key to terminals |
| gate_id | UUID FK | Foreign key to gates |
| scheduled_departure | DateTime | Scheduled departure time |
| actual_departure | DateTime | Actual departure time |
| scheduled_arrival | DateTime | Scheduled arrival time |
| actual_arrival | DateTime | Actual arrival time |
| status | String | Flight status |
| delay_minutes | Integer | Delay in minutes |
| created_at | DateTime | Creation timestamp |

### passengers
| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Primary key |
| flight_id | UUID FK | Foreign key to flights |
| name | String | Passenger name |
| email | String | Email address |
| phone | String | Phone number |
| seat_no | String | Seat number |
| boarding_group | String | Boarding group |

*Note: Fake data only*

### announcements
| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Primary key |
| flight_id | UUID FK | Foreign key to flights |
| announcement_type | String | Type (BOARDING, FINAL_CALL, DELAY, GATE_CHANGE) |
| message | String | Announcement message |
| created_at | DateTime | Creation timestamp |
| played | Boolean | Whether announcement was played |

### notifications
| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Primary key |
| flight_id | UUID FK | Foreign key to flights |
| notification_type | String | Notification type |
| recipient | String | Recipient |
| message | String | Notification message |
| status | String | Notification status |
| created_at | DateTime | Creation timestamp |

### flight_events (Most Important Table)
| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Primary key |
| flight_id | UUID FK | Foreign key to flights |
| event_type | String | Event type (FLIGHT_DELAYED, BOARDING_STARTED, GATE_CHANGED, CANCELLED, FINAL_CALL) |
| old_value | String | Previous value |
| new_value | String | New value |
| event_time | DateTime | Event timestamp |
| created_by | String | Creator |

### display_boards
| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Primary key |
| board_name | String | Board name |
| board_type | String | Board type |
| terminal_id | UUID FK | Foreign key to terminals |
| last_updated | DateTime | Last update timestamp |

### simulation_logs
| Column | Type | Description |
|--------|------|-------------|
| id | UUID PK | Primary key |
| event_name | String | Event name |
| source_node | String | Source node |
| target_node | String | Target node |
| payload | JSON | Event payload |
| created_at | DateTime | Creation timestamp |

*Note: Used only by simulator*

---

## JSON Storage Files

### terminal_map.json
```json
{
  "terminal1": {
    "gates": ["A1", "A2", "A3"]
  }
}
```

### simulation_state.json
```json
{
  "current_event": "FLIGHT_DELAYED",
  "flight": "AI101",
  "gate": "A12"
}
```

### live_display_cache.json
```json
{
  "departures": [],
  "arrivals": []
}
```

### fake_passengers.json
```json
[
  {
    "name": "John Doe",
    "flight": "AI101"
  }
]
```

---

## Simulation Flow

### Example Scenario
1. Flight AI101 is scheduled for 10:00 AM
2. Admin delays the flight
3. API call: `POST /api/flights/{id}/delay` with body `{"delay_minutes": 90}`

### Backend Processing Flow
```
Flight Service
       │
       ▼
  Update Flight
       │
       ▼
  Create Event
       │
       ▼
Generate Announcement
       │
       ▼
Generate Notification
       │
       ▼
Update Display Board
       │
       ▼
WebSocket Broadcast
```

### Simulator Visualization Flow
```
Flight Service
     │
     ▼
Event Service
     │
     ▼
Announcement
     │
     ▼
Notification
     │
     ▼
Display Board
     │
     ▼
Passenger
```

Each node lights up and each connection animates for visual demonstration.

---

## Swagger Testing

When project runs, access Swagger UI at:
```
http://localhost:8000/docs
```

### Available Actions
- Create airport
- Create terminal
- Create gate
- Create flight
- Delay flight
- Cancel flight
- Change gate
- Start boarding
- Trigger final call

---

## Phase 1 Coding Order

1. **Step 1** - FastAPI Setup, PostgreSQL Setup, SQLAlchemy, Alembic
2. **Step 2** - Airport Model, Terminal Model, Gate Model, Flight Model
3. **Step 3** - CRUD APIs, Swagger Testing
4. **Step 4** - Flight Event Engine
5. **Step 5** - WebSockets
6. **Step 6** - Simulation Engine
7. **Step 7** - React Flow Visualization
8. **Step 8** - Animations (Delay, Announcement, Notification, Gate Change)

---

This architecture is large enough to look like a real airport operations platform and gives you both a strong backend project and an impressive visualization layer for demonstrations and interviews.
