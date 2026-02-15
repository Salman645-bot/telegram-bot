import os
import telebot
import requests
from flask import Flask
from threading import Thread

# --- Flask for Railway ---
app = Flask('')
@app.route('/')
def home(): return "Bot is Online!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    Thread(target=run).start()

# --- Bot Setup ---
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Luhn Algorithm (Free card validation)
def luhn_check(card_no):
    n_digits = len(card_no)
    n_sum = 0
    is_second = False
    for i in range(n_digits - 1, -1, -1):
        d = ord(card_no[i]) - ord('0')
        if is_second: d = d * 2
        n_sum += d // 10
        n_sum += d % 10
        is_second = not is_second
    return n_sum % 10 == 0

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "<b>👋 Welcome Janu! Bot Active Hai!</b>\n\n🔍 /bin 123456\n💳 /chk card|mm|yy|cvv")

@bot.message_handler(commands=['bin'])
def bin_check(message):
    bin_num = message.text.split()[1][:6] if len(message.text.split()) > 1 else ""
    if not bin_num: return bot.reply_to(message, "❌ BIN bhejain!")
    
    data = requests.get(f"https://lookup.binlist.net/{bin_num}").json()
    res = (f"🔍 <b>BIN:</b> {bin_num}\n"
           f"🏦 <b>Bank:</b> {data.get('bank', {}).get('name', 'N/A')}\n"
           f"🌍 <b>Country:</b> {data.get('country', {}).get('name', 'N/A')}")
    bot.reply_to(message, res)

@bot.message_handler(commands=['chk'])
def chk_free(message):
    input_data = message.text.replace('/chk', '').strip()
    if "|" not in input_data: return bot.reply_to(message, "❌ Format: <code>card|mm|yy|cvv</code>")
    
    cc = input_data.split('|')[0]
    bot.send_chat_action(message.chat.id, 'typing')
    
    # Check if card is valid via Luhn (Free)
    is_valid = luhn_check(cc)
    status = "✅ <b>CARD VALID (Luhn Pass)</b>" if is_valid else "❌ <b>INVALID CARD NUMBER</b>"
    
    msg = (f"━━━━━━━━━━━━━━━━━━\n"
           f"{status}\n"
           f"━━━━━━━━━━━━━━━━━━\n\n"
           f"💳 <b>Card:</b> <code>{input_data}</code>\n"
           f"📝 <b>Note:</b> Luhn check passed. Free version testing.\n"
           f"━━━━━━━━━━━━━━━━━━")
    bot.reply_to(message, msg)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
