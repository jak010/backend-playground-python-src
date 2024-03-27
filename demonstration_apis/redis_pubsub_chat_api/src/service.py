import json

from redis.client import PubSub

from src.utils import RedisClient, AsyncRedisClient


class RedisChannelManager:
    redis_client = RedisClient()

    def __init__(self, channe_id: str):
        self.channel = f"channel:{channe_id}"

    def add_user(self, user_id: str, user_data: dict):
        self.redis_client.client.hset(
            name=self.channel,
            key=f"user_{user_id}",
            value=json.dumps(user_data, ensure_ascii=False)
        )

    def get_user(self, channel: str, user_id: str):
        self.redis_client.client.hget(name=channel, key=user_id)

    def get_chanels(self, channel_id: str):
        self.redis_client.client.hgetall(name=channel_id)

    def delete_user(self, user_id: str):
        user = f"user_{user_id}"
        self.redis_client.client.hdel(self.channel, user)


class RedisChannelHistory:
    async_redis_client = AsyncRedisClient()

    def __init__(self, channel_id: str):
        self.channel = f"channel_{channel_id}"

        self._init_cursor_start = -5
        self._init_cursor_end = -1

    async def mark_chat_read(self, user_id):
        logs = await self.async_redis_client.client.lrange(
            name=self.channel,
            start=-0,
            end=-1
        )
        for idx, log in enumerate(logs):
            payload = json.loads(log)

            if payload['sender'] != user_id:
                payload['receiver'] = user_id

            await self.async_redis_client.client.lset(
                name=self.channel,
                index=idx,
                value=json.dumps(payload, ensure_ascii=False)
            )

    async def read_latest_history_by_size(self, size: int) -> list[dict]:
        channel_history = await self.async_redis_client.client.lrange(
            name=self.channel,
            start=-size,
            end=-1
        )
        return sorted([json.loads(history) for history in channel_history], key=lambda x: x['timestamp'])

    async def read_latest_history_from_cursor(self, cursor):
        history_size = await self.read_messages_length()

        if abs(self._init_cursor_end) > abs(history_size):
            channel_history = await self.async_redis_client.client.lrange(name=self.channel, start=0, end=1)
            return sorted([json.loads(history) for history in channel_history], key=lambda x: x['timestamp'])

        channel_history = await self.async_redis_client.client.lrange(
            name=self.channel,
            start=self._init_cursor_start - cursor,
            end=-self._init_cursor_end - cursor
        )

        self._init_cursor_start -= cursor
        if self._init_cursor_end == -1:
            self._init_cursor_end -= cursor - 1
        else:
            self._init_cursor_end -= cursor

        return sorted([json.loads(history) for history in channel_history], key=lambda x: x['timestamp'])

    async def read_messages_length(self) -> int:
        return await self.async_redis_client.client.llen(name=self.channel)

    async def fetched_by_unread_message_with_user(self, user_id):
        channel_histories = await self.async_redis_client.client.lrange(
            name=self.channel, start=0, end=-1
        )
        unread_count = 0
        for channel_history in channel_histories:
            data = json.loads(channel_history)
            if data['sender'] == str(user_id) and data['receiver'] is None:
                unread_count += 1
        return unread_count

    async def add_log(self, message_payload: str):
        await self.async_redis_client.client.rpush(
            self.channel,
            message_payload
        )


class RedisChannelMessenger:
    async_redis_client = AsyncRedisClient()

    def __init__(self, channel_id: str):
        self.channel = f"channel_{channel_id}"

        self.connection: PubSub = self.async_redis_client.client.pubsub()

    async def send_message(self, message_payload: str):
        await self.async_redis_client.client.publish(
            self.channel,
            message=message_payload
        )

    async def listen(self):
        await self.connection.subscribe(self.channel)
        return await self.connection.get_message(ignore_subscribe_messages=True)
