from app.websocket.manager import manager


async def publish_event(
    event_type: str,
    payload: dict
):

    await manager.broadcast(
        {
            "event": event_type,
            "payload": payload
        }
    )