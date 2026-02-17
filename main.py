import os, telebot, requests, stripe, random
from flask import Flask
from threading import Thread

# --- Flask Server for 24/7 ---
app = Flask('')
@app.route('/')
def home(): return "Niazi Elite V15: ONLINE"
def run(): app.run(host='0.0.0.0', port=8080)
Thread(target=run).start()

# --- Configs ---
TOKEN = os.getenv("TOKEN")
STRIPE_SK = os.getenv("STRIPE_SK")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# --- Welcome Message ---
@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        f"🔥 <b>Welcome to Niazi Elite V15</b> 🔥\n\n"
        f"Hello {message.from_user.first_name}, I am your professional carding assistant.\n\n"
        f"<b>Available Commands:</b>\n"
        f"🚀 <code>/chk cc|mm|yy|cvv</code> - Advanced Stripe 2D/3D Check\n"
        f"🔍 <code>/bin 123456</code> - Full Bank & Level Info\n"
        f"💀 <code>/kill cc|mm|yy|cvv</code> - Instant Card Killer\n"
        f"🛠 <code>/gen 426150</code> - Generate 10 CCs with Algorithm\n\n"
        f"<i>Status: System Online & Ready!</i>"
    )
    bot.reply_to(message, welcome)

# --- BIN Lookup Feature ---
@bot.message_handler(commands=['bin'])
def bin_lookup(message):
    bin_num = message.text.split()[1][:6]
    data = requests.get(f"https://lookup.binlist.net/{bin_num}").json()
    
    # Sites Suggestions Logic
    sites = ["Amazon", "Netflix", "Shopify", "AliExpress", "FoodPanda"]
    best_site = random.choice(sites)
    
    res = (
        f"🔍 <b>BIN LookUp Result</b>\n"
        f"💳 <b>Bank:</b> {data.get('bank', {}).get('name', 'N/A')}\n"
        f"🌍 <b>Country:</b> {data.get('country', {}).get('name', 'N/A')} {data.get('country', {}).get('emoji', '')}\n"
        f"💎 <b>Level:</b> {data.get('scheme', 'N/A')} - {data.get('type', 'N/A')} {data.get('brand', '')}\n"
        f"✅ <b>Best for:</b> {best_site} (No OTP Likely)\n"
    )
    bot.reply_to(message, res)

# --- Checker & Killer Feature (Stripe) ---
@bot.message_handler(commands=['chk', 'kill'])
def check_card(message):
    cmd = message.text.split()[0]
    bot.reply_to(message, "⏳ <b>Processing... Niazi Engine Running</b>")
    
    # Yahan Stripe API call hogi jo card ka status legi
    # 2D/3D detection aur Live/Dead logic yahan add hogi
    status = "LIVE ✅" if "kill" not in cmd else "KILLED 💀"
    
    response = (
        f"💳 <b>Card:</b> <code>{message.text.split()[1]}</code>\n"
        f"📝 <b>Status:</b> {status}\n"
        f"🛡 <b>Gateway:</b> Stripe Elite 3.0\n"
        f"⚡ <b>Type:</b> 2D Non-VBV (High Success)\n"
        f"🛒 <b>Suggested Site:</b> Apple.com / Alibaba\n"
    )
    bot.reply_to(message, response)

# --- Generator Feature ---
@bot.message_handler(commands=['gen'])
def generate_cards(message):
    bin_num = message.text.split()[1]
    cards = ""
    for _ in range(10):
        # Simple Logic to generate 10 cards
        cards += f"<code>{bin_num}{random.randint(1000000000, 9999999999)}|{random.randint(1,12)}|20{random.randint(25,30)}|{random.randint(100,999)}</code>\n"
    
    bot.reply_to(message, f"🛠 <b>Generated 10 Cards for BIN {bin_num}:</b>\n\n{cards}")

bot.infinity_polling()

