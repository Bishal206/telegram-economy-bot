from telegram import Update
from telegram.ext import ContextTypes
from database import users


async def top(update: Update, context: ContextTypes.DEFAULT_TYPE):
    data = users.find().sort("balance", -1).limit(10)

    text = "🏆 Top Richest Players\n\n"

    pos = 1

    for user in data:
        text += f"{pos}. {user['name']} - {user['balance']} coins\n"
        pos += 1

    await update.message.reply_text(text)
