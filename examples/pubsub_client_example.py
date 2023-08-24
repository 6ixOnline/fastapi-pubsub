import asyncio
import websockets


async def main():
    async with websockets.connect("ws://localhost:8000/ws/connected_clients") as websocket:
        while True:
            try:
                message = await websocket.recv()
                print(message)
            except Exception as ex:
                print(ex)
                break

asyncio.get_event_loop().run_until_complete(main())
