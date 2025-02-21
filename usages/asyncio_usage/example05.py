import asyncio


async def f():
    await asyncio.sleep(0)
    return 111


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    coro = f()
    loop.run_until_complete(coro)
