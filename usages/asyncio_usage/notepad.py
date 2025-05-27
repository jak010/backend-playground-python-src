import asyncio


def foo(test):
    return f"{test}"


async def main():
    loop = asyncio.get_event_loop()
    r = await loop.run_in_executor(None, foo, ("test",))

    print(r)


if __name__ == '__main__':
    asyncio.run(main())
