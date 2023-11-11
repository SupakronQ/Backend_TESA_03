from pymongo import MongoClient
from dotenv import load_dotenv
import os
load_dotenv()

# "mongodb://localhost:27017/test"
conn = MongoClient(os.getenv('Mongo_DB'))
