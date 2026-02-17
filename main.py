import os, telebot, requests, time, stripe, random
from telebot import types 
from flask import Flask
from threading import Thread

# --- Professional Uptime Monitor ---
app = Flask('')
@app.route('/')
def home(): return "<h1>NiaziBin Bot is Online</h1>"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    Thread(target=run).start()

# --- Config & Variables ---
TOKEN = os.getenv("TOKEN")
RAPID_KEY = os.getenv("RAPIDAPI_KEY")
STRIPE_SK = os.getenv("STRIPE_SK")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# --- UI Aesthetics ---
LOG_URL = "https://i.ibb.co/example.jpg" # Yahan apna logo link daal sakte ho

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📢 Channel", url="https://t.me/your_link"),
        types.InlineKeyboardButton("🛠️ Tools", callback_data="tools"),
        types.InlineKeyboardButton("💳 My Account", callback_data="account")
    )
    
    welcome = (
        f"<b>⚜️ WELCOME TO NIAZIBIN PREMIUM ⚜️</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👤 <b>User:</b> <code>{message.from_user.first_name}</code>\n"
        f"🆔 <b>ID:</b> <code>{message.from_user.id}</code>\n"
        f"🚀 <b>Status:</b> <pre>Premium V3.0 Active</pre>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"💡 <i>Use /chk to start validating cards with high-speed gateways!</i>"
    )
    bot.reply_to(message, welcome, reply_markup=markup)

@bot.message_handler(commands=['chk'])
def chk_handler(message):
    start_time = time.time()
    input_data = message.text.replace('/chk', '').strip()
    
    if "|" not in input_data:
        return bot.reply_to(message, "<b>⚠️ INVALID FORMAT</b>\n\nFormat: <code>card|mm|yy|cvv</code>")
    
    try:
        cc, mm, yy, cvv = input_data.split('|')
    except:
        return bot.reply_to(message, "❌ <b>Parse Error!</b> Check your CC format.")

    # Professional Live Status
    loading = bot.reply_to(message, "<b>⚡ Processing... ♻️</b>")
    
    gateway, status, icon = "RapidAPI-V2", "DECLINED", "❌"

    # --- HIGH SPEED STRIPE GATEWAY ---
    if STRIPE_SK:
        try:
            stripe.api_key = STRIPE_SK
            stripe.PaymentMethod.create(type="card", card={"number": cc, "exp_month": int(mm), "exp_year": int(yy), "cvc": cvv})
            status, gateway, icon = "LIVE / HIT", "Stripe-Auth 🔥", "✅"
        except Exception as e:
            err = str(e)
            if "declined" in err or "incorrect_cvc" in err:
                status, gateway, icon = "DEAD / DECLINED", "Stripe-Auth 🔥", "❌"
            else:
                # Automatic Fallback
                try:
                    headers = {"X-RapidAPI-Key": RAPID_KEY, "X-RapidAPI-Host": "credit-card-validator2.p.rapidapi.com"}
                    res = requests.post("https://credit-card-validator2.p.rapidapi.com/validate-credit-card", json={"cardNumber": cc}, headers=headers).json()
                    status = "LIVE / HIT" if res.get('isValid') else "DEAD"
                    icon = "✅" if res.get('isValid') else "❌"
                except: status, icon = "GATEWAY ERROR", "⚠️"

    time_taken = round(time.time() - start_time, 2)
    
    # --- The Ultra Pro Max Professional Reply ---
    response = (
        f"{icon} <b>{status}</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"💳 <b>Card:</b> <code>{input_data}</code>\n"
        f"⚡ <b>Gateway:</b> <code>{gateway}</code>\n"
        f"🛡️ <b>Security:</b> <code>2D / Stripe-V3</code>\n"
        f"⏱️ <b>Time Taken:</b> <code>{time_taken}s</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ <b>Checked By:</b> @{bot.get_me().username}"
    )
    bot.edit_message_text(response, message.chat.id, loading.message_id)

if __name__ == "__main__":
    keep_alive()
    bot.delete_webhook() # Clearing Conflict 409
    bot.infinity_polling()
