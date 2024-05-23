import motor.motor_asyncio
from bson import ObjectId

MONGO_DETAILS = "mongodb://localhost:27017"

client = motor.motor_asyncio.AsyncIOMotorClient(MONGO_DETAILS)

database = client.get_database('sample_airbnb')

collection = database.get_collection("listingsAndReviews")

import asyncio


async def retreive_item(_id: str):
    result = await collection.find_one({"_id": "1001265"})

    for x in result:
        print(x)

    return result


if __name__ == '__main__':
    # print(retreive_item("1001265"))

    asyncio.run(retreive_item("1001265"))
