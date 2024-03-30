import asyncio
from time import sleep

from fastapi import APIRouter

concurrency_router = APIRouter(tags=["Conncurrency"], prefix="/api/v1/concurrency")


async def get_burgers(number: int):
    sleep(2)
    result = number
    return result


async def get_numbers(number):
    print(number)
    return number


@concurrency_router.get("/test")
async def read_burgers():
    # XXX: TC 1
    # buregers = await get_burgers(2)

    await asyncio.create_task(get_numbers(2))

    return 2
