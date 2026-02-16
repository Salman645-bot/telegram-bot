import os
import telebot
import requests
import time
from telebot import types # Professional buttons ke liye
from flask import Flask
from threading import Thread

# --- Railway/Uptime Health Check ---
app = Flask('')
@app.route('/')
def home(): return "NiaziBin Bot is Online 24/7"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    Thread(target=run).start()

# --- Configuration ---
TOKEN = os.getenv("TOKEN")
RAPID_KEY = os.getenv("RAPIDAPI_KEY") #
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# --- Commands List for Menu ---
# Janu, BotFather mein ja kar ye commands set kar lena
@bot.message_handler(commands=['start'])
def start(message):
    user_name = message.from_user.first_name
    user_id = message.from_user.id
    
    # Inline Buttons
    markup = types.InlineKeyboardMarkup()
    btn1 = types.InlineKeyboardButton("📢 My Channel", url="https://t.me/your_channel_link") # Apna link dalo
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
        
        # Agar LIVE aaye to admin ko ya channel ko forward karne ka code yahan add ho sakta hai
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
    keep_alive() #
    bot.infinity_polling()
