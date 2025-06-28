import telebot
import requests
import json
import os
from flask import Flask

# ✅ Your actual tokens
BOT_TOKEN = "8026951635:AAGX8UhpvLBz8c12GoaScIcYDP_LMUnnkTg"
OPENROUTER_API_KEY = "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"

bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route('/')
def index():
    return "Hustler AI is running..."

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
        reply = res.json()['choices'][0]['message']['content']
        bot.reply_to(message, reply.strip())
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")

# 🔁 Start both Flask and Telegram polling on Render
if __name__ == "__main__":
    import threading

    # Start Telegram bot polling in a separate thread
    threading.Thread(target=bot.infinity_polling).start()

    # Start Flask app (Render looks for open port)
    PORT = int(os.environ.get("PORT", 8080))
    app.run(host="0.0.0.0", port=PORT)
