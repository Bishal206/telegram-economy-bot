import random
import time

from telegram import Update
from telegram.ext import ContextTypes

from database import (
    create_user,
    get_user,
    update_balance,
    users
)


async def streak(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    data = get_user(user.id)

    now = int(time.time())

    last = data.get("last_streak", 0)

    if now - last < 86400:
        return await update.message.reply_text(
            "⏳ Come back tomorrow."
        )

    streak_count = data.get("streak", 0) + 1

    reward = streak_count * 500

    update_balance(user.id, reward)

    users.update_one(
        {"_id": user.id},
        {
            "$set": {
                "streak": streak_count,
                "last_streak": now
            }
        }
    )

    await update.message.reply_text(
        f"🔥 Streak: {streak_count}\n"
        f"🎁 Reward: {reward}"
    )


async def lottery(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    ticket = 1000

    data = get_user(user.id)

    if data["balance"] < ticket:
        return await update.message.reply_text(
            "Need 1000 coins."
        )

    update_balance(user.id, -ticket)

    lucky = random.randint(1, 100)

    if lucky == 50:
        prize = 100000

        update_balance(user.id, prize)

        await update.message.reply_text(
            f"🎉 JACKPOT!\nWon {prize}"
        )
    else:
        await update.message.reply_text(
            "🎫 Better luck next time."
        )