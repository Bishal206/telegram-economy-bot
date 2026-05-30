from telegram import Update
from telegram.ext import ContextTypes

from database import (
    create_user,
    get_user,
    update_balance,
    users
)

PETS = {
    "dog": 10000,
    "cat": 8000,
    "dragon": 500000,
    "phoenix": 1000000,
}


async def petshop(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = "🐾 Pet Shop\n\n"

    for pet, price in PETS.items():
        text += f"{pet} - {price} coins\n"

    await update.message.reply_text(text)


async def buypet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    if not context.args:
        return await update.message.reply_text(
            "Usage: /buypet petname"
        )

    pet = context.args[0].lower()

    if pet not in PETS:
        return await update.message.reply_text(
            "Pet not found."
        )

    data = get_user(user.id)

    if data["balance"] < PETS[pet]:
        return await update.message.reply_text(
            "Not enough coins."
        )

    update_balance(user.id, -PETS[pet])

    users.update_one(
        {"_id": user.id},
        {"$push": {"pets": pet}}
    )

    await update.message.reply_text(
        f"🐾 You bought a {pet}!"
    )


async def pets(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    data = get_user(user.id)

    pet_list = data.get("pets", [])

    if not pet_list:
        return await update.message.reply_text(
            "No pets."
        )

    text = "🐾 Your Pets\n\n"

    for pet in pet_list:
        text += f"• {pet}\n"

    await update.message.reply_text(text)