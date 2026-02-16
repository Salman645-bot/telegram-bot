import os
import telebot
import requests
import time
from flask import Flask
from threading import Thread

# --- Railway/Uptime Health Check ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online 24/7"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    Thread(target=run).start()

# --- Configuration ---
# Railway Variables mein 'TOKEN' aur 'RAPIDAPI_KEY' add karna zaroori hai
TOKEN = os.getenv("TOKEN")
RAPID_KEY = os.getenv("RAPIDAPI_KEY") 
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        "<b>🔥 Welcome to Professional Checker Bot!</b>\n\n"
        "💳 <b>Usage:</b>\n"
        "• <code>/chk card|mm|yy|cvv</code>\n"
        "• <code>/bin 411122</code>\n\n"
        "🚀 <b>Status:</b> 24/7 Active via Railway"
    )
    bot.reply_to(message, welcome)

@bot.message_handler(commands=['chk'])
def chk_handler(message):
    start_time = time.time()
    input_data = message.text.replace('/chk', '').strip()
    
    if "|" not in input_data:
        return bot.reply_to(message, "❌ <b>Error:</b> Use <code>card|mm|yy|cvv</code>")
    
    parts = input_data.split('|')
    cc = parts[0]
    bot.send_chat_action(message.chat.id, 'typing')

    # RapidAPI Real-Time Validation
    url = "https://credit-card-validator2.p.rapidapi.com/validate-credit-card"
    headers = {
        "content-type": "application/json",
        "X-RapidAPI-Key": RAPID_KEY,
        "X-RapidAPI-Host": "credit-card-validator2.p.rapidapi.com"
    }
    
    try:
        response = requests.post(url, json={"cardNumber": cc}, headers=headers).json()
        end_time = time.time()
        time_taken = round(end_time - start_time, 2)
        
        is_valid = response.get('isValid', False)
        ctype = response.get('cardType', 'Unknown').upper()
        
        # Result Logic
        status = "✅ <b>LIVE / HIT</b>" if is_valid else "❌ <b>DEAD / DECLINED</b>"
        security = "3D Secure" if is_valid and "VISA" in ctype else "2D / Unknown"

        res = (
            f"<b>{status}</b>\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"💳 <b>Card:</b> <code>{input_data}</code>\n"
            f"🛡️ <b>Type:</b> <code>{ctype}</code>\n"
            f"🔒 <b>Security:</b> <code>{security}</code>\n"
            f"⚡ <b>Gateway:</b> <code>RapidAPI-V2</code>\n"
            f"⏱️ <b>Time Taken:</b> <code>{time_taken}s</code>\n"
            f"━━━━━━━━━━━━━━━━━━━━━\n"
            f"✨ <b>Checked By:</b> @{bot.get_me().username}"
        )
        bot.reply_to(message, res)
    except:
        bot.reply_to(message, "⚠️ <b>Error:</b> API limit reached or key invalid.")

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
        bot.reply_to(message, "❌ <b>Error:</b> BIN not found or API down.")

if __name__ == "__main__":
    keep_alive() # Keep bot 24/7 on Railway
    bot.infinity_polling()
