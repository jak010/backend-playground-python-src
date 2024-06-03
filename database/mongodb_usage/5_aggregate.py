from pymongo import MongoClient
import datetime

client = MongoClient(host="127.0.0.1", port=27017)

database = client.get_database("test")
collection = database.get_collection("orders")

# 이름별 총 판매된 수량을 확인하자.
documents = collection.aggregate(
    [
        {
            "$match": {"size": "medium"}
        },
        {
            "$group": {
                "_id": {"$getField": "name"},
                "totalQuantity": {
                    "$sum": {"$getField": "quantity"}
                }
            }
        }
    ]
)
documents = collection.aggregate(
    [
        {
            "$match": {"size": "medium"}
        },
        {
            "$group": {
                "_id": "$name",
                "totalQuantity": {
                    "$sum": "$quantity"
                }
            }
        }
    ]
)
# 2020년도, 2년간 데이터들에 대해서 날짜별 매출과 평균판매수량
documents = collection.aggregate(
    [
        {
            "$match": {
                "date": {
                    "$gte": datetime.datetime(2020, 1, 30),
                    "$lt": datetime.datetime(2022, 1, 30)
                }
            }
        },
        {
            "$group": {
                "_id": {
                    "$dateToString": {
                        "format": "%Y-%m-%d", "date": "$date"
                    }
                },
                "totalOrderValue": {
                    "$sum": {
                        "$multiply": ["$price", "$quantity"]
                    }
                },
                "averageOrderQuantity": {
                    "$avg": "$quantity"
                }
            }
        },
        {
            "$sort": {
                "totalOrderValue": -1
            }
        }
    ]
)

# Book

collection = database.get_collection("books")
# books라는 배열안에 저자를 넣는다.
documents = collection.aggregate(
    [
        {
            "$group": {
                "_id": "$author",
                "books": {
                    "$push": "$title"
                }
            }
        }
    ]
)
# 값이 아닌 document를 넣고 싶다면?
documents = collection.aggregate(
    [
        {
            "$group": {
                "_id": "$author",
                "books": {
                    "$push": "$$ROOT"  # $$ROOT란?, 변수에 대한
                }
            }
        }
    ]
)

documents = collection.aggregate(

    [
        {
            "$group": {
                "_id": "$author",
                "books": {
                    "$push": "$$ROOT"  # $$ROOT란?, 변수에 대한
                },
            }
        },
        {
            "$addFields": {
                "totalCopies": {"$sum": "$books.copies"}
            }
        }
    ]
)

# join

database = client.get_database("test")
collection = database.get_collection("orders")

documents = collection.aggregate(
    [
        {
            "$lookup": {
                "from": "products",
                "localField": "productId",
                "foreignField": "id",
                "as": "data"  # join 대상 별칭
            }
        },
        {
            "$match": {
                "$expr": {  # expr은 배열을 이용하면 정상적인 결과를 얻을 수 없음
                    "$gt": ["$data.instock", "$price"]
                }
            }
        }
    ]
)
documents = collection.aggregate(
    [
        {
            "$lookup": {
                "from": "products",
                "localField": "productId",
                "foreignField": "id",
                "as": "data"  # join 대상 별칭
            }
        },
        {
            "$unwind": '$data'
        },

    ]
)

# 데이터를 sampling 하고 싶은 경우
database = client.get_database("sample_airbnb")
collection = database.get_collection("listingsAndReviews")

documents = collection.aggregate(
    [
        {
            "$sample": {"size": 3}
        },
        {
            "$project": {
                "name": 1,
                "summary": 1
            }
        }
    ]
)

# skip과 limit을 이용한 paging
documents = collection.aggregate(
    [
        {
            "$match": {"property_type": "Apartment"}
        },
        {
            "$sort": {
                "number_of_reviews": -1,
            }
        },
        {
            "$skip": 5
        },
        {
            "$limit": 5
        },
        {
            "$project": {
                "name": 1,
                "number_of_reviews": 1
            }
        }
    ]
)

database = client.get_database("test")
collection = database.get_collection("books")

# 새로운 Collection으로 생성하기
collection.aggregate(
    [
        {
            "$group": {
                "_id": "$author",
                "books": {"$push": "$title"}
            }
        },
        {
            "$out": "authors"
        }
    ]
)

# from pprint import pprint
#
# pprint([document for document in documents])
client.close()
