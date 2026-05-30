from telegram import Update
from telegram.ext import ContextTypes

from database import (
    create_user,
    get_user
)


async def achievements(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    data = get_user(user.id)

    badges = []

    if data["balance"] >= 10000:
        badges.append("💰 Rich")

    if data["balance"] >= 100000:
        badges.append("👑 Millionaire")

    if len(data.get("inventory", [])) >= 5:
        badges.append("🎒 Collector")

    if len(data.get("pets", [])) >= 3:
        badges.append("🐾 Pet Master")

    if not badges:
        badges.append("No achievements yet.")

    await update.message.reply_text(
        "\n".join(badges)
    )