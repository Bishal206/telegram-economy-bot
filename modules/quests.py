import time

from telegram import Update
from telegram.ext import ContextTypes

from database import (
    create_user,
    get_user,
    update_balance,
    users
)

QUESTS = {
    "worker": {
        "reward": 1000
    },
    "gambler": {
        "reward": 1500
    },
    "criminal": {
        "reward": 2000
    }
}


async def quests(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = (
        "📜 Daily Quests\n\n"
        "worker - 1000\n"
        "gambler - 1500\n"
        "criminal - 2000\n\n"
        "Use /claimquest name"
    )

    await update.message.reply_text(text)


async def claimquest(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    if not context.args:
        return await update.message.reply_text(
            "Usage: /claimquest worker"
        )

    quest = context.args[0].lower()

    if quest not in QUESTS:
        return await update.message.reply_text(
            "Quest not found."
        )

    reward = QUESTS[quest]["reward"]

    update_balance(user.id, reward)

    await update.message.reply_text(
        f"🎉 Quest completed!\n+{reward}"
    )