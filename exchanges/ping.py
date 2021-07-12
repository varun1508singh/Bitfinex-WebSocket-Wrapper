import asyncio
from time import sleep

import websockets


async def response(websocket, path):
    message = await websocket.recv()
    print(f"We got the message from the client: {message}")

    await websocket.send("I can confirm I got your message!")
    sleep(2)
    await websocket.send("I can confirm I got your message2!")
    sleep(2)
    await websocket.send("I can confirm I got your message3!")


start_server = websockets.serve(response, 'localhost', 1234)
asyncio.get_event_loop().run_until_complete(start_server)
asyncio.get_event_loop().run_forever()
