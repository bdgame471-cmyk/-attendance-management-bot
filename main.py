import os
import pytz
from datetime import datetime
from flask import Flask
from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    MessageHandler,
    filters,
    ContextTypes
)

# ১. Web Server (Health Check & Port Binding)
web_app = Flask(__name__)

@web_app.route('/')
def home():
    return "Office Attendance Telegram Bot is Live & Operational!"

# ২. টাইমজোন কনফিগারেশন (Asia/Dhaka)
DHAKA_TZ = pytz.timezone('Asia/Dhaka')

def get_dhaka_now():
    return datetime.now(DHAKA_TZ)

# ৩. মূল কীবোর্ড বাটন লেআউট
def get_main_keyboard():
    keyboard = [
        ['🟢 Start Work'],
        ['🚬 Smoke', '🚽 Toilet'],
        ['🍽️ Eat', '🪑 Back to Seat'],
        ['🔴 Off Work'],
        ['📊 Status']
    ]
    return ReplyKeyboardMarkup(keyboard, resize_keyboard=True)

# ৪. /start কমান্ড
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    welcome_text = "👋 **Welcome to Office Attendance Bot!**\n\nনিচের বাটনগুলো ব্যবহার করে আপনার অ্যাটেন্ডেন্স মার্ক করুন।"
    await update.message.reply_text(
        welcome_text,
        parse_mode='Markdown',
        reply_markup=get_main_keyboard()
    )

# ৫. Start Work হ্যান্ডলার
async def start_work_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    now = get_dhaka_now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%I:%M:%S %p')

    msg = (
        f"🟢 **Start Work Confirmed**\n\n"
        f"👤 **Member:** {user.full_name}\n"
        f"📅 **Date:** {date_str}\n"
        f"⏰ **Start Time:** {time_str}"
    )
    await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=get_main_keyboard())

# ৬. Off Work হ্যান্ডলার (সরাসরি কনফার্ম হবে)
async def off_work_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user = update.effective_user
    now = get_dhaka_now()
    date_str = now.strftime('%Y-%m-%d')
    time_str = now.strftime('%I:%M:%S %p')

    msg = (
        f"🔴 **Off Work Confirmed**\n\n"
        f"👤 **Member:** {user.full_name}\n"
        f"📅 **Date:** {date_str}\n"
        f"⏰ **Off Work Time:** {time_str}"
    )
    await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=get_main_keyboard())

# ৭. অন্যান্য কীবোর্ড বাটনের হ্যান্ডলার
async def handle_buttons(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = update.message.text
    user = update.effective_user
    now = get_dhaka_now()
    time_str = now.strftime('%I:%M:%S %p')

    if text == '🟢 Start Work':
        await start_work_handler(update, context)
    elif text == '🔴 Off Work':
        await off_work_handler(update, context)
    elif text in ['🚬 Smoke', '🚽 Toilet', '🍽️ Eat', '🪑 Back to Seat']:
        msg = f"📌 **{text}**\n👤 **Member:** {user.full_name}\n⏰ **Time:** {time_str}"
        await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=get_main_keyboard())
    elif text == '📊 Status':
        msg = f"📊 **Status Update**\n👤 **Member:** {user.full_name}\n⏰ **Current Time:** {time_str}"
        await update.message.reply_text(msg, parse_mode='Markdown', reply_markup=get_main_keyboard())

def main():
    token = os.environ.get("BOT_TOKEN")
    if not token:
        print("Error: BOT_TOKEN is missing!")
        return

    application = Application.builder().token(token).build()

    application.add_handler(CommandHandler("start", start_command))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_buttons))

    print("Bot is starting...")
    application.run_polling()

if __name__ == '__main__':
    main()
