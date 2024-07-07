import asyncio


async def f():
    try:
        while True:
            await asyncio.sleep(0)
    except asyncio.CancelledError:
        print("I was Cancelled!")
    else:
        return 123


coro = f()
coro.send(None)
coro.send(None)
coro.throw(asyncio.CancelledError)  # Task Cancellation을 수행한다.
# coro.throw(Exception, "blah")  # Task Cancellation을 수행한다.
