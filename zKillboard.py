import asyncio
import websockets

async def hello():
    async with websockets.connect(
            'wss://zkillboard.com:2096') as websocket:
        # name = input("What's your name? ")

        await websocket.send('{"action":"sub","channel":"killstream"}')
        print("Request sent")

        greeting = await websocket.recv()
        print(f"{greeting}")

asyncio.get_event_loop().run_until_complete(hello())