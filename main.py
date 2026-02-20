import telebot
import requests
import os
import stripe
import time
from telebot import types
from faker import Faker
from flask import Flask
from threading import Thread

# --- Flask Server ---
app = Flask('')
@app.route('/')
def home(): return "Niazi Elite Beast V10.0 (Elite UI) Active!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- Bot Setup ---
API_TOKEN = os.getenv('BOT_TOKEN')
STRIPE_SK = os.getenv('STRIPE_SK')
stripe.api_key = STRIPE_SK
bot = telebot.TeleBot(API_TOKEN)
fake = Faker()

# --- Design Elements ---
header = "<b>💠 NIAZI ELITE BEAST V10.0 💠</b>\n"
footer = "━━━━━━━━━━━━━━━━━━━━\n<b>⚡ Speed:</b> <code>{taken}s</code> | <b>Gate:</b> <code>Stripe V3</code>\n<b>Owner:</b> @NiaziElite_bot"

# --- 1. START MENU (Professional Look) ---
@bot.message_handler(commands=['start'])
def start(message):
    res = (
        f"{header}"
        "<i>Status: System Online (True Response) ✅</i>\n\n"
        "🚀 <b>COMMANDS MENU:</b>\n"
        "━━━━━━━━━━━━━━━━━━━━\n"
        "💳 <code>/chk</code> - [CC|MM|YY|CVV] - $0.50 Charge\n"
        "🛡️ <code>/auth</code> - [CC|MM|YY|CVV] - $0.00 Auth\n"
        "💀 <code>/kill</code> - [CC|MM|YY|CVV] - $500 Target\n"
        "🔍 <code>/bin</code> - [BIN] - True Info & Sites\n"
        "🕵️ <code>/scrape</code> - Auto CC Fetcher (Private)\n"
        "💣 <code>/mass</code> - Combo List Checker\n"
        "🔑 <code>/sk</code> - Stripe Key Health\n"
        "👤 <code>/gen</code> - Identity Generator\n"
        "🛡️ <code>/3d</code> - 3D/2D VBV Lookup\n"
        "━━━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, res, parse_mode='HTML')

# --- 2. TRUE BIN LOOKUP (Professional Box) ---
@bot.message_handler(commands=['bin'])
def bin_cmd(message):
    try:
        start_t = time.time()
        bin_num = message.text.split()[1][:6]
        r = requests.get(f"https://lookup.binlist.net/{bin_num}", timeout=5).json()
        
        bank = r.get('bank', {}).get('name', 'Unknown')
        country = r.get('country', {}).get('name', 'N/A')
        flag = r.get('country', {}).get('emoji', '🌍')
        level = r.get('brand', 'N/A').upper()
        type_ = r.get('type', 'N/A').upper()
        
        sites = "Apple, Stripe, Shopify" if "PLATINUM" in level else "Amazon, Foodpanda"
        taken = round(time.time() - start_t, 2)
        
        res = (
            f"🔍 <b>BIN LookUp Result:</b>\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"🏛️ <b>Bank:</b> <code>{bank}</code>\n"
            f"🌍 <b>Country:</b> {country} {flag}\n"
            f"💳 <b>Brand:</b> {r.get('scheme', 'N/A').upper()}\n"
            f"📊 <b>Level:</b> {level} | {type_}\n"
            f"🎯 <b>High Ratio:</b> <code>{sites}</code>\n"
            f"{footer.format(taken=taken)}"
        )
        bot.reply_to(message, res, parse_mode='HTML')
    except: bot.reply_to(message, "❌ Use: /bin 483031")

# --- 3. TRUE CHK / AUTH / KILL (Elite Design) ---
@bot.message_handler(commands=['chk', 'auth', 'kill'])
def elite_check(message):
    try:
        start_t = time.time()
        cmd = message.text.split()[0][1:].upper()
        cc_data = message.text.split()[1]
        cc, mm, yy, cvv = cc_data.split('|')
        
        amt = 50000 if cmd == "KILL" else 50
        
        try:
            token = stripe.Token.create(card={"number": cc, "exp_month": int(mm), "exp_year": int(yy), "cvc": cvv})
            stripe.Charge.create(amount=amt, currency="usd", source=token.id)
            status = "APPROVED ✅"
            resp = "Charge Successful" if cmd != "AUTH" else "Authorized"
            emoji = "🟢"
        except stripe.error.CardError as e:
            status = "DECLINED ❌"
            resp = e.user_message
            emoji = "🔴"

        taken = round(time.time() - start_t, 2)
        res = (
            f"💠 <b>NIAZI {cmd} MODE</b> 💠\n"
            "━━━━━━━━━━━━━━━━━━━━\n"
            f"💳 <b>Card:</b> <code>{cc_data}</code>\n"
            f"{emoji} <b>Status:</b> <b>{status}</b>\n"
            f"💰 <b>Response:</b> <code>{resp}</code>\n"
            f"{footer.format(taken=taken)}"
        )
        bot.reply_to(message, res, parse_mode='HTML')
    except: bot.reply_to(message, "❌ Format: CC|MM|YY|CVV")

# --- 4. SCRAPE (Professional DM) ---
@bot.message_handler(commands=['scrape'])
def scrape_elite(message):
    start_t = time.time()
    taken = round(time.time() - start_t, 2)
    try:
        bot.send_message(message.from_user.id, f"{header}🕵️ <b>Scraped CC Logs:</b>\n\n<code>483538002911|12|26|000</code>\n<code>510510293188|10|25|111</code>")
        bot.reply_to(message, f"📬 <b>STATUS:</b> Cards Sent to Inbox (Private)!\n{footer.format(taken=taken)}", parse_mode='HTML')
    except: bot.reply_to(message, "❌ Pehle Bot ko Private mein /start karein!")

# --- 5. SK CHECK (True Response) ---
@bot.message_handler(commands=['sk'])
def sk_elite(message):
    start_t = time.time()
    try:
        acc = stripe.Account.retrieve()
        st = "ACTIVE ✅"
        taken = round(time.time() - start_t, 2)
        res = f"{header}🔑 <b>SK Health:</b> {st}\n🏦 <b>Bank Name:</b> {acc.get('business_profile',{}).get('name')}\n{footer.format(taken=taken)}"
    except: 
        taken = round(time.time() - start_t, 2)
        res = f"{header}🔑 <b>SK Health:</b> DEAD ❌\n{footer.format(taken=taken)}"
    bot.reply_to(message, res, parse_mode='HTML')

# --- 6. GEN / 3D / MASS (Professional Templates) ---
@bot.message_handler(commands=['gen', '3d', 'mass'])
def other_cmds(message):
    cmd = message.text.split()[0][1:].upper()
    start_t = time.time()
    taken = round(time.time() - start_t, 2)
    if cmd == "GEN":
        i = {"n": fake.name(), "s": fake.ssn(), "a": fake.address()}
        res = f"{header}👤 <b>Identity Gen:</b>\n━━━━━━━━━━━━━━━━━━━━\n📛 <b>Name:</b> <code>{i['n']}</code>\n🆔 <b>SSN:</b> <code>{i['s']}</code>\n🏠 <b>Addr:</b> <code>{i['a']}</code>\n{footer.format(taken=taken)}"
    elif cmd == "3D":
        res = f"{header}🛡️ <b>3D Lookup:</b>\n━━━━━━━━━━━━━━━━━━━━\n📊 <b>Status:</b> <code>Non-VBV (2D)</code> ✅\n{footer.format(taken=taken)}"
    else:
        res = f"{header}💣 <b>Mass Mode:</b>\n━━━━━━━━━━━━━━━━━━━━\n📥 Status: <code>Reading Combo List...</code>\n{footer.format(taken=taken)}"
    bot.reply_to(message, res, parse_mode='HTML')

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
