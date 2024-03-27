from fastapi import WebSocket

import redis
import aioredis
from functools import cached_property


class RedisConnector:
    HOST = "127.0.0.1"
    PORT = 6380
    DB = 1


class RedisClient(RedisConnector):

    def __init__(self):
        self.redis_client = redis.StrictRedis(
            host=self.HOST,
            port=self.PORT,
            db=self.DB,
            decode_responses=True
        )

    @cached_property
    def client(self) -> redis.StrictRedis:
        return self.redis_client


class AsyncRedisClient(RedisConnector):
    def __init__(self):
        self.async_redis_client = aioredis.StrictRedis(
            host=self.HOST,
            port=self.PORT,
            db=self.DB,
            decode_responses=True
        )

    @cached_property
    def client(self) -> redis.StrictRedis:
        return self.async_redis_client


class LiveUserConnection:
    channels = {}

    def add_user_on_channel(self, channel_id, websocket):
        if channel_id not in self.channels:
            self.channels[channel_id] = [websocket]
        else:
            self.channels[channel_id].append(websocket)

    def remove_user_on_channel(self, channel_id, websocket):
        self.channels[channel_id].remove(websocket)

        if not self.channels[channel_id]:
            self.channels.pop(channel_id)

    def show(self):
        print("Current Channels:", self.channels)


class ConnectionManager:
    """ FastAPI의 WebSocket Conncetion(Active) 관리 """

    live_user = LiveUserConnection()

    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket, channel_id: str):
        await websocket.accept()
        self.active_connections.append(websocket)

        self.live_user.add_user_on_channel(channel_id=channel_id, websocket=websocket)
        self.live_user.show()

    def disconnect(self, websocket: WebSocket, channel_id):
        self.active_connections.remove(websocket)
        self.live_user.remove_user_on_channel(channel_id=channel_id, websocket=websocket)
        self.live_user.show()

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
