import asyncio
import websockets


async def listen():

    uri = "ws://localhost:8000/ws"

    async with websockets.connect(uri) as websocket:

        print("Connected")

        while True:

            message = await websocket.recv()

            print(message)


asyncio.run(listen())