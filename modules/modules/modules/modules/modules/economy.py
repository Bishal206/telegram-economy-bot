import random


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


__all__ = ["bet"]

