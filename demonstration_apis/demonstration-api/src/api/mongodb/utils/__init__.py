from datetime import datetime

import bson
import mongoengine
from pymongo import MongoClient
from bson import ObjectId


def get_sample_document(uri, db_name, collection_name):
    client = MongoClient(uri)
    db = client[db_name]
    collection = db[collection_name]
    sample_doc = collection.find_one()
    client.close()
    return sample_doc


def generate_model_class(name: str, sample_doc: dict):
    attrs = {}
    for field, value in sample_doc.items():
        # print(field, type(value))
        if isinstance(value, str):
            field_type = mongoengine.StringField()
        elif isinstance(value, int):
            field_type = mongoengine.IntField()
        elif isinstance(value, float):
            field_type = mongoengine.FloatField()
        elif isinstance(value, bool):
            field_type = mongoengine.BooleanField()
        elif isinstance(value, dict):
            field_type = mongoengine.DictField()
        elif isinstance(value, list):
            field_type = mongoengine.ListField()
        elif isinstance(value, ObjectId):
            field_type = mongoengine.ObjectIdField()
        elif isinstance(value, datetime):
            field_type = mongoengine.DateTimeField()
        elif isinstance(value, bson.decimal128.Decimal128):
            field_type = mongoengine.DecimalField()
        else:
            field_type = mongoengine.DictField()
        attrs[field] = field_type.__class__.__name__

    return attrs


# 예시 사용법
uri = 'mongodb://localhost:27017/'
db_name = 'sample_airbnb'
collection_name = 'listingsAndReviews'
sample_doc = get_sample_document(uri, db_name, collection_name)

model_name = 'ListingsAndReviews'
ListingsAndReviews = generate_model_class(model_name, sample_doc)

for k, v in ListingsAndReviews.items():
    attr_template = f'{k}={v}()'
    print(attr_template)
