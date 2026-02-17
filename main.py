import os, telebot, requests, time, stripe, random
from telebot import types 
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "NiaziBin Ultra Pro Max Active"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    Thread(target=run).start()

# --- Config ---
TOKEN = os.getenv("TOKEN")
RAPID_KEY = os.getenv("RAPIDAPI_KEY")
STRIPE_SK = os.getenv("STRIPE_SK")

if not TOKEN:
    print("❌ Token Missing!")
    exit()

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        f"<b>🌟 NIAZIBIN ULTRA PRO MAX 🌟</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"🤖 <b>Status:</b> <code>Premium Active</code>\n"
        f"💳 <b>Format:</b> <code>/chk card|mm|yy|cvv</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ <b>Checked By:</b> @{bot.get_me().username}"
    )
    bot.reply_to(message, welcome)

@bot.message_handler(commands=['chk'])
def chk_handler(message):
    start_time = time.time()
    input_data = message.text.replace('/chk', '').strip()
    if "|" not in input_data:
        return bot.reply_to(message, "❌ Use <code>card|mm|yy|cvv</code>")
    
    parts = input_data.split('|')
    cc, mm, yy, cvv = parts[0], parts[1], parts[2], parts[3]
    
    bot.send_chat_action(message.chat.id, 'typing')
    gateway, status = "RapidAPI-V2", "❌ <b>DEAD</b>"

    if STRIPE_SK:
        try:
            stripe.api_key = STRIPE_SK
            stripe.PaymentMethod.create(type="card", card={"number": cc, "exp_month": int(mm), "exp_year": int(yy), "cvc": cvv})
            status, gateway = "✅ <b>LIVE / HIT</b>", "Stripe-SK 🔥"
        except Exception as e:
            err = str(e)
            if "declined" in err or "incorrect_cvc" in err:
                status, gateway = "❌ <b>DECLINED</b>", "Stripe-SK 🔥"
            else:
                try:
                    headers = {"X-RapidAPI-Key": RAPID_KEY, "X-RapidAPI-Host": "credit-card-validator2.p.rapidapi.com"}
                    res = requests.post("https://credit-card-validator2.p.rapidapi.com/validate-credit-card", json={"cardNumber": cc}, headers=headers).json()
                    status = "✅ <b>LIVE / HIT</b>" if res.get('isValid') else "❌ <b>DEAD</b>"
                except: status = "⚠️ <b>API ERROR</b>"

    time_taken = round(time.time() - start_time, 2)
    res = f"{status}\n━━━━━━━━━━━━\n💳 <b>Card:</b> <code>{input_data}</code>\n⚡ <b>Gateway:</b> {gateway}\n⏱️ <b>Time:</b> {time_taken}s"
    bot.reply_to(message, res)

if __name__ == "__main__":
    keep_alive()
    # Conflict fix: delete_webhook purane connections clear karta hai
    bot.delete_webhook()
    bot.infinity_polling(timeout=10, long_polling_timeout=5)
