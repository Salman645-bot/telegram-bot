import telebot
import stripe
import os
import random
from telebot import types

# Railway Variables
API_TOKEN = os.getenv('BOT_TOKEN')
STRIPE_SK = os.getenv('STRIPE_SK')

stripe.api_key = STRIPE_SK
bot = telebot.TeleBot(API_TOKEN)

# --- Welcome Menu ---
@bot.message_handler(commands=['start'])
def send_welcome(message):
    welcome_text = (
        "🔥 <b>Niazi Elite Beast V3 Live!</b> 🔥\n\n"
        "🚀 <b>Available Services:</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💳 <b>/chk</b> - $0.50 Charge & Auto Fullz\n"
        "🌍 <b>/bin</b> - Global Site Suggester\n"
        "🎯 <b>/kill</b> - High Amount Hit\n"
        "👤 <b>/gen</b> - Identity Generator\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "👉 <i>Bas '/' dalo aur menu khul jaye ga.</i>"
    )
    bot.reply_to(message, welcome_text, parse_mode='HTML')

# --- BIN & Site Suggester ---
@bot.message_handler(commands=['bin'])
def bin_info(message):
    try:
        bin_num = message.text.split()[1][:6]
        res = (
            f"🏛️ <b>BIN Intelligence Report</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💳 <b>BIN:</b> <code>{bin_num}</code>\n"
            f"🛡️ <b>Type:</b> Non-VBV (2D) ✅\n\n"
            f"🎯 <b>Best Sites for this BIN:</b>\n"
            f"• 🛒 Amazon, AliExpress\n"
            f"• 🍔 Foodpanda, DoorDash\n"
            f"• 🎥 Netflix, Spotify\n\n"
            f"📊 <b>Success Ratio:</b> 98%\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        bot.reply_to(message, res, parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ Use: /bin 411111")

# --- Commands List Menu ---
def set_commands():
    commands = [
        types.BotCommand("start", "Main Menu 🏠"),
        types.BotCommand("chk", "Check Card ($0.50) 💳"),
        types.BotCommand("bin", "Site Suggester 🌍"),
        types.BotCommand("gen", "Identity Gen 👤"),
        types.BotCommand("kill", "Hit Mode 🎯")
    ]
    bot.set_my_commands(commands)

set_commands()
bot.infinity_polling()
