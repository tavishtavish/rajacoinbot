from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, filters, ContextTypes

TOKEN = 8713691588:AAFdiP6PLGzedKlQyzF6jYTLITUq-Jt16p8 

users = {}
bets = {"red": 0, "green": 0, "blue": 0}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome to Raja Coin Game 🎮\nSend: red / green / blue")

async def handle_bet(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user.id
    text = update.message.text.lower()

    if text in ["red", "green", "blue"]:
        bets[text] += 10
        users[user] = text
        await update.message.reply_text(f"Bet placed on {text}")
    else:
        await update.message.reply_text("Send red / green / blue only")

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT, handle_bet))

app.run_polling()
