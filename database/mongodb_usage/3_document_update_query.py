from pymongo import MongoClient

client = MongoClient(host="127.0.0.1", port=27017)

# Usage 12, 포지셔닝 오퍼레이터 (Projection)
database = client.get_database("test")
collection = database.get_collection("students")

collection.drop()
# Saved Data
collection.insert_many(
    [
        {"_id": 1, "grades": [85, 80, 80]},
        {"_id": 2, "grades": [88, 90, 92]},
        {"_id": 3, "grades": [85, 100, 90]}
    ]
)

# Usage01,  첫번쨰로 만나는 값을 82로 업데이트
# collection.update_one(
#     {"_id": 1, "grades": 80},
#     {"$set": {"grades.$": 82}}
# )

# Usage02, 조건에 맞는 모든 데이터 10씩 업데이트
# collection.update_one(
#     {},
#     {"$inc": {"grades.$[]": 10}}
# )

# Usage03,
collection.insert_many(
    [{
        "_id": 4,
        "grades": [
            {"grade": 80, "mean": 75, "std": 8},
            {"grade": 85, "mean": 90, "std": 5},
            {"grade": 85, "mean": 85, "std": 8},
        ]
    }]
)

collection.update_one(
    {"_id": 4, "grades.grade": 85},
    {"$set": {"grades.$.std": 6}}
)

collection.update_one(
    {"_id": 4, "grades": {"$elemMatch": {"grade": {"$gte": 85}}}},
    {"$set": {"grades.$[].grade": 100}}
)

# Usage04,
collection.insert_many(
    [{
        "_id": 6,
        "grades": [
            {"grade": 90, "mean": 75, "std": 8},
            {"grade": 87, "mean": 90, "std": 6},
            {"grade": 85, "mean": 85, "std": 8},
        ]
    }]
)

collection.update_many(
    filter={"_id": 6},
    update={"$set": {"grades.$[element].grade": 100}},
    array_filters=[{"element.grade": {"$gte": 87}}]
)

client.close()
