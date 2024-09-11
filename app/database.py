from pymongo import MongoClient
from .exporter import MONGO_DB_LINK

import certifi

# Mongo DB Client
# Warning: use get_mongo_client method to get client access
_Mongo_Client = MongoClient(MONGO_DB_LINK, tlsCAFile=certifi.where())


def get_mongo_client(collection=None, from_ts=None, real_time_data=None):
    return _Mongo_Client
