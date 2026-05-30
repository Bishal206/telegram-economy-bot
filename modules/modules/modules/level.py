from telegram import Update
from telegram.ext import ContextTypes

from database import (
    create_user,
    get_user
)


async def level(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    data = get_user(user.id)

    xp = data.get("xp", 0)
    lvl = data.get("level", 1)

    await update.message.reply_text(
        f"⭐ Level: {lvl}\n"
        f"✨ XP: {xp}"
    )