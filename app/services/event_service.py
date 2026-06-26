from app.models.event import FlightEvent


def create_event(
    db,
    flight_id,
    event_type,
    old_value=None,
    new_value=None
):

    event = FlightEvent(
        flight_id=flight_id,
        event_type=event_type,
        old_value=old_value,
        new_value=new_value
    )

    db.add(event)

    db.commit()

    db.refresh(event)

    return event