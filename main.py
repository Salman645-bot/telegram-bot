import os
import time
import telebot
import requests

API_TOKEN = os.getenv("TOKEN")

if not API_TOKEN:
    print("❌ TOKEN not found!")
    exit()

bot = telebot.TeleBot(API_TOKEN, parse_mode="HTML")


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.reply_to(
        message,
        "<b>👋 Welcome to BIN Lookup Bot</b>\n\n"
        "Send a <b>6 digit BIN</b>\n"
        "Example: <code>457173</code>"
    )


@bot.message_handler(func=lambda message: True)
def handle_message(message):
    text = message.text.strip()

    if not text.isdigit() or len(text) != 6:
        bot.reply_to(message, "❌ Please send a valid 6 digit BIN.")
        return

    start_time = time.time()

    try:
        res = requests.get(f"https://lookup.binlist.net/{text}", timeout=10)

        if res.status_code != 200:
            bot.reply_to(message, "⚠️ BIN not found.")
            return

        data = res.json()

        bank = data.get('bank', {}).get('name', 'N/A')
        scheme = data.get('scheme', 'N/A')
        card_type = data.get('type', 'N/A')
        brand = data.get('brand', 'N/A')
        country = data.get('country', {}).get('name', 'UNKNOWN')
        flag = data.get('country', {}).get('emoji', '🌍')

    except Exception as e:
        print("API ERROR:", e)
        bot.reply_to(message, "⚠️ Server Busy. Try Again Later.")
        return

    response_time = round(time.time() - start_time, 2)

    response = (
        "━━━━━━━━━━━━━━━━━━\n"
        "<b>💳 BIN RESULT</b>\n"
        "━━━━━━━━━━━━━━━━━━\n\n"
        f"<b>🔢 BIN:</b> <code>{text}</code>\n"
        f"<b>🏦 Bank:</b> {bank}\n"
        f"<b>🌐 Network:</b> {scheme}\n"
        f"<b>💼 Type:</b> {card_type}\n"
        f"<b>⭐ Brand:</b> {brand}\n"
        f"<b>🌎 Country:</b> {country} {flag}\n\n"
        f"⏱ <i>Response:</i> {response_time}s\n"
        "━━━━━━━━━━━━━━━━━━"
    )

    bot.reply_to(message, response)


print("🚀 Bot is Running...")
bot.infinity_polling()
