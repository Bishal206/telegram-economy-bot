from telegram import Update
from telegram.ext import ContextTypes

from database import (
    create_user,
    get_user,
    update_balance,
    add_item,
    deposit_money,
    withdraw_money,
)

SHOP_ITEMS = {
    "phone": 5000,
    "laptop": 15000,
    "car": 50000,
    "house": 250000,
    "villa": 1000000,
}


async def shop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🛒 Shop\n\n"

    for item, price in SHOP_ITEMS.items():
        text += f"{item} - {price} coins\n"

    await update.message.reply_text(text)


async def buy(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    if not context.args:
        await update.message.reply_text(
            "Usage: /buy item"
        )
        return

    item = context.args[0].lower()

    if item not in SHOP_ITEMS:
        await update.message.reply_text(
            "Item not found."
        )
        return

    data = get_user(user.id)

    price = SHOP_ITEMS[item]

    if data["balance"] < price:
        await update.message.reply_text(
            "Not enough coins."
        )
        return

    update_balance(user.id, -price)
    add_item(user.id, item)

    await update.message.reply_text(
        f"✅ Purchased {item}"
    )


async def inventory(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    data = get_user(user.id)

    inv = data.get("inventory", [])

    if not inv:
        await update.message.reply_text(
            "Inventory is empty."
        )
        return

    text = "🎒 Inventory\n\n"

    for item in inv:
        text += f"• {item}\n"

    await update.message.reply_text(text)


async def deposit(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    if not context.args:
        return await update.message.reply_text(
            "Usage: /deposit amount"
        )

    amount = int(context.args[0])

    data = get_user(user.id)

    if amount > data["balance"]:
        return await update.message.reply_text(
            "Not enough balance."
        )

    deposit_money(user.id, amount)

    await update.message.reply_text(
        f"🏦 Deposited {amount}"
    )


async def withdraw(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    if not context.args:
        return await update.message.reply_text(
            "Usage: /withdraw amount"
        )

    amount = int(context.args[0])

    data = get_user(user.id)

    if amount > data["bank"]:
        return await update.message.reply_text(
            "Not enough bank balance."
        )

    withdraw_money(user.id, amount)

    await update.message.reply_text(
        f"💵 Withdrew {amount}"
    )


import time
from database import users


async def income(update, context):
    user = update.effective_user

    create_user(user.id, user.first_name)

    data = get_user(user.id)

    now = int(time.time())

    if now - data.get("last_income", 0) < 43200:
        return await update.message.reply_text(
            "⏳ Income already collected."
        )

    inv = data.get("inventory", [])

    reward = 0

    if "car" in inv:
        reward += 1000

    if "house" in inv:
        reward += 5000

    if "villa" in inv:
        reward += 20000

    if reward == 0:
        return await update.message.reply_text(
            "Buy assets first."
        )

    update_balance(user.id, reward)

    users.update_one(
        {"_id": user.id},
        {"$set": {"last_income": now}}
    )

    await update.message.reply_text(
        f"💵 Passive income: {reward}"
    )