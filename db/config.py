from pymongo import MongoClient

bucket_name = 'search-engine-bd'
client = MongoClient('localhost', 27017)  
db = client['search_engine_db']