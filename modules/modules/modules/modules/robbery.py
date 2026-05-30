import random
import time

from telegram import Update
from telegram.ext import ContextTypes

from database import (
    users,
    create_user,
    get_user,
    update_balance,
)

rob_cooldown = {}


async def rob(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Reply to someone's message to rob them."
        )
        return

    victim = update.message.reply_to_message.from_user

    if victim.id == user.id:
        await update.message.reply_text(
            "You can't rob yourself."
        )
        return

    create_user(victim.id, victim.first_name)

    now = time.time()

    if user.id in rob_cooldown:
        if now - rob_cooldown[user.id] < 600:
            await update.message.reply_text(
                "⏳ Wait before robbing again."
            )
            return

    robber_data = get_user(user.id)
    victim_data = get_user(victim.id)

    if victim_data["balance"] < 100:
        await update.message.reply_text(
            "Victim is too poor."
        )
        return

    rob_cooldown[user.id] = now

    success = random.randint(1, 100)

    if success <= 50:
        amount = random.randint(50, 300)

        update_balance(user.id, amount)
        update_balance(victim.id, -amount)

        await update.message.reply_text(
            f"💰 Success! You stole {amount} coins."
        )

    else:
        fine = random.randint(50, 200)

        update_balance(user.id, -fine)

        await update.message.reply_text(
            f"🚔 Caught! Lost {fine} coins."
        )
