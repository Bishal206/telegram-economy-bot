import os

BOT_TOKEN = os.getenv("BOT_TOKEN")

MONGO_URL = os.getenv("MONGO_URL")

OWNER_ID = int(os.getenv("OWNER_ID", "0"))
