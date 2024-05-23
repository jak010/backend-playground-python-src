import motor.motor_asyncio

from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorDatabase, AsyncIOMotorClient, AsyncIOMotorClientSession
from functools import cached_property


class AsyncDocumenDBMangaer:
    DATABASE = "sample_airbnb"

    def __init__(self, collection):
        self.monogdb_url = "mongodb://localhost:27017"
        self.client = motor.motor_asyncio.AsyncIOMotorClient(self.monogdb_url)
        self._session: AsyncIOMotorClientSession = None

        self._collection = collection

    # async def client(self) -> AsyncIOMotorClient:
    #     return await motor.motor_asyncio.AsyncIOMotorClient(self.monogdb_url)

    # def database(self) -> AsyncIOMotorDatabase:
    #     return self.client.get_database("sample_airbnb")

    # def collection(self):
    #     return self.database.get_collection("listingsAndReviews")

    async def __aenter__(self):
        await self.client.start_session()

        return self.client.get_database(name=self.DATABASE).get_collection(self._collection)

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        self.client.close()


# client.get_database(name=self.DATABASE).get_collection(icollection)
#
# return.start_session()


class DocumentDBRepository:
    collection = "sample_airbnb"

    def __init__(self):
        self.manger = AsyncDocumenDBMangaer(self.collection)

    async def find_by_id(self, _id: str):
        async with AsyncDocumenDBMangaer(self.collection) as client:
            print(client)

    # result = await self.collection.find_one({"_id": "1001265"})
    # return result
