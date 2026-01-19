import os
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    ApplicationBuilder,
    CommandHandler,
    MessageHandler,
    ContextTypes,
    filters,
)

# نجيب التوكن من Environment
TOKEN = os.getenv("BOT_TOKEN")

if not TOKEN:
    raise ValueError("BOT_TOKEN not found in environment variables")

# /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    keyboard = [
        ["دكتور", "صيدلية"],
    ]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True)
    await update.message.reply_text(
        "مرحبا 👋\nاختار نوع الزيارة:",
        reply_markup=reply_markup,
    )

# استقبال الرسائل
async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text

    if text == "دكتور":
        await update.message.reply_text("اكتب اسم الدكتور:")
    elif text == "صيدلية":
        await update.message.reply_text("اكتب اسم الصيدلية:")
    else:
        await update.message.reply_text(
            f"تم تسجيل:\n{text}\n\n(توّة هذا مثال، وبنطوّروه بعد)"
        )

def main():
    app = ApplicationBuilder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))

    app.run_polling(close_loop=False)

if __name__ == "__main__":
    main()
