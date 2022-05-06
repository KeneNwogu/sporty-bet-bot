import os
from pymongo import MongoClient

MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/'

client = MongoClient(MONGO_URI)
db = client.sporty_bot

users = db.users
games = db.games
events = db.events
