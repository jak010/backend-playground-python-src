import asyncio
import dataclasses
import datetime
import json
import random
import time
import uuid
from typing import Optional

from fastapi import WebSocket, Path, WebSocketDisconnect, Body, UploadFile
from fastapi.params import File
from fastapi.responses import JSONResponse
from fastapi.routing import APIRouter
from pydantic import BaseModel

from src.service import RedisChannelManager
from src.utils import AsyncRedisClient

websocket_router2 = APIRouter(tags=['API'], prefix="/v2")

async_redis_client = AsyncRedisClient()


@dataclasses.dataclass
class Message:
    message_id: str
    sender: str
    receiver: Optional[str]
    content: str
    timestamp: str

    def to_json(self):
        return json.dumps(dataclasses.asdict(self), ensure_ascii=False)
        # return dataclasses.asdict(self)


class Item(BaseModel):
    text: str


class ItemFile(BaseModel):
    file: str


from src.service import RedisChannelHistory, RedisChannelMessenger


@websocket_router2.post("/channel/{channel_id}/send-message")
async def send_message(
        channel_id: str = Path(),
        message: Item = Body(default=None)
):
    log = RedisChannelHistory(channel_id=channel_id)
    live_chat = RedisChannelMessenger(channel_id=channel_id)

    user_id = "1"  # 고정된 user_id가 message 전송
    message = {
        "timestamp": datetime.datetime.now().isoformat(),
        "sender": str(user_id),
        "message": message.text,
        "receiver": None
    }

    message = Message(
        message_id=str(uuid.uuid4()),
        sender=str(user_id),
        receiver=None,
        content="이상무",
        timestamp=datetime.datetime.now().isoformat()
    ).to_json()

    await live_chat.send_message(message)
    await log.add_log(message)

    return JSONResponse(status_code=200, content={})


@websocket_router2.post("/channel/{channel_id}/send-file")
async def send_file(
        channel_id: str = Path(),
        file: UploadFile = File(...)
):
    import base64

    to_base64 = base64.b64encode(await file.read())
    user_id = random.randint(1, 10000)
    messages = json.dumps(
        {
            "timestamp": datetime.datetime.now(),
            "sender": user_id,
            "file": to_base64.decode()
        }
    )
    await async_redis_client.client.handle_event(channel_id, messages)
    await async_redis_client.client.rpush(channel_id, messages)

    await file.close()

    return JSONResponse(status_code=200, content={})


async def receive_text_with_timeout(websocket, timeout):
    try:
        task = asyncio.ensure_future(websocket.receive_json())
        return await asyncio.wait_for(task, timeout=timeout)
    except asyncio.TimeoutError:
        return None


@websocket_router2.websocket("/channel/{channel_id}/{user_id}")
async def enter_room(
        websocket: WebSocket,
        channel_id: str = Path(),
        user_id: str = Path()
):
    RedisChannelManager(channel_id).add_user(user_id=user_id, user_data={"joined_time": time.time()})

    redis_channel_history = RedisChannelHistory(channel_id=channel_id)
    await websocket.accept()

    # 1. Connection이 성공하면 subscribe 시키기
    connection = RedisChannelMessenger(channel_id=channel_id)

    # 2. chatting 읽음 표시
    await redis_channel_history.mark_chat_read(user_id=user_id)

    # 3. subscribe 이후 최근 채팅 로그 보내주기
    datas = await redis_channel_history.read_latest_history_by_size(size=10)
    await websocket.send_json(datas)

    try:
        while True:
            data = await receive_text_with_timeout(websocket, 0.01)
            if data is not None:
                if data.get('method') is None:
                    await websocket.send_text(data='')

                elif data['method'] == 'unread':
                    # temp: 2번 유저가 안 읽은 메세지 수 보내주기
                    unread_count = await redis_channel_history.fetched_by_unread_message_with_user(user_id=user_id)
                    await websocket.send_text(data=json.dumps({"user": "2", "unread": unread_count}))

                elif data['method'] == 'length':
                    # chatting history의 수
                    message_length = await redis_channel_history.read_messages_length()
                    await websocket.send_text(data=json.dumps({"length": message_length}))

                elif data['method'] == 'read_more':
                    # chatting history의 수
                    channel_histories = await redis_channel_history.read_latest_history_from_cursor(10)
                    await websocket.send_json(data=channel_histories)


            else:
                if data := await connection.listen():
                    await websocket.send_json(json.loads(data['data']))
    except WebSocketDisconnect as e:
        RedisChannelManager(channel_id).delete_user(user_id=user_id)
