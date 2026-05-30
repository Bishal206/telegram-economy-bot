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


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    await update.message.reply_text(
        f"Welcome {user.first_name}!\n\n"
        f"Use /balance to check coins."
    )


async def balance(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    data = get_user(user.id)

    await update.message.reply_text(
        f"💰 Balance: {data['balance']} coins"
    )

import time

async def daily(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    data = get_user(user.id)

    now = int(time.time())

    if now - data.get("last_daily", 0) < 86400:
        return await update.message.reply_text(
            "⏳ You can claim daily reward once every 24 hours."
        )

    reward = 1000

    update_balance(user.id, reward)

    users.update_one(
        {"user_id": user.id},
        {"$set": {"last_daily": now}}
    )

    await update.message.reply_text(
        f"🎁 Daily reward claimed!\n+{reward} coins"
    )


async def work(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    data = get_user(user.id)

    now = int(time.time())
    if now - data.get("last_work", 0) < 3600:
        return await update.message.reply_text(
            "⏳ You can work once every hour."
        )
        

    reward = random.randint(200, 800)

    update_balance(user.id, reward)

    users.update_one(
        {"user_id": user.id},
        {"$set": {"last_work": now}}
    )

    await update.message.reply_text(
        f"🛠 You worked and earned {reward} coins."
    )


async def beg(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    reward = random.randint(10, 100)

    update_balance(user.id, reward)

    await update.message.reply_text(
        f"🙏 Someone gave you {reward} coins."
    )


async def bet(update, context):
    user = update.effective_user

    create_user(user.id, user.first_name)

    if not context.args:
        await update.message.reply_text(
            "Usage: /bet amount"
        )
        return

    try:
        amount = int(context.args[0])
    except:
        await update.message.reply_text(
            "Enter a valid number."
        )
        return

    data = get_user(user.id)

    if amount <= 0:
        return

    if data["balance"] < amount:
        await update.message.reply_text(
            "Not enough coins."
        )
        return

    chance = random.randint(1, 100)

    if chance <= 45:
        update_balance(user.id, amount)

        await update.message.reply_text(
            f"🎉 You won {amount} coins!"
        )
    else:
        update_balance(user.id, -amount)

        await update.message.reply_text(
            f"💸 You lost {amount} coins."
        )
