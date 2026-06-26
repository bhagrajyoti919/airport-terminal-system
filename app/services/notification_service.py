from app.models.notification import Notification


def create_notification(
    db,
    flight_id,
    recipient,
    message
):

    obj = Notification(
        flight_id=flight_id,
        recipient=recipient,
        message=message
    )

    db.add(obj)

    db.commit()

    db.refresh(obj)

    return obj