from pymongo import MongoClient

client = MongoClient(host="127.0.0.1", port=27017)

database = client.get_database("test")

collection = database.get_collection("inventory")
collection.drop()

collection.insert_many(
    [
        {"item": "journal", "qty": 25, "tags": ["blank", "red"], "dim_cm": [14, 21]},
        {"item": "notebook", "qty": 50, "tags": ["red", "blank"], "dim_cm": [14, 21]},
        {"item": "paper", "qty": 100, "tags": ["red", "blank", "plain"], "dim_cm": [14, 21]},
        {"item": "planner", "qty": 75, "tags": ["blank", "red"], "dim_cm": [22.85, 30]},
        {"item": "postcard", "qty": 45, "tags": ["blue"], "dim_cm": [10, 15.25]},
    ]
)

# Usage02: 배열의 요소 순서까지 동일해야 결과가 나옴
# result = collection.find_one({"tags": ["red", "blank"]})


# Usage03: 모두 들어간 값을 찾는다면?
result = collection.find({"tags": {"$all": ["red", "blank"]}})

# Usage04 : SQL의 in 처럼 포함되는 값을 찾고 싶다면
result = collection.find({"tags": {"$in": ["red", "blank"]}})

# Usage05 : Document의 조건별로 검색할 수 있음
result = collection.find({"dim_cm": {"$gt": 15}})

# Usage06 : and 조건
result = collection.find({"dim_cm": {"$gt": 15, "$lt": 20}})  # 해당 조건에 만족하는 요소라면 다 찾게됨 (이는 AND 조건으로 찾음)

# Usage07: elemMatch를 사용하면 배열 요소 중 하나라도 조건에 맞는 요소를 찾음
result = collection.find({"dim_cm": {"$elemMatch": {"$gt": 15, "$lt": 20}}})

# Usage:08 : 배열 index(배열의 특정위치로)로 찾기
reesult = collection.find({"dim_cm.1": {"$lt": 20}})
"""
{'_id': ObjectId('665b25f175975daab2722467'), 'item': 'postcard', 'qty': 45, 'tags': ['blue'], 'dim_cm': [10, 15.25]}
"""

# Usage:09: 배열 크기에 대해서 조회하기
result = collection.find({"tags": {"$size": 3}})
"""
{'_id': ObjectId('665b2640aeeab0134e140364'), 'item': 'paper', 'qty': 100, 'tags': ['red', 'blank', 'plain'], 'dim_cm': [14, 21]}
"""

# Usage10, items.name과 items.quantity라는 두 가지 조건 모두를 만족하는 걸 찾는다.
database = client.get_database("sample_supplies")
collection = database.get_collection("sales")
result = collection.find(
    {
        "items.name": "binder",
        "items.quantity": {"$lte": 6},
    }
)

# Usage 11,
database = client.get_database("sample_supplies")
collection = database.get_collection("sales")
result2 = collection.find(
    {
        "items": {
            "$elemMatch": {
                "name": "binder",
                "quantity": {"$lte": 6}
            }
        }
    }
)

# Usage 12, 포지셔닝 오퍼레이터 (Projection)
database = client.get_database("sample_supplies")
collection = database.get_collection("sales")
result2 = collection.find(
    {
        "items": {
            "$elemMatch": {
                "name": "binder",
                "quantity": {"$lte": 6}
            }
        }
    },
    # Projectioning, 배열 요소중에 조건에 맞는 요소 하나만 반환
    {
        "saleDate": 1,
        "items.$": 1,
        "storeLocation": 1,
        "customer": 1
    }
)
for c in result2:
    print(c)

client.close()
