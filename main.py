import telebot
import requests
import json
import os
from flask import Flask

# 🔐 Replace with your active tokens
BOT_TOKEN = "8026951635:AAGX8UhpvLBz8c12GoaScIcYDP_LMUnnkTg"
OPENROUTER_API_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "🚀 Hustler AI is live! Ask me anything.")

@bot.message_handler(func=lambda m: True)
def chat_with_ai(message):
    try:
        url = "https://openrouter.ai/api/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {OPENROUTER_API_KEY}",
            "Content-Type": "application/json"
        }
        payload = {
            "model": "deepseek/deepseek-chat-v3-0324:free",
            "messages": [{"role": "user", "content": message.text}]
        }

        res = requests.post(url, headers=headers, data=json.dumps(payload))
        data = res.json()

        # ✅ Check if 'choices' exist in response
        if 'choices' in data and len(data['choices']) > 0:
            reply = data['choices'][0]['message']['content']
            bot.reply_to(message, reply.strip())
        else:
            bot.reply_to(message, "⚠️ AI didn't return a valid reply. Try again later.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")

# Flask routes
@app.route('/')
def index():
    return "Hustler AI is running..."

@app.route('/healthz')
def health_check():
    return "OK", 200

# Run bot and Flask server
def start_bot():
    bot.infinity_polling()

if __name__ == '__main__':
    import threading
    threading.Thread(target=start_bot).start()

    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
