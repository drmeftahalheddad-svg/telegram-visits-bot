import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import ApplicationBuilder, CommandHandler, MessageHandler, ContextTypes, filters

TOKEN = os.getenv("BOT_TOKEN")

users = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [["دكتور", "صيدلية"]]
    await update.message.reply_text(
        "اختار نوع الزيارة:",
        reply_markup=ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    )

async def handle_type(update: Update, context: ContextTypes.DEFAULT_TYPE):
    users[update.effective_user.id] = {"type": update.message.text}
    await update.message.reply_text("اكتب الاسم:")

async def handle_name(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = users.get(update.effective_user.id)
    if user and "name" not in user:
        user["name"] = update.message.text
        await update.message.reply_text("اكتب الملاحظة:")

async def handle_note(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = users.get(update.effective_user.id)
    if user and "note" not in user:
        user["note"] = update.message.text
        await update.message.reply_text(
            f"✅ تم تسجيل الزيارة\n"
            f"النوع: {user['type']}\n"
            f"الاسم: {user['name']}\n"
            f"الملاحظة: {user['note']}"
        )
        users.pop(update.effective_user.id)

app = ApplicationBuilder().token(TOKEN).build()

app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.Regex("^(دكتور|صيدلية)$"), handle_type))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_name))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_note))

app.run_polling()
