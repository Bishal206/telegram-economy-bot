from telegram import Update
from telegram.ext import ContextTypes

from database import get_user, create_user
from database import marriages


async def profile(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user

    create_user(user.id, user.first_name)

    data = get_user(user.id)

    marriage = marriages.find_one(
        {"user": user.id}
    )

    partner = "Single"

    if marriage:
        partner = marriage["partner_name"]

    inv_count = len(
        data.get("inventory", [])
    )

    text = (
        f"👤 {user.first_name}\n\n"
        f"💰 Wallet: {data['balance']}\n"
        f"🏦 Bank: {data['bank']}\n"
        f"🎒 Items: {inv_count}\n"
        f"❤️ Partner: {partner}"
    )

    await update.message.reply_text(text)