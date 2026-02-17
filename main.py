import os, telebot, requests, time, stripe, random
from telebot import types 
from flask import Flask
from threading import Thread

# --- Railway Health Check ---
app = Flask('')
@app.route('/')
def home(): return "NiaziBin Ultra Pro Max is Online"

def run():
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 8080)))

def keep_alive():
    Thread(target=run).start()

# --- Configuration (Railway Variables) ---
TOKEN = os.getenv("TOKEN")
RAPID_KEY = os.getenv("RAPIDAPI_KEY")
STRIPE_SK = os.getenv("STRIPE_SK")
ADMIN_ID = 123456789  # <--- Janu, yahan apni Telegram ID dalo

if not TOKEN:
    exit("❌ Error: TOKEN missing in Railway!")

bot = telebot.TeleBot(TOKEN, parse_mode="HTML")

# --- Commands ---

@bot.message_handler(commands=['start'])
def start(message):
    markup = types.InlineKeyboardMarkup(row_width=2)
    markup.add(
        types.InlineKeyboardButton("📢 Channel", url="https://t.me/your_link"),
        types.InlineKeyboardButton("🛠️ Tools", callback_data="tools_menu")
    )
    welcome = (
        f"<b>🌟 NIAZIBIN ULTRA PRO MAX 🌟</b>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"👋 <b>Welcome,</b> {message.from_user.first_name}!\n"
        f"🚀 <b>Status:</b> <code>Premium Active</code>\n"
        f"🛰️ <b>Server:</b> <code>Railway Cloud</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"💳 <b>Format:</b> <code>/chk card|mm|yy|cvv</code>"
    )
    bot.reply_to(message, welcome, reply_markup=markup)

@bot.message_handler(commands=['chk'])
def chk_handler(message):
    start_time = time.time()
    input_data = message.text.replace('/chk', '').strip()
    
    if "|" not in input_data:
        return bot.reply_to(message, "❌ <b>Format:</b> <code>card|mm|yy|cvv</code>")
    
    try:
        cc, mm, yy, cvv = input_data.split('|')
    except:
        return bot.reply_to(message, "❌ <b>Error:</b> Invalid Format")

    bot.send_chat_action(message.chat.id, 'typing')
    msg = bot.reply_to(message, "🔍 <b>Authenticating with Stripe...</b>")
    
    gateway, status = "RapidAPI-V2", "❌ <b>DEAD</b>"

    # --- STRIPE GATEWAY ---
    if STRIPE_SK:
        try:
            stripe.api_key = STRIPE_SK
            stripe.PaymentMethod.create(type="card", card={"number": cc, "exp_month": int(mm), "exp_year": int(yy), "cvc": cvv})
            status, gateway = "✅ <b>LIVE / HIT</b>", "Stripe-Auth 🔥"
        except Exception as e:
            err = str(e)
            if "declined" in err or "incorrect_cvc" in err:
                status, gateway = "❌ <b>DECLINED</b>", "Stripe-Auth 🔥"
            elif "expired" in err:
                status, gateway = "❌ <b>EXPIRED</b>", "Stripe-Auth 🔥"
            else:
                # Fallback to Rapid
                try:
                    headers = {"X-RapidAPI-Key": RAPID_KEY, "X-RapidAPI-Host": "credit-card-validator2.p.rapidapi.com"}
                    res = requests.post("https://credit-card-validator2.p.rapidapi.com/validate-credit-card", json={"cardNumber": cc}, headers=headers).json()
                    status = "✅ <b>LIVE / HIT</b>" if res.get('isValid') else "❌ <b>DEAD</b>"
                except: status = "⚠️ <b>GATEWAY ERROR</b>"

    time_taken = round(time.time() - start_time, 2)
    response = (
        f"{status}\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"💳 <b>Card:</b> <code>{input_data}</code>\n"
        f"⚡ <b>Gateway:</b> <code>{gateway}</code>\n"
        f"🛡️ <b>Security:</b> <code>2D / Stripe-V3</code>\n"
        f"⏱️ <b>Time Taken:</b> <code>{time_taken}s</code>\n"
        f"━━━━━━━━━━━━━━━━━━━━━\n"
        f"✨ <b>Checked By:</b> @{bot.get_me().username}"
    )
    bot.edit_message_text(response, message.chat.id, msg.message_id)

@bot.message_handler(commands=['gen'])
def gen_handler(message):
    bin_num = message.text.replace('/gen', '').strip()[:6]
    if not bin_num: return bot.reply_to(message, "❌ <b>Enter BIN:</b> <code>/gen 411122</code>")
    
    cards = []
    for _ in range(10):
        extra = "".join([str(random.randint(0,9)) for _ in range(10)])
        cards.append(f"<code>{bin_num}{extra}|{random.randint(1,12)}|20{random.randint(25,30)}|{random.randint(100,999)}</code>")
    
    bot.reply_to(message, "<b>🎲 Generated Cards:</b>\n\n" + "\n".join(cards))

@bot.message_handler(commands=['bin'])
def bin_lookup(message):
    bin_num = message.text.replace('/bin', '').strip()[:6]
    try:
        r = requests.get(f"https://lookup.binlist.net/{bin_num}").json()
        res = (
            f"🏦 <b>BIN LOOKUP</b>\n"
            f"━━━━━━━━━━━━\n"
            f"🌍 <b>Country:</b> {r.get('country', {}).get('name', 'N/A')}\n"
            f"🏢 <b>Bank:</b> {r.get('bank', {}).get('name', 'N/A')}\n"
            f"💳 <b>Level:</b> {r.get('brand', 'N/A')}"
        )
        bot.reply_to(message, res)
    except: bot.reply_to(message, "❌ BIN Not Found")

if __name__ == "__main__":
    keep_alive()
    bot.infinity_polling()
