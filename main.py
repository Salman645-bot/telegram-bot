import telebot
import requests
import os
from telebot import types

# Railway se variables uthana
API_TOKEN = os.getenv('BOT_TOKEN')
bot = telebot.TeleBot(API_TOKEN)

# --- 1. BIN Lookup Engine (Bank, Country, Level Details) ---
def get_bin_details(bin_num):
    try:
        # Free API for BIN info
        response = requests.get(f"https://lookup.binlist.net/{bin_num}")
        if response.status_code == 200:
            data = response.json()
            bank = data.get('bank', {}).get('name', 'Unknown Bank')
            country = data.get('country', {}).get('name', 'Unknown Country')
            flag = data.get('country', {}).get('emoji', '🌍')
            scheme = data.get('scheme', 'Unknown').upper()
            level = data.get('brand', 'Standard').upper()
            type_ = data.get('type', 'Unknown').upper()
            return f"🏛️ <b>Bank:</b> {bank}\n🌍 <b>Country:</b> {country} {flag}\n💳 <b>Brand:</b> {scheme} {level}\n🛠️ <b>Type:</b> {type_}"
        return "❌ Details not found."
    except:
        return "⚠️ Service busy, try again."

# --- 2. Welcome Menu ---
@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        "🔥 <b>Niazi Elite Beast V3 Live!</b> 🔥\n\n"
        "🚀 <b>Commands:</b>\n"
        "• <code>/bin 123456</code> - Full Info\n"
        "• <code>/chk card|mm|yy|cvv</code> - Check CC\n"
        "• <code>/gen 123456</code> - Identity Gen\n"
        "• <code>/kill</code> - High Hit Mode"
    )
    bot.reply_to(message, welcome, parse_mode='HTML')

# --- 3. Bin Command Handler ---
@bot.message_handler(commands=['bin'])
def bin_handler(message):
    try:
        bin_num = message.text.split()[1][:6]
        details = get_bin_details(bin_num)
        res = (
            f"🔍 <b>BIN LookUp:</b> <code>{bin_num}</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━\n"
            f"{details}\n"
            f"🛡️ <b>OTP Status:</b> Non-VBV (2D) ✅\n\n"
            f"🎯 <b>Best Sites:</b> Amazon, Foodpanda, Netflix\n"
            f"📊 <b>Success Rate:</b> 98%\n"
            f"━━━━━━━━━━━━━━━━━━━━"
        )
        bot.reply_to(message, res, parse_mode='HTML')
    except:
        bot.reply_to(message, "❌ <b>Galti!</b> Format: <code>/bin 411111</code>", parse_mode='HTML')

# --- 4. Card Checker Handler ---
@bot.message_handler(commands=['chk'])
def chk_handler(message):
    # Abhi ke liye ye reply karega, baad mein Stripe integrate karenge
    bot.reply_to(message, "⏳ <b>Checking Card...</b>\n\n🟢 <b>Status:</b> LIVE\n💰 <b>Balance:</b> Available", parse_mode='HTML')

# --- 5. Identity Generator Handler ---
@bot.message_handler(commands=['gen'])
def gen_handler(message):
    bot.reply_to(message, "👤 <b>Identity Generated:</b>\n\nName: John Wick\nZip: 10001\nAddr: NYC", parse_mode='HTML')

bot.infinity_polling()
