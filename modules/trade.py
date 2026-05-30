from telegram import Update
from telegram.ext import ContextTypes

from database import (
    users,
    create_user,
    get_user
)

pending_trades = {}


async def trade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    if len(context.args) < 1:
        return await update.message.reply_text(
            "Usage: /trade item"
        )

    if not update.message.reply_to_message:
        return await update.message.reply_text(
            "Reply to a player."
        )

    target = update.message.reply_to_message.from_user

    item = context.args[0].lower()

    data = get_user(user.id)

    if item not in data.get("inventory", []):
        return await update.message.reply_text(
            "You don't own that item."
        )

    pending_trades[target.id] = {
        "from": user.id,
        "item": item
    }

    await update.message.reply_text(
        f"Trade request sent for {item}."
    )


async def accepttrade(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    if user.id not in pending_trades:
        return await update.message.reply_text(
            "No pending trade."
        )

    trade_data = pending_trades[user.id]

    seller = trade_data["from"]
    item = trade_data["item"]

    users.update_one(
        {"_id": seller},
        {"$pull": {"inventory": item}}
    )

    users.update_one(
        {"_id": user.id},
        {"$push": {"inventory": item}}
    )

    del pending_trades[user.id]

    await update.message.reply_text(
        f"Trade accepted.\nReceived {item}"
    )