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


class ConnectionManager:
    def __init__(self):
        self.active_connections: list[WebSocket] = []

    async def connect(self, websocket: WebSocket):
        await websocket.accept()
        self.active_connections.append(websocket)

    def disconnect(self, websocket: WebSocket):
        self.active_connections.remove(websocket)

    async def send_personal_message(self, message: str, websocket: WebSocket):
        await websocket.send_text(message)

    async def broadcast(self, message: str):
        for connection in self.active_connections:
            await connection.send_text(message)
