import random
import asyncio
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = "8713691588:AAFdiP6PLGzedKlQyzF6jYTLITUq-Jt16p8"

BET_OPTIONS = [10, 20, 50, 100, 500, 1000]
COLORS = ["red", "green", "blue"]

users = {}  # user_id: {"color": str, "amount": int}
bets = {"red": 0, "green": 0, "blue": 0}

betting_open = False
time_left = 0

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "Welcome to Raja Coin Game 🎮\n\n"
        "Commands:\n"
        "/bet <color> <amount>\n"
        "Example: /bet red 100\n\n"
        f"Available coins: {BET_OPTIONS}"
    )

async def bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global betting_open

    if not betting_open:
        await update.message.reply_text("⛔ Betting closed, wait for next round")
        return

    user = update.message.from_user.id

    try:
        color = context.args[0].lower()
        amount = int(context.args[1])
    except:
        await update.message.reply_text("Usage: /bet red 100")
        return

    if color not in COLORS:
        await update.message.reply_text("❌ Invalid color (red/green/blue)")
        return

    if amount not in BET_OPTIONS:
        await update.message.reply_text(f"❌ Invalid amount. Choose from {BET_OPTIONS}")
        return

    users[user] = {"color": color, "amount": amount}
    bets[color] += amount

    await update.message.reply_text(f"✅ Bet placed: {color} | ₹{amount}")

async def game_loop(app):
    global betting_open, users, bets, time_left

    while True:
        users = {}
        bets = {"red": 0, "green": 0, "blue": 0}

        betting_open = True
        time_left = 30

        while time_left > 0:
            if time_left == 10:
                betting_open = False
            await asyncio.sleep(1)
            time_left -= 1

        result = random.choice(COLORS)

        for user_id, data in users.items():
            if data["color"] == result:
                win_amount = data["amount"] * 2
                try:
                    await app.bot.send_message(user_id, f"🎉 You won! Result: {result} | ₹{win_amount}")
                except:
                    pass
            else:
                try:
                    await app.bot.send_message(user_id, f"❌ You lost! Result: {result}")
                except:
                    pass

        await asyncio.sleep(5)

async def admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    msg = "📊 Admin Panel\n"
    msg += f"Total Bets:\nRed: ₹{bets['red']}\nGreen: ₹{bets['green']}\nBlue: ₹{bets['blue']}\n\n"
    msg += f"Users playing: {len(users)}"
    await update.message.reply_text(msg)

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("bet", bet))
    app.add_handler(CommandHandler("admin", admin))

    app.job_queue.run_once(lambda ctx: asyncio.create_task(game_loop(app)), 0)

    app.run_polling()

if name == "main":
    main()
