import os
import telebot
import requests
import time
import stripe
from telebot import types 
from flask import Flask
from threading import Thread

# --- Railway Health Check ---
app = Flask('')
@app.route('/')
def home(): return "NiaziBin Bot is Online"

def run():
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Configuration ---
TOKEN = os.getenv("TOKEN")
RAPID_KEY = os.getenv("RAPIDAPI_KEY")
STRIPE_SK = os.getenv("STRIPE_SK")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start(message):
    welcome = f"<b>🔥 NiaziBin Bot Active!</b>\n\nFormat: <code>/chk card|mm|yy|cvv</code>"
    bot.reply_to(message, welcome)

@bot.message_handler(commands=['chk'])
def chk_handler(message):
    start_time = time.time()
    input_data = message.text.replace('/chk', '').strip()
    
    if "|" not in input_data:
        return bot.reply_to(message, "❌ Use <code>card|mm|yy|cvv</code>")
    
    try:
        parts = input_data.split('|')
        cc, mm, yy, cvv = parts[0], parts[1], parts[2], parts[3]
    except:
        return bot.reply_to(message, "❌ Invalid Format!")

    bot.send_chat_action(message.chat.id, 'typing')
    gateway = "RapidAPI-V2"
    status = "RETRY"

    # --- Stripe Logic ---
    if STRIPE_SK:
        try:
            stripe.api_key = STRIPE_SK
            stripe.PaymentMethod.create(
                type="card",
                card={"number": cc, "exp_month": int(mm), "exp_year": int(yy), "cvc": cvv},
            )
            status = "✅ <b>LIVE / HIT</b>"
            gateway = "Stripe-SK 🔥"
        except Exception as e:
            err = str(e)
            if "declined" in err or "incorrect_cvc" in err:
                status = "❌ <b>DEAD / DECLINED</b>"
                gateway = "Stripe-SK 🔥"
            else:
                status = "RETRY"

    # --- Fallback ---
    if status == "RETRY":
        try:
            url = "https://credit-card-validator2.p.rapidapi.com/validate-credit-card"
            headers = {"X-RapidAPI-Key": RAPID_KEY, "X-RapidAPI-Host": "credit-card-validator2.p.rapidapi.com"}
            res = requests.post(url, json={"cardNumber": cc}, headers=headers).json()
            status = "✅ <b>LIVE / HIT</b>" if res.get('isValid') else "❌ <b>DEAD / DECLINED</b>"
            gateway = "RapidAPI-V2"
        except:
            status = "⚠️ API ERROR"

    time_taken = round(time.time() - start_time, 2)
    reply = f"{status}\n━━━━━━━━━━━━\n💳 <b>Card:</b> <code>{input_data}</code>\n⚡ <b>Gateway:</b> {gateway}\n⏱️ <b>Time:</b> {time_taken}s"
    bot.reply_to(message, reply)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
