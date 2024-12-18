from pymongo import MongoClient
from env_handler import env

client = MongoClient(env.DB_URL)
db = client[env.DB_NAME]