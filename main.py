import os
import telebot
import requests
import time
import stripe # Naya engine
from telebot import types 
from flask import Flask
from threading import Thread

# --- Railway/Uptime Health Check (Same as before) ---
app = Flask('')
@app.route('/')
def home(): return "NiaziBin Bot is Online 24/7"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    Thread(target=run).start()

# --- Configuration (Added STRIPE_SK) ---
TOKEN = os.getenv("TOKEN")
RAPID_KEY = os.getenv("RAPIDAPI_KEY")
STRIPE_SK = os.getenv("STRIPE_SK") # Railway Variables mein jo key dali thi
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# --- Start Command (Same as before) ---
@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("📢 My Channel", url="https://t.me/your_channel_link") 
    btn2 = types.InlineKeyboardButton("🛠️ Commands", callback_data="help_cmd")
    markup.add(btn1, btn2)
    
    welcome = (
        f"<b>🔥 Welcome {user_name} to NiaziBin Bot!</b>\n\n"
        f"🆔 <b>User ID:</b> <code>{user_id}</code>\n"
        f"🚀 <b>Status:</b> <code>Premium Active</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"💳 <b>Format:</b> <code>/chk card|mm|yy|cvv</code>\n"
        f"🔍 <b>Format:</b> <code>/bin 411122</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ <b>Powered by:</b> @NiaziBin_bot"
    )
    bot.reply_to(message, welcome, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "help_cmd")
def help_callback(call):
    bot.answer_callback_query(call.id, "Use /chk or /bin")
    bot.send_message(call.message.chat.id, "📖 <b>Manual:</b>\n\n1. Card check: /chk 411111|11|28|123\n2. BIN lookup: /bin 411122")

# --- New Optimized CHK Command ---
@bot.message_handler(commands=['chk'])
def chk_handler(message):
    start_time = time.time()
    input_data = message.text.replace('/chk', '').strip()
    
    if "|" not in input_data:
        return bot.reply_to(message, "❌ <b>Error:</b> Use <code>card|mm|yy|cvv</code>")
    
    parts = input_data.split('|')
    cc, mm, yy, cvv = parts[0], parts[1], parts[2], parts[3]
    bot.send_chat_action(message.chat.id, 'typing')

    gateway = "RapidAPI-V2"
    status = "DEAD"

    # --- Step 1: Try Stripe First ---
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
            if "Your card was declined" in err or "incorrect_cvc" in err:
                status = "❌ <b>DEAD / DECLINED</b>"
                gateway = "Stripe-SK 🔥"
            elif "expired_card" in err:
                status = "❌ <b>EXPIRED</b>"
                gateway = "Stripe-SK 🔥"
            else:
                # Agar Key block ho to RapidAPI par shift ho jayega
                status = "RETRY"

    # --- Step 2: Fallback to RapidAPI (If Stripe Fails) ---
    if status == "RETRY" or not STRIPE_SK:
        try:
            url = "https://credit-card-validator2.p.rapidapi.com/validate-credit-card"
            headers = {"X-RapidAPI-Key": RAPID_KEY, "X-RapidAPI-Host": "credit-card-validator2.p.rapidapi.com"}
            response = requests.post(url, json={"cardNumber": cc}, headers=headers).json()
            is_valid = response.get('isValid', False)
            status = "✅ <b>LIVE / HIT</b>" if is_valid else "❌ <b>DEAD / DECLINED</b>"
            gateway = "RapidAPI-V2"
        except:
            status = "⚠️ <b>API ERROR</b>"

    time_taken = round(time.time() - start_time, 2)
    res = (
        f"{status}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"💳 <b>Card:</b> <code>{input_data}</code>\n"
        f"🛡️ <b>Type:</b> <code>Checking...</code>\n"
        f"🔒 <b>Security:</b> <code>2D / Stripe</code>\n"
        f"⚡ <b>Gateway:</b> <code>{gateway}</code>\n"
        f"⏱️ <b>Time Taken:</b> {time_taken}s\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ <b>Checked By:</b> @{bot.get_me().username}"
    )
    bot.reply_to(message, res)

@bot.message_handler(commands=['bin'])
def bin_handler(message):
    bin_num = message.text.replace('/bin', '').strip()[:6]
    if not bin_num: return bot.reply_to(message, "❌ <b>Enter BIN!</b>")
    
    try:
        r = requests.get(f"https://lookup.binlist.net/{bin_num}").json()
        res = (
            f"🏦 <b>BIN LOOKUP RESULT</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"💳 <b>BIN:</b> <code>{bin_num}</code>\n"
            f"🌍 <b>Country:</b> {r.get('country', {}).get('name', 'N/A')} {r.get('country', {}).get('emoji', '')}\n"
            f"🏢 <b>Bank:</b> {r.get('bank', {}).get('name', 'N/A')}\n"
            f"📊 <b>Level:</b> {r.get('brand', 'N/A')}\n"
            f"📝 <b>Type:</b> {r.get('type', 'N/A').upper()}\n"
            f"💳 <b>Scheme:</b> {r.get('scheme', 'N/A').upper()}\n"
            f"━━━━━━━━━━━━━━━━━━━━━"
        )
        bot.reply_to(message, res)
    except:
        bot.reply_to(message, "❌ <b>Error:</b> BIN not found.")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
