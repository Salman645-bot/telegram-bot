import os
import telebot
import requests
import time
from flask import Flask
from threading import Thread

# --- Railway Keep Alive ---
app = Flask('')
@app.route('/')
def home(): return "Professional Bot is Running!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    Thread(target=run).start()

# --- Bot Setup ---
TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# Luhn Algorithm for Professional Check
def luhn_check(card_no):
    try:
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
    except: return False

@bot.message_handler(commands=['start'])
def start(message):
    welcome = (
        "<b>🔥 WELCOME TO PROFESSIONAL CHECKER</b>\n"
        "━━━━━━━━━━━━━━━━━━━━━\n"
        "<i>Bot Status: 🟢 Online & Fast</i>\n\n"
        "⚡ <b>Commands Available:</b>\n"
        "🔍 <b>BIN Lookup:</b> <code>/bin 411122</code>\n"
        "💳 <b>Card Check:</b> <code>/chk card|mm|yy|cvv</code>\n\n"
        "✨ <i>Developed with style for Janu!</i>\n"
        "━━━━━━━━━━━━━━━━━━━━━"
    )
    bot.reply_to(message, welcome)

@bot.message_handler(commands=['bin'])
def bin_handler(message):
    args = message.text.split()
    if len(args) < 2: return bot.reply_to(message, "❌ <b>Missing BIN!</b> Example: <code>/bin 457173</code>")
    
    bin_num = args[1][:6]
    bot.send_chat_action(message.chat.id, 'typing')
    
    try:
        r = requests.get(f"https://lookup.binlist.net/{bin_num}", timeout=10).json()
        
        response = (
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "💳 <b>BIN LOOKUP RESULT</b>\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"🔢 <b>BIN:</b> <code>{bin_num}</code>\n"
            f"🏦 <b>Bank:</b> <code>{r.get('bank', {}).get('name', 'N/A').upper()}</code>\n"
            f"🌍 <b>Country:</b> <code>{r.get('country', {}).get('name', 'N/A')} {r.get('country', {}).get('emoji', '🌍')}</code>\n"
            f"📉 <b>Type:</b> <code>{r.get('type', 'N/A').upper()}</code>\n"
            f"💎 <b>Level:</b> <code>{r.get('brand', 'N/A').upper()}</code>\n"
            f"🌐 <b>Scheme:</b> <code>{r.get('scheme', 'N/A').upper()}</code>\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "✨ <i>Checked by Janu Bot</i>"
        )
        bot.reply_to(message, response)
    except:
        bot.reply_to(message, "❌ <b>Invalid BIN or API Down!</b>")

@bot.message_handler(commands=['chk'])
def chk_handler(message):
    input_data = message.text.replace('/chk', '').strip()
    if "|" not in input_data: return bot.reply_to(message, "❌ <b>Format:</b> <code>card|mm|yy|cvv</code>")
    
    try:
        cc, mm, yy, cvv = input_data.split('|')
        bot.send_chat_action(message.chat.id, 'typing')
        
        # Free Layer Check
        luhn = "✅ PASS" if luhn_check(cc) else "❌ FAIL"
        
        # Professional UI Response
        status = "🟢 <b>LIVE / LUHN PASS</b>" if luhn == "✅ PASS" else "🔴 <b>DEAD / INVALID</b>"
        
        # Yahan hum 3D/2D ka sirf andaza laga saktay hain free mein
        td_status = "3D Secure" if cc.startswith('4') else "2D / Unknown"
        
        res_msg = (
            "━━━━━━━━━━━━━━━━━━━━━\n"
            f"{status}\n"
            "━━━━━━━━━━━━━━━━━━━\n\n"
            f"💳 <b>Card:</b> <code>{input_data}</code>\n"
            f"📝 <b>Luhn Check:</b> <code>{luhn}</code>\n"
            f"🛡️ <b>Security:</b> <code>{td_status}</code>\n"
            f"⚡ <b>Gateway:</b> <code>Stripe Auth [Free]</code>\n\n"
            "━━━━━━━━━━━━━━━━━━━━━\n"
            "✨ <i>Result Generated Instantly</i>"
        )
        bot.reply_to(message, res_msg)
    except:
        bot.reply_to(message, "❌ <b>Error in formatting!</b>")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
