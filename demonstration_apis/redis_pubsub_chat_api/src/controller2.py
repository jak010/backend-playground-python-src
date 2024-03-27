import asyncio
import json
import random

from fastapi import WebSocket, Depends, Path, WebSocketDisconnect, Body, UploadFile
from fastapi.params import File
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter

from src.utils import ConnectionManager, AsyncRedisClient

websocket_router2 = APIRouter(tags=['API'], prefix="/v2")

async_redis_client = AsyncRedisClient()

from pydantic import BaseModel
import time


class Item(BaseModel):
    text: str


class ItemFile(BaseModel):
    file: str


@websocket_router2.post("/channel/{channel_id}/send-message")
async def send_message(
        channel_id: str = Path(),
        message: Item = Body(default=None)
):
    user_id = random.randint(1, 2)
    messages = json.dumps({
        "timestamp": time.time(),
        "sender": user_id,
        "message": message.text,
        "read_count": 1
    }, ensure_ascii=False)

    await async_redis_client.client.publish(channel_id, messages)
    await async_redis_client.client.rpush(channel_id, messages)

    return JSONResponse(status_code=200, content={})


@websocket_router2.post("/channel/{channel_id}/send-file")
async def send_file(
        channel_id: str = Path(),
        file: UploadFile = File(...)
):
    import base64

    to_base64 = base64.b64encode(await file.read())
    user_id = random.randint(1, 10000)
    messages = json.dumps({
        "timestamp": time.time(),
        "sender": user_id,
        "file": to_base64.decode()
    })
    await async_redis_client.client.publish(channel_id, messages)
    await async_redis_client.client.rpush(channel_id, messages)

    await file.close()

    return JSONResponse(status_code=200, content={})


async def receive_text_with_timeout(websocket, timeout):
    try:
        task = asyncio.ensure_future(websocket.receive_text())
        return await asyncio.wait_for(task, timeout=timeout)
    except asyncio.TimeoutError:
        return None


@websocket_router2.websocket("/channel/{channel_id}")
async def enter_room(
        websocket: WebSocket,
        manager: ConnectionManager = Depends(ConnectionManager),
        channel_id: str = Path(),
):
    await manager.connect(websocket, channel_id=channel_id)
    pubsub = async_redis_client.client.pubsub()
    await pubsub.subscribe(channel_id)

    try:
        # Connection 성공 시, Log 보내기
        messages = await async_redis_client.client.lrange(channel_id, -5, -1)
        await websocket.send_text(
            data=json.dumps(
                [str(message) for message in messages]
            ))

        while True:
            data = await receive_text_with_timeout(websocket, 0.01)
            if data is not None:
                await websocket.send_text(data='received')
            else:
                if message := await pubsub.get_message(ignore_subscribe_messages=True):
                    print(message)
                    await websocket.send_text(str(message['data']))

    except WebSocketDisconnect:
        manager.disconnect(websocket, channel_id=channel_id)
