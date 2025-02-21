import asyncio


#
# loop = asyncio.get_event_loop()
# loop2 = asyncio.get_event_loop()
#
# print(loop, loop2)
# print(loop == loop2)
# print(loop is loop2)


async def some_coro():
    return "Hello"


async def f():
    for i in range(10):
        task = asyncio.create_task(some_coro())
        print(task)
        return await task


if __name__ == '__main__':
    asyncio.run(f())
