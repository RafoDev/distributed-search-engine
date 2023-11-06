import json
from pymongo import MongoClient

client = MongoClient('localhost', 27017)  
client.drop_database('search_engine_db')