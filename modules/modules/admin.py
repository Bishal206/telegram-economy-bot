from telegram import Update
from telegram.ext import ContextTypes

from config import OWNER_ID
from database import (
    create_user,
    get_user,
    update_balance,
    set_balance,
)


async def give(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if len(context.args) < 2:
        return await update.message.reply_text(
            "Usage: /give userid amount"
        )

    user_id = int(context.args[0])
    amount = int(context.args[1])

    update_balance(user_id, amount)

    await update.message.reply_text(
        f"Given {amount} coins."
    )


async def setbal(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.effective_user.id != OWNER_ID:
        return

    if len(context.args) < 2:
        return await update.message.reply_text(
            "Usage: /setbal userid amount"
        )

    user_id = int(context.args[0])
    amount = int(context.args[1])

    set_balance(user_id, amount)

    await update.message.reply_text(
        "Balance updated."
    )