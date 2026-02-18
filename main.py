import telebot
from telebot import types
import random

# 🔑 Apni API Key yahan dalein
API_TOKEN = 'YOUR_TELEGRAM_BOT_TOKEN'
bot = telebot.TeleBot(API_TOKEN)

# --- 1. Stylish Menu & Commands Setup ---
def set_bot_commands():
    commands = [
        types.BotCommand("start", "Welcome & Services Menu 🏠"),
        types.BotCommand("chk", "Check Card ($0.50) + Fullz 💳"),
        types.BotCommand("auth", "Authorize Card ($0.00) 🛡️"),
        types.BotCommand("bin", "Global Site Suggester & Info 🌍"),
        types.BotCommand("gen", "Generate Fake Identity 👤"),
        types.BotCommand("kill", "Hit Card (High Amount) 🎯")
    ]
    bot.set_my_commands(commands)

# --- 2. Welcome Message (First Start) ---
@bot.message_handler(commands=['start'])
def welcome(message):
    welcome_msg = (
        "🔥 <b>Welcome to Niazi Elite Beast V3!</b> 🔥\n\n"
        "<i>Duniya ka sab se tez aur smart carding intelligence system.</i>\n\n"
        "🚀 <b>Hamari Ultra Pro Services:</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💳 <b>/chk</b> - $0.50 Balance Sniffer + Auto Fullz\n"
        "🛡️ <b>/auth</b> - Safe Check (Authorization Only)\n"
        "🌍 <b>/bin</b> - Global Site Suggester (2D/3D Search)\n"
        "👤 <b>/gen</b> - Identity Generator (Name/Addr/Zip)\n"
        "🎯 <b>/kill</b> - Card Hit Mode (High Success)\n"
        "━━━━━━━━━━━━━━━━━━━━\n\n"
        "📢 <b>Note:</b> Bot khud bataye ga kaunsi BIN kis site par 100% chal rahi hai!\n"
        "👉 Bas <b>'/'</b> dalo aur menu khul jaye ga."
    )
    bot.reply_to(message, welcome_msg, parse_mode='HTML')

# --- 3. BIN Lookup & Global Site Suggester ---
@bot.message_handler(commands=['bin'])
def bin_info(message):
    try:
        bin_num = message.text.split()[1][:6]
        # Fake suggestions based on logic for demo
        res = (
            f"🏛️ <b>BIN Intelligence Report</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"💳 <b>BIN:</b> <code>{bin_num}</code>\n"
            f"🏳️ <b>Country:</b> USA 🇺🇸 | <b>Level:</b> Infinite\n"
            f"🛡️ <b>OTP Status:</b> <b>Non-VBV (2D) - NO OTP!</b> 🚀\n\n"
            f"🎯 <b>Best Success Sites (Global):</b>\n"
            f"• 🛒 <b>Amazon, AliExpress, Walmart</b>\n"
            f"• 🍔 <b>Foodpanda, DoorDash, UberEats</b>\n"
            f"• 🎥 <b>Netflix, Spotify, DigitalOcean</b>\n\n"
            f"📊 <b>Success Ratio:</b> 98% (Outstanding!)\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        bot.reply_to(message, res, parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ <b>Galti!</b> Use: /bin 411111", parse_mode='HTML')

# --- 4. Card Checker + Balance + Fullz ---
@bot.message_handler(commands=['chk'])
def check_card(message):
    try:
        cc_data = message.text.split()[1]
        # Logic: $0.50 charge simulation
        res = (
            f"💳 <b>Checker Result (Niazi Beast)</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"📝 <b>Card:</b> <code>{cc_data}</code>\n"
            f"🟢 <b>Status:</b> <b>LIVE (Charged $0.50)</b> ✅\n"
            f"💰 <b>Balance:</b> AVAILABLE (High Limit) 🔋\n\n"
            f"👤 <b>Generated Fullz (Billing Info):</b>\n"
            f"• <b>Name:</b> John Wick\n"
            f"• <b>Addr:</b> 123 Street Ave, New York\n"
            f"• <b>Zip:</b> 10001\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"🚀 <b>Verdict:</b> Perfect for 2D Sites!"
        )
        bot.reply_to(message, res, parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ <b>Galti!</b> Use: /chk cc|mm|yy|cvv", parse_mode='HTML')

# Commands set karein aur bot start karein
set_bot_commands()
bot.infinity_polling()
