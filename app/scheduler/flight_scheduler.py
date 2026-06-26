from datetime import timedelta

from app.services.scheduler_service import scheduler

from app.models.flight import Flight

from app.services.event_service import create_event


def update_flight_status(
    db,
    flight_id,
    new_status
):

    flight = (
        db.query(Flight)
        .filter(
            Flight.id == flight_id
        )
        .first()
    )

    if not flight:
        return

    old_status = flight.status

    flight.status = new_status

    db.commit()

    create_event(
        db=db,
        flight_id=flight.id,
        event_type=f"STATUS_{new_status}",
        old_value=str(old_status),
        new_value=new_status
    )


def schedule_flight(
    db,
    flight
):

    departure = flight.scheduled_departure

    checkin_time = departure - timedelta(hours=2)

    boarding_time = departure - timedelta(minutes=40)

    final_call_time = departure - timedelta(minutes=15)

    scheduler.add_job(
        update_flight_status,
        trigger="date",
        id=f"{flight.id}_checkin",
        replace_existing=True,
        run_date=checkin_time,
        args=[
            db,
            flight.id,
            "CHECK_IN_OPEN"
        ]
    )

    scheduler.add_job(
        update_flight_status,
        trigger="date",
        id=f"{flight.id}_boarding",
        replace_existing=True,
        run_date=boarding_time,
        args=[
            db,
            flight.id,
            "BOARDING"
        ]
    )

    scheduler.add_job(
        update_flight_status,
        trigger="date",
        id=f"{flight.id}_final",
        replace_existing=True,
        run_date=final_call_time,
        args=[
            db,
            flight.id,
            "FINAL_CALL"
        ]
    )

    scheduler.add_job(
        update_flight_status,
        trigger="date",
        id=f"{flight.id}_departed",
        replace_existing=True,
        run_date=departure,
        args=[
            db,
            flight.id,
            "DEPARTED"
        ]
    )

def reschedule_flight(
    db,
    flight
):

    try:
        scheduler.remove_job(
            f"{flight.id}_checkin"
        )
    except:
        pass

    try:
        scheduler.remove_job(
            f"{flight.id}_boarding"
        )
    except:
        pass

    try:
        scheduler.remove_job(
            f"{flight.id}_final"
        )
    except:
        pass

    try:
        scheduler.remove_job(
            f"{flight.id}_departed"
        )
    except:
        pass

    schedule_flight(
        db=db,
        flight=flight
    )