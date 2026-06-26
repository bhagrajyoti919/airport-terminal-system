from app.models.announcement import Announcement


def create_announcement(
    db,
    flight_id,
    message
):

    obj = Announcement(
        flight_id=flight_id,
        message=message
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj