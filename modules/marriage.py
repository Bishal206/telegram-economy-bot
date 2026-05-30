from telegram import Update
from telegram.ext import ContextTypes
from database import (marriages, create_user)


async def marry(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    if not update.message.reply_to_message:
        await update.message.reply_text(
            "Reply to a user to marry them."
        )
        return

    partner = update.message.reply_to_message.from_user

    if partner.id == user.id:
        await update.message.reply_text(
            "You can't marry yourself."
        )
        return

    if marriages.find_one({"user": user.id}):
        await update.message.reply_text(
            "You are already married."
        )
        return

    if marriages.find_one({"user": partner.id}):
        await update.message.reply_text(
            "That user is already married."
        )
        return

    marriages.insert_one(
        {
            "user": user.id,
            "partner": partner.id,
            "partner_name": partner.first_name,
        }
    )

    marriages.insert_one(
        {
            "user": partner.id,
            "partner": user.id,
            "partner_name": user.first_name,
        }
    )

    await update.message.reply_text(
        f"💍 {user.first_name} married {partner.first_name}!"
    )


async def partner(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    data = marriages.find_one({"user": user.id})

    if not data:
        await update.message.reply_text(
            "💔 You are single."
        )
        return

    await update.message.reply_text(
        f"❤️ Partner: {data['partner_name']}"
    )


async def divorce(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    data = marriages.find_one({"user": user.id})

    if not data:
        await update.message.reply_text(
            "You are not married."
        )
        return

    marriages.delete_many(
        {
            "$or": [
                {"user": user.id},
                {"user": data["partner"]},
            ]
        }
    )

    await update.message.reply_text(
        "💔 Divorce completed."
    )
