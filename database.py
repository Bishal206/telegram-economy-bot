from pymongo import MongoClient
from config import MONGO_URL

client = MongoClient(MONGO_URL)

db = client["EconomyBot"]

users = db["users"]
marriages = db["marriages"]
shop = db["shop"]

def create_user(user_id, name):
    user_data = {
        "xp": 0,
        "level": 1,
        "last_daily": 0,
        "last_job": 0,
        "streak": 0,
        "last_streak": 0,
        "last_income": 0,
        "pets": [],
        "achievements": [],
    }
    if users.find_one({"_id": user_id}):
        return

    users.insert_one(
        {
            "_id": user_id,
            "name": name,
            "balance": 1000,
            "bank": 0,
            "inventory": [],
            "last_daily": 0,
            "last_work": 0,
            "last_rob": 0,
        }
    )


def get_user(user_id):
    return users.find_one({"_id": user_id})


def update_balance(user_id, amount):
    users.update_one(
        {"_id": user_id},
        {"$inc": {"balance": amount}}
    )


def update_bank(user_id, amount):
    users.update_one(
        {"_id": user_id},
        {"$inc": {"bank": amount}}
    )


def add_item(user_id, item):
        users.update_one(
        {"_id": user_id},
        {"$push": {"inventory": item}}
    )


def deposit_money(user_id, amount):
    users.update_one(
        {"_id": user_id},
        {
            "$inc": {
                "balance": -amount,
                "bank": amount
            }
        }
    )


def withdraw_money(user_id, amount):
    users.update_one(
        {"_id": user_id},
        {
            "$inc": {
                "balance": amount,
                "bank": -amount
            }
        }
    )


def set_balance(user_id, amount):
    users.update_one(
        {"_id": user_id},
        {"$set": {"balance": amount}}
    )


def update_user(user_id, data):
    users.update_one(
        {"_id": user_id},
        {"$set": data}
    )   
