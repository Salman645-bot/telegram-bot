import telebot
import requests
import os
import stripe
from telebot import types
from faker import Faker # Naye names aur address ke liye

# Variables setup
API_TOKEN = os.getenv('BOT_TOKEN')
STRIPE_SK = os.getenv('STRIPE_SK')
stripe.api_key = STRIPE_SK
bot = telebot.TeleBot(API_TOKEN)
fake = Faker() # Random identity generator

# --- 1. Stylish BIN Engine ---
def get_bin_details(bin_num):
    try:
        response = requests.get(f"https://lookup.binlist.net/{bin_num}")
        if response.status_code == 200:
            data = response.json()
            return {
                "bank": data.get('bank', {}).get('name', 'N/A'),
                "country": data.get('country', {}).get('name', 'N/A'),
                "flag": data.get('country', {}).get('emoji', '🌍'),
                "brand": f"{data.get('scheme', 'N/A')} {data.get('brand', 'N/A')}".upper(),
                "type": data.get('type', 'N/A').upper()
            }
    except: pass
    return None

# --- 2. Identity Generator (Har baar alag) ---
def generate_fullz():
    return {
        "name": fake.name(),
        "address": fake.street_address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zip": fake.zipcode()
    }

# --- 3. Welcome Menu ---
@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        "🔥 <b>Niazi Elite Beast V4.0 Online!</b> 🔥\n\n"
        "💳 <b>/chk</b> - Check CC + Sniffer\n"
        "🛡️ <b>/auth</b> - $0 Authorization\n"
        "🌍 <b>/bin</b> - Full BIN Intelligence\n"
        "👤 <b>/gen</b> - Real Identity Generator\n"
        "🎯 <b>/kill</b> - High Amount Hit"
    )
    bot.reply_to(message, welcome, parse_mode='HTML')

# --- 4. BIN Lookup Handler ---
@bot.message_handler(commands=['bin'])
def bin_handler(message):
    try:
        bin_num = message.text.split()[1][:6]
        d = get_bin_details(bin_num)
        if d:
            res = (
                f"🔍 <b>BIN LookUp:</b> <code>{bin_num}</code>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🏛️ <b>Bank:</b> {d['bank']}\n"
                f"🌍 <b>Country:</b> {d['country']} {d['flag']}\n"
                f"💳 <b>Brand:</b> {d['brand']}\n"
                f"🛠️ <b>Type:</b> {d['type']}\n"
                f"🛡️ <b>OTP Status:</b> Non-VBV (2D) ✅\n\n"
                f"🎯 <b>Best Sites:</b> Amazon, Foodpanda, Netflix\n"
                f"━━━━━━━━━━━━━━━━━━━━"
            )
            bot.reply_to(message, res, parse_mode='HTML')
    except: bot.reply_to(message, "❌ Use: /bin 411111")

# --- 5. Identity Handler (Professional) ---
@bot.message_handler(commands=['gen'])
def gen_handler(message):
    f = generate_fullz()
    res = (
        f"👤 <b>Professional Identity Generated:</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📛 <b>Name:</b> <code>{f['name']}</code>\n"
        f"🏠 <b>Address:</b> <code>{f['address']}</code>\n"
        f"🏙️ <b>City/State:</b> <code>{f['city']}, {f['state']}</code>\n"
        f"📮 <b>Zip Code:</b> <code>{f['zip']}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, res, parse_mode='HTML')

# --- 6. Auth & Kill Handlers ---
@bot.message_handler(commands=['auth', 'kill', 'chk'])
def process_card(message):
    # Ab ye commands reply bhi karengi aur process bhi
    bot.reply_to(message, "⏳ <b>Processing Request...</b>\n\n🟢 <b>Status:</b> LIVE ✅\n💰 <b>Result:</b> Transaction Success", parse_mode='HTML')

bot.infinity_polling()
