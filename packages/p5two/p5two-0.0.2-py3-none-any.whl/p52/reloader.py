import asyncio
from threading import Thread
from websockets.server import serve

browser = None


async def handler(websocket):
    global browser
    async for message in websocket:
        if message == "BROWSER":
            browser = websocket
        if message == "RELOAD":
            await browser.send(message)


async def main():
    async with serve(handler, "localhost", 8765):
        await asyncio.Future()  # run forever


def launchReloadServer():
    t = Thread(target=lambda: asyncio.run(main()), args=[], daemon=True)
    t.start()
