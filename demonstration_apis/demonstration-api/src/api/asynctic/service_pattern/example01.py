import asyncio


async def pp1():  # rps 8550
    return "Hello world"


def pp2():  # rps 8550
    return "Hello world"


async def service_method01():
    # loop = asyncio.get_event_loop()
    # loop.create_task(pp)

    # task1 = asyncio.create_task(pp())
    # return task1

    asyncio.run(pp())
