from telegram.ext import (
    Application,
    CommandHandler,
)

from modules.marriage import (
    marry,
    partner,
    divorce,
)

from modules.shop import (
    shop,
    buy,
    inventory,
    deposit,
    withdraw
)

from config import BOT_TOKEN
from modules.economy import (
    start,
    balance,
    daily,
    work,
    beg,
    bet,
)
from modules.admin import (
    give,
    setbal,
)
from modules.profile import profile 
from modules.robbery import rob
from modules.leaderboard import top
from modules.games import (
    coinflip,
    crime,
    job,
    cricket,
    dice,
    football,
    dart,
    basketball,
)
from modules.level import (
    level,
)
from modules.rewards import (
    streak,
    lottery,
)
from modules.shop import income
from modules.pets import (
    petshop,
    buypet,
    pets,
)
from modules.achievements import (
    achievements,
)
from modules.trade import (
    trade,
    accepttrade,
)
from modules.quests import (
    quests,
    claimquest,
)

app = Application.builder().token(BOT_TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(CommandHandler("balance", balance))
app.add_handler(CommandHandler("bal", balance))
app.add_handler(CommandHandler("daily", daily))
app.add_handler(CommandHandler("work", work))
app.add_handler(CommandHandler("beg", beg))
app.add_handler(CommandHandler("bet", bet))
app.add_handler(CommandHandler("rob", rob))
app.add_handler(CommandHandler("marry", marry))
app.add_handler(CommandHandler("partner", partner))
app.add_handler(CommandHandler("divorce", divorce))
app.add_handler(CommandHandler("shop", shop))
app.add_handler(CommandHandler("buy", buy))
app.add_handler(CommandHandler("inventory", inventory))
app.add_handler(CommandHandler("deposit", deposit))
app.add_handler(CommandHandler("withdraw", withdraw))
app.add_handler(CommandHandler("profile", profile))
app.add_handler(CommandHandler("give", give))
app.add_handler(CommandHandler("setbal", setbal))
app.add_handler(CommandHandler("level", level))
app.add_handler(CommandHandler("coinflip", coinflip))
app.add_handler(CommandHandler("crime", crime))
app.add_handler(CommandHandler("job", job))
app.add_handler(CommandHandler("cricket", cricket))
app.add_handler(CommandHandler("dice", dice))
app.add_handler(CommandHandler("football", football))
app.add_handler(CommandHandler("dart", dart))
app.add_handler(CommandHandler("basketball", basketball))
app.add_handler(CommandHandler("streak", streak))
app.add_handler(CommandHandler("lottery", lottery))
app.add_handler(CommandHandler("income", income))
app.add_handler(CommandHandler("petshop", petshop))
app.add_handler(CommandHandler("buypet", buypet))
app.add_handler(CommandHandler("pets", pets))
app.add_handler(CommandHandler("achievements", achievements))
app.add_handler(CommandHandler("trade", trade))
app.add_handler(CommandHandler("accepttrade", accepttrade))
app.add_handler(CommandHandler("quests", quests))
app.add_handler(CommandHandler("claimquest", claimquest))
print("Bot Started")

app.run_polling()

if __name__ == "__main__":
    main()
