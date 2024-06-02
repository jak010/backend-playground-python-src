from pymongo import MongoClient

client = MongoClient(host="127.0.0.1", port=27017)

# 01. sample_mflix database의 movie collection 전체를 조회
database = client.get_database("sample_mflix")
collection = database.get_collection("movies")

# 02. movies collection의 Document의 수를 구한다.
c = collection.estimated_document_count()

# 03. movies collection 전체를 조회하는데, title, year, genres, runtime, rated 필드를 출력하고 _id 필드는 출력하지 않는다.
# - Projection
c = collection.find(
    {},
    {
        "title": 1,
        "year": 1,
        "genres": 1,
        "runtime": 1,
        "rated": 1,
        "_id": 0
    }
)

# 04. movies collection에서 runtime이 100분 이하인 Document
documents = collection.find({"runtime": {"$lt": 100}})
# for document in documents:
#     print(document["runtime"])

# 05, movies collection에서 runtime이 100분 이하이고 genres에 Drama가 포함되는 Document를 조회한다.
documents = collection.find(
    {
        "runtime": {"$lt": 100},
        "genres": "Drama"
    }
)
# for document in documents:
#     print(document['genres'])


# 06, movies collection에서 runtime이 100분 이하이고 genres가 Drama인 Document를 조회한다.
documents = collection.find(
    {
        "$and": [
            {"runtime": {"$lt": 100}},
            {"genres": "Drama"},
            {"genres": {"$size": 1}}
        ]
    },
    {"genres": 1}
)

# 07,  movies collection에서 runtime이 100분 이하이고 type이 series가 아니고  개봉연도가 2015년 익상이거나 1925 이하인 영화를찾는다.
documents = collection.find(
    {
        "$and": [
            {"runtime": {"$lte": 100}},
            {"type": {"$ne": 'series'}},
            {
                "$or": [
                    {"year": {"$gte": 2015}},
                    {"year": {"$lte": 1925}},
                ]
            }
        ],
    },
    {"runtime": 1, "type": 1, "year": 1}
).sort({"year": -1})

# 08, movies colelctions에서 viewr 평가가 4.5이상이거나 critic 평가가 9.5이상인 영화를찾고
#   - runtime이 가장 긴 순서대로 5개 document를 출력한다.
#   - 필드는 title, runtime, tomatoes, _id 필드를 출력한다.
documents = collection.find(
    {
        "$or": [
            {"tomatoes.viewer.rating": {"$gte": 4.5}},
            {"tomatoes.critic.rating": {"$gte": 9.5}},
        ]
    },
    {"title": 1, "runtime": 1, "tomatoes": 1}
).sort({"runtime": -1}).limit(5)

# for document in documents:
#     print(document)

# 09, sample_restuarants database의 restaurants collection에서 Queens에 있는 음식점 중에, A grade가 없는 음식점을 찾는다.
database = client.get_database("sample_restaurants")
collection = database.get_collection("restaurants")

documents = collection.find(
    {
        "borough": "Queens",
        "grades.grade": {"$ne": 'A'},
        "grades": {"$size": 3},
    },
    {
        "grades": 1, "_id": 0
    }
)

# 10, sample_restuarants database의 restaurants collection에서 Queens에 있는 음식점 중에, A와 Z가 같이 있는 음식점 조회.
documents = collection.find(
    {
        "$and": [
            {"borough": "Queens"},
            {"grades": {"$elemMatch": {'grade': 'A'}}},
            {"grades": {"$elemMatch": {'grade': 'Z'}}},
        ]
    },
    {"grades.grade": 1}
)
# for document in documents:
#     print(document)

# 11, sample_restuarants database의 restaurants collection에서 Queens에 있는 음식점 중에,
#      grades의 score가 하나라도 70이상인 document를 조회하고 grades 배열에는 70이 넘는 document 하나만 출력한다.
documents = collection.find(
    {
        "borough": "Queens",
        "grades.score": {"$gte": 70}
    },
    {
        "address": 1,
        "borough": 1,
        "cuisine": 1,
        "grades.$": 1,
        "name": 1,
        "restaurant_id": 1
    }
)
for document in documents:
    print(document)

client.close()
