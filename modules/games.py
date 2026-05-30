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


def add_xp(user_id, xp):
    data = get_user(user_id)

    current_xp = data.get("xp", 0)
    level = data.get("level", 1)

    current_xp += xp

    need = level * 100

    if current_xp >= need:
        level += 1
        current_xp = 0

    users.update_one(
        {"_id": user_id},
        {
            "$set": {
                "xp": current_xp,
                "level": level
            }
        }
    )


async def coinflip(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    if not context.args:
        return await update.message.reply_text(
            "Usage: /coinflip amount"
        )

    amount = int(context.args[0])

    data = get_user(user.id)

    if amount > data["balance"]:
        return await update.message.reply_text(
            "Not enough coins."
        )

    if random.choice([True, False]):
        update_balance(user.id, amount)

        await update.message.reply_text(
            f"🪙 You won {amount} coins!"
        )
    else:
        update_balance(user.id, -amount)

        await update.message.reply_text(
            f"💸 You lost {amount} coins."
        )

    add_xp(user.id, 10)


async def crime(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    data = get_user(user.id)

    now = int(time.time())

    if now - data.get("last_crime", 0) < 3600:
        return await update.message.reply_text(
            "⏳ Crime cooldown active."
        )

    success = random.randint(1, 100)

    if success <= 60:
        reward = random.randint(500, 2500)

        update_balance(user.id, reward)

        await update.message.reply_text(
            f"🔫 Successful crime!\n+{reward}"
        )
    else:
        fine = random.randint(100, 1000)

        update_balance(user.id, -fine)

        await update.message.reply_text(
            f"🚔 Caught!\n-{fine}"
        )

    users.update_one(
        {"_id": user.id},
        {"$set": {"last_crime": now}}
    )

    add_xp(user.id, 15)


async def job(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    jobs = [
        "Programmer",
        "Doctor",
        "Pilot",
        "Chef",
        "Police Officer",
        "Engineer"
    ]

    job_name = random.choice(jobs)

    reward = random.randint(300, 1500)

    update_balance(user.id, reward)

    add_xp(user.id, 20)

    await update.message.reply_text(
        f"💼 Job: {job_name}\n"
        f"Earned {reward} coins."
    )


import random

async def dice(update, context):
    user = update.effective_user
    create_user(user.id, user.first_name)

    if not context.args:
        return await update.message.reply_text("Usage: /dice amount")

    amount = int(context.args[0])
    data = get_user(user.id)

    if amount > data["balance"]:
        return await update.message.reply_text("Not enough coins.")

    roll = random.randint(1, 6)

    if roll >= 4:
        update_balance(user.id, amount)
        await update.message.reply_text(
            f"🎲 Dice: {roll}\n💰 You won {amount} coins!"
        )
    else:
        update_balance(user.id, -amount)
        await update.message.reply_text(
            f"🎲 Dice: {roll}\n💸 You lost {amount} coins!"
        )


async def dart(update, context):
    user = update.effective_user
    create_user(user.id, user.first_name)

    if not context.args:
        return await update.message.reply_text("Usage: /dart amount")

    amount = int(context.args[0])
    data = get_user(user.id)

    if amount > data["balance"]:
        return await update.message.reply_text("Not enough coins.")

    hit = random.choice([True, False])

    if hit:
        update_balance(user.id, amount)
        await update.message.reply_text(
            f"🎯 Bullseye!\n💰 You won {amount} coins!"
        )
    else:
        update_balance(user.id, -amount)
        await update.message.reply_text(
            f"🎯 Missed!\n💸 You lost {amount} coins!"
        )


async def football(update, context):
    user = update.effective_user
    create_user(user.id, user.first_name)

    if not context.args:
        return await update.message.reply_text("Usage: /football amount")

    amount = int(context.args[0])
    data = get_user(user.id)

    if amount > data["balance"]:
        return await update.message.reply_text("Not enough coins.")

    goal = random.choice([True, False])

    if goal:
        update_balance(user.id, amount)
        await update.message.reply_text(
            f"⚽ GOAL!\n💰 You won {amount} coins!"
        )
    else:
        update_balance(user.id, -amount)
        await update.message.reply_text(
            f"⚽ Missed!\n💸 You lost {amount} coins!"
        )


async def basketball(update, context):
    user = update.effective_user
    create_user(user.id, user.first_name)

    if not context.args:
        return await update.message.reply_text("Usage: /basketball amount")

    amount = int(context.args[0])
    data = get_user(user.id)

    if amount > data["balance"]:
        return await update.message.reply_text("Not enough coins.")

    basket = random.choice([True, False])

    if basket:
        update_balance(user.id, amount)
        await update.message.reply_text(
            f"🏀 Basket!\n💰 You won {amount} coins!"
        )
    else:
        update_balance(user.id, -amount)
        await update.message.reply_text(
            f"🏀 Missed!\n💸 You lost {amount} coins!"
        )


async def cricket(update, context):
    user = update.effective_user
    create_user(user.id, user.first_name)

    if not context.args:
        return await update.message.reply_text("Usage: /cricket amount")

    amount = int(context.args[0])
    data = get_user(user.id)

    if amount > data["balance"]:
        return await update.message.reply_text("Not enough coins.")

    runs = random.choice([0, 1, 2, 3, 4, 6])

    if runs >= 4:
        update_balance(user.id, amount)
        await update.message.reply_text(
            f"🏏 Scored {runs} runs!\n💰 You won {amount} coins!"
        )
    else:
        update_balance(user.id, -amount)
        await update.message.reply_text(
            f"🏏 Scored {runs} runs!\n💸 You lost {amount} coins!"
        )
