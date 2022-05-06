from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017/')
db = client.sporty_bot

users = db.users
games = db.games
events = db.events
