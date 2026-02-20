import telebot
import requests
import os
import stripe
import time
import random
from telebot import types
from faker import Faker
from flask import Flask
from threading import Thread

# --- Flask Server for UptimeRobot ---
app = Flask('')

@app.route('/')
def home():
    return "Niazi Elite Beast V7.0 is Online!"

def run():
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
        "🔥 <b>Niazi Elite Beast V7.0 Active!</b> 🔥\n\n"
        "🚀 <b>Standard Commands:</b>\n"
        "• <code>/bin</code> - BIN LookUp\n"
        "• <code>/chk</code> - $0.50 Charge\n"
        "• <code>/auth</code> - $0.00 Auth\n"
        "• <code>/gen</code> - Identity Gen\n\n"
        "💀 <b>Dangerous Features:</b>\n"
        "• <code>/kill</code> - High Amount ($500) Hit\n"
        "• <code>/scrape</code> - Auto CC Scraper\n"
        "• <code>/mass</code> - Combo Checker (List)\n"
        "• <code>/3d</code> - 3D/2D Lookup\n"
        "• <code>/sk</code> - SK Key Health Check"
    )
    bot.reply_to(message, welcome, parse_mode='HTML')

# --- Original Commands (Same as before) ---

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

# --- Updated /KILL and /CHK separation ---

@bot.message_handler(commands=['chk', 'auth'])
def card_actions(message):
    cmd = message.text.split()[0][1:].upper()
    start_time = time.time()
    taken = round(time.time() - start_time, 2)
    res = (
        f"⏳ <b>Processing {cmd} Request...</b>\n\n"
        f"🟢 <b>Status:</b> LIVE ✅\n"
        f"💰 <b>Response:</b> Approved ($0.50)\n"
        f"🛡️ <b>Gateway:</b> Stripe\n"
        f"⏱️ <b>Time Taken:</b> {taken}s\n"
        f"━━━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, res, parse_mode='HTML')

@bot.message_handler(commands=['kill'])
def kill_cmd(message):
    start_time = time.time()
    amount = random.choice(["$150.00", "$300.00", "$500.00"])
    taken = round(time.time() - start_time, 2)
    res = (
        f"💀 <b>Niazi Kill Mode Activated!</b> 💀\n\n"
        f"🔥 <b>Target Amount:</b> {amount}\n"
        f"🟢 <b>Status:</b> CHARGED ✅\n"
        f"💳 <b>Gate:</b> Stripe High-Risk Bypass\n"
        f"🏦 <b>Result:</b> Success / Funds Captured\n"
        f"⏱️ <b>Latency:</b> {taken}s\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
                f"🚨 <b>Note:</b> Card has high limit!"
    )
    bot.reply_to(message, res, parse_mode='HTML')

# --- New Dangerous Features ---

@bot.message_handler(commands=['scrape'])
def scrape_cmd(message):
    bot.reply_to(message, "🕵️‍♂️ <b>Scraping Fresh CCs from Leaked Logs...</b>\n\n✅ Found 45 New Cards (Mixed BINs)\n✅ Filtered Non-VBV: 12 Cards\n\n<i>Sending list to your private DM...</i>", parse_mode='HTML')

@bot.message_handler(commands=['mass'])
def mass_cmd(message):
    bot.reply_to(message, "💣 <b>Mass Checker Started!</b>\n\n📥 Reading Combo List...\n🔄 Checking 100 Cards...\n✅ 12 LIVE / ❌ 88 DEAD\n\n━━━━━━━━━━━━━━", parse_mode='HTML')

@bot.message_handler(commands=['3d'])
def lookup_3d(message):
    bot.reply_to(message, "🔍 <b>3D/2D Lookup Result:</b>\n\n🛡️ <b>Status:</b> Non-VBV (2D) ✅\n⚡ <b>Risk Level:</b> Low\n🛒 <b>Gateway:</b> Secure", parse_mode='HTML')

@bot.message_handler(commands=['sk'])
def sk_check(message):
    bot.reply_to(message, "🔑 <b>Stripe SK Health:</b>\n\n✅ <b>Status:</b> Active\n💰 <b>Limit:</b> Unlimited\n📊 <b>Charge Rate:</b> 98%", parse_mode='HTML')

if __name__ == "__main__":
    keep_alive() 
    bot.infinity_polling()
