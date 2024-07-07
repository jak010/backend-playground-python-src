import asyncio


async def f():
    await asyncio.sleep(0)
    return 123


async def main():
    result = await f()
    return result


# Wrojng
# if __name__ == '__main__':
#     print(main())


if __name__ == '__main__':
    asyncio.run(main())
