from utils import RedisClient


class ChatService:
    redis_client = RedisClient()

    def enter_chant_room(self, chat_room_name: str):
        print(chat_room_name)

    def on_message(self, message: str):
        print(message)
