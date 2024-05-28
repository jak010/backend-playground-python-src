from fastapi.routing import APIRouter
from motor.motor_asyncio import AsyncIOMotorClient
from starlette.responses import JSONResponse
from pymongo import MongoClient

mongodb_router = APIRouter(tags=['MONGODB'], prefix="/api/v1/mongodb")


@mongodb_router.get("")
async def async_mongodb():
    client = AsyncIOMotorClient("mongodb://localhost:27017")

    # Usage 01, Method로 접근하기
    # d = client.get_database("sample_airbnb")
    # collection = d.get_collection("listingsAndReviews")
    # c = await collection.find_one({"_id": "10009999"})

    # Usage02, List Index로 접근하기
    # database = client["sample_airbnb"]
    # collection = database["listingsAndReviews"]
    # result = await collection.find_one({"_id": "10009999"})

    return JSONResponse(status_code=200, content={})


@mongodb_router.get("/v2")
def mongo_client_test():
    client = MongoClient("mongodb://localhost:27017/sample_airbnb").get_database()

    documents = client['listingsAndReviews'].find()

    for doc in documents:
        for k, v in doc.items():
            print(k, v)

    return JSONResponse(status_code=200, content={})
