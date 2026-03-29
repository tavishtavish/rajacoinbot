import random
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

TOKEN = "8713691588:AAFdiP6PLGzedKlQyzF6jYTLITUq-Jt16p8"

BET_OPTIONS = [10, 20, 50, 100, 500, 1000]
COLORS = ["red", "green", "blue"]

users = {}
bets = {"red": 0, "green": 0, "blue": 0}
betting_open = False

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🎮 Raja Coin Game\n\nUse:\n/bet red 100\nCoins: 10,20,50,100,500,1000"
    )

async def bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global betting_open

    if not betting_open:
        await update.message.reply_text("⛔ Betting closed")
        return

    user = update.message.from_user.id

    try:
        color = context.args[0].lower()
        amount = int(context.args[1])
    except:
        await update.message.reply_text("Use: /bet red 100")
        return

    if color not in COLORS:
        await update.message.reply_text("❌ Invalid color")
        return

    if amount not in BET_OPTIONS:
        await update.message.reply_text("❌ Invalid amount")
        return

    users[user] = {"color": color, "amount": amount}
    bets[color] += amount

    await update.message.reply_text(f"✅ Bet placed: {color} ₹{amount}")

async def game_loop(application):
    global users, bets, betting_open

    while True:
        users.clear()
        bets["red"] = bets["green"] = bets["blue"] = 0

        betting_open = True
        print("🟢 Betting Open (30s)")

        for i in range(30):
            if i == 20:
                betting_open = False
                print("🔴 Last 10s - Closed")
            await asyncio.sleep(1)

        result = random.choice(COLORS)
        print("🎯 Result:", result)

        for user_id, data in users.items():
            try:
                if data["color"] == result:
                    win = data["amount"] * 2
                    await application.bot.send_message(user_id, f"🎉 You Won ₹{win} | {result}")
                else:
                    await application.bot.send_message(user_id, f"❌ Lost | {result}")
            except:
                pass

        await asyncio.sleep(5)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bet", bet))

    # 🔥 correct background start (NO asyncio.run)
    async def start_game(app):
        asyncio.create_task(game_loop(app))

    app.post_init = start_game

    print("Bot started 🚀")
    app.run_polling()

if __name__ == "__main__":
    main()
