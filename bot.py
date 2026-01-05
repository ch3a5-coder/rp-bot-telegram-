import os
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, ContextTypes, filters

# ✅ Replace static token + ID by environment variable
BOT_TOKEN = os.getenv("BOT_TOKEN")
ADMIN_ID = int(os.getenv("ADMIN_ID"))

# Map user ↔ admin reply
user_map = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("💬 សួស្តី! អ្នកអាច chat នៅទីនេះបាន")

async def user_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.message.from_user
    text = update.message.text
    user_map[ADMIN_ID] = user.id
    await context.bot.send_message(chat_id=ADMIN_ID, text=f"👤 User ({user.id}):\n{text}")
    await update.message.reply_text("📨 សាររបស់អ្នកបានផ្ញើរទៅ admin ហើយ")

async def admin_reply(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if update.message.from_user.id == ADMIN_ID:
        user_id = user_map.get(ADMIN_ID)
        if user_id:
            await context.bot.send_message(chat_id=user_id, text=f"💬 RP:\n{update.message.text}")

app = ApplicationBuilder().token(BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.User(ADMIN_ID), user_message))
app.add_handler(MessageHandler(filters.TEXT & filters.User(ADMIN_ID), admin_reply))

app.run_polling()
