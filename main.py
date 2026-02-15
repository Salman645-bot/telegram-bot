import os
import telebot
import requests
import stripe
from flask import Flask
from threading import Thread
import time

# --- Flask Server (Railway ko "Active" rakhne ke liye) ---
app = Flask('')

@app.route('/')
def home():
    return "Bot is alive!"

def run():
    # Railway PORT variable use karta hai, default 8080
    port = int(os.environ.get('PORT', 8080))
    app.run(host='0.0.0.0', port=port)

def keep_alive():
    t = Thread(target=run)
    t.start()

# --- Setup ---
# Railway ke Variables mein TOKEN hona chahiye
API_TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")

# Tumhari Live Stripe Key (Already added)
stripe.api_key = "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"

# --- Welcome Message (/start) ---
@bot.message_handler(commands=['start'])
def start_message(message):
    welcome = (
        "<b>👋 Welcome Janu! Bot Full Active Hai.</b>\n\n"
        "🔍 <b>BIN Details:</b> Type <code>/bin 411122</code>\n"
        "💳 <b>Card Checker:</b> Type <code>/chk card|mm|yy|cvv</code>\n\n"
        "<i>⚡ Powered by Stripe Live API</i>"
    )
    bot.reply_to(message, welcome)

# --- BIN Lookup Feature (/bin) ---
@bot.message_handler(commands=['bin'])
def handle_bin(message):
    text = message.text.replace('/bin', '').strip()
    if not text.isdigit() or len(text) < 6:
        bot.reply_to(message, "❌ Sahi BIN likho. Example: <code>/bin 457173</code>")
        return
    
    bin_to_check = text[:6]
    try:
        res = requests.get(f"https://lookup.binlist.net/{bin_to_check}", timeout=10)
        data = res.json()
        response = (
            "━━━━━━━━━━━━━━━━━━\n"
            "<b>💳 BIN RESULT</b>\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"<b>🔢 BIN:</b> <code>{bin_to_check}</code>\n"
            f"<b>🏦 Bank:</b> {data.get('bank', {}).get('name', 'N/A')}\n"
            f"<b>🌐 Network:</b> {data.get('scheme', 'N/A')}\n"
            f"<b>🌎 Country:</b> {data.get('country', {}).get('name', 'N/A')}\n\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        bot.reply_to(message, response)
    except:
        bot.reply_to(message, "⚠️ BIN details nahi milin.")

# --- Card Checker Feature (/chk) ---
@bot.message_handler(commands=['chk'])
def handle_chk(message):
    input_text = message.text.replace('/chk', '').strip()
    if "|" not in input_text:
        bot.reply_to(message, "❌ Format: <code>/chk card|mm|yy|cvv</code>")
        return
    
    try:
        parts = input_text.split('|')
        cc = parts[0].strip()
        mm = parts[1].strip()
        yy = parts[2].strip()
        cvv = parts[3].strip()
        
        if len(yy) == 2: yy = "20" + yy
        
        bot.send_chat_action(message.chat.id, 'typing')
        
        try:
            # Stripe API check
            token = stripe.Token.create(
                card={"number": cc, "exp_month": int(mm), "exp_year": int(yy), "cvc": cvv}
            )
            status = "✅ <b>CARD LIVE</b>"
            reason = "Success (CVV Match)"
        except stripe.error.CardError as e:
            status = "❌ <b>DECLINED</b>"
            reason = e.user_message
        
        res_chk = (
            "━━━━━━━━━━━━━━━━━━\n"
            f"{status}\n"
            "━━━━━━━━━━━━━━━━━━\n\n"
            f"💳 <b>Card:</b> <code>{input_text}</code>\n"
            f"📝 <b>Response:</b> {reason}\n"
            f"⚡ <b>Gateway:</b> Stripe Live\n"
            "━━━━━━━━━━━━━━━━━━"
        )
        bot.reply_to(message, res_chk)
    except:
        bot.reply_to(message, "⚠️ System Error. Check format.")

if __name__ == "__main__":
    keep_alive()
    print("🚀 Bot is Starting...")
    bot.infinity_polling()
