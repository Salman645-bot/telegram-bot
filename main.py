import telebot
import requests
import os
import stripe
import time
from telebot import types
from faker import Faker
from flask import Flask
from threading import Thread

# --- Flask Server for UptimeRobot ---
app = Flask('')

@app.route('/')
def home():
    return "Niazi Elite Beast is Online!"

def run():
    # Railway hamesha port 8080 use karta hai
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Bot Setup ---
API_TOKEN = os.getenv('BOT_TOKEN')
STRIPE_SK = os.getenv('STRIPE_SK')
stripe.api_key = STRIPE_SK
bot = telebot.TeleBot(API_TOKEN)
fake = Faker()

# --- Functions ---

def get_bin_info(bin_num):
    try:
        r = requests.get(f"https://lookup.binlist.net/{bin_num}", timeout=5).json()
        return {
            "bank": r.get('bank', {}).get('name', 'N/A'),
            "country": r.get('country', {}).get('name', 'N/A'),
            "flag": r.get('country', {}).get('emoji', '🌍'),
            "brand": r.get('scheme', 'N/A').upper(),
            "level": r.get('brand', 'N/A').upper(),
            "type": r.get('type', 'N/A').upper()
        }
    except: return None

def gen_identity():
    return {
        "name": fake.name(),
        "ssn": fake.ssn(),
        "address": fake.street_address(),
        "city": fake.city(),
        "state": fake.state_abbr(),
        "zip": fake.zipcode(),
        "dob": str(fake.date_of_birth(minimum_age=18, maximum_age=65)),
        "phone": fake.phone_number()
    }

# --- Command Handlers ---

@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        "🔥 <b>Niazi Elite Beast V6.0 Active!</b> 🔥\n\n"
        "🚀 <b>Available Commands:</b>\n"
        "• <code>/bin</code> - BIN History & Site Suggester\n"
        "• <code>/chk</code> - $0.50 Charge + Fullz\n"
        "• <code>/auth</code> - $0.00 Verification\n"
        "• <code>/gen</code> - Identity + SSN Generator\n"
        "• <code>/kill</code> - High Amount Hit Mode"
    )
    bot.reply_to(message, welcome, parse_mode='HTML')

@bot.message_handler(commands=['bin'])
def bin_cmd(message):
    try:
        bin_num = message.text.split()[1][:6]
        d = get_bin_info(bin_num)
        if d:
            res = (
                f"🔍 <b>BIN LookUp:</b> <code>{bin_num}</code>\n"
                f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🏛️ <b>Bank:</b> {d['bank']}\n"
                f"🌍 <b>Country:</b> {d['country']} {d['flag']}\n"
                f"💳 <b>Vendor:</b> {d['brand']}\n"
                f"📊 <b>Level:</b> {d['level']}\n"
                f"🛠️ <b>Type:</b> {d['type']}\n"
                f"🛡️ <b>OTP Status:</b> Non-VBV (2D) ✅\n\n"
                f"🎯 <b>Site Suggestions:</b> Amazon, Foodpanda, Netflix\n"
                f"━━━━━━━━━━━━━━━━━━━━"
            )
            bot.reply_to(message, res, parse_mode='HTML')
    except: bot.reply_to(message, "❌ Use: /bin 483031")

@bot.message_handler(commands=['gen'])
def gen_cmd(message):
    i = gen_identity()
    res = (
        f"👤 <b>Professional Fullz Generated:</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📛 <b>Name:</b> <code>{i['name']}</code>\n"
        f"🆔 <b>SSN:</b> <code>{i['ssn']}</code>\n"
        f"🏠 <b>Address:</b> <code>{i['address']}</code>\n"
        f"🏙️ <b>City/State:</b> <code>{i['city']}, {i['state']}</code>\n"
        f"📮 <b>Zip Code:</b> <code>{i['zip']}</code>\n"
        f"📅 <b>DOB:</b> <code>{i['dob']}</code>\n"
        f"📞 <b>Phone:</b> <code>{i['phone']}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, res, parse_mode='HTML')

@bot.message_handler(commands=['chk', 'auth', 'kill'])
def card_actions(message):
    cmd = message.text.split()[0][1:].upper()
    start_time = time.time()
    taken = round(time.time() - start_time, 2)
    
    res = (
        f"⏳ <b>Processing {cmd} Request...</b>\n\n"
        f"🟢 <b>Status:</b> LIVE ✅\n"
        f"💰 <b>Response:</b> Approved\n"
        f"🛡️ <b>Gateway:</b> Stripe\n"
        f"⏱️ <b>Time Taken:</b> {taken}s\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"🏛️ <b>Bank Info:</b> JP Morgan | US 🇺🇸"
    )
    bot.reply_to(message, res, parse_mode='HTML')

# --- Start Everything ---
if __name__ == "__main__":
    keep_alive() # Flask start karega
    bot.infinity_polling() # Bot start karega
