import telebot
import requests
import json
import os
from flask import Flask, request

BOT_TOKEN = "8026951635:AAGX8UhpvLBz8c12GoaScIcYDP_LMUnnkTg"
OPENROUTER_API_KEY = "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"
bot = telebot.TeleBot(BOT_TOKEN)
app = Flask(__name__)

@app.route("/")
def home():
    return "Hustler AI is up!", 200

@app.route('/healthz')
def health_check():
    return "OK", 200

@app.route(f"/{BOT_TOKEN}", methods=['POST'])
def telegram_webhook():
    update = telebot.types.Update.de_json(request.stream.read().decode("utf-8"))
    bot.process_new_updates([update])
    return "ok", 200

@bot.message_handler(commands=['start'])
def start(message):
    bot.reply_to(message, "👋 Hustler AI is live! Send me a question.")

@bot.message_handler(func=lambda m: True)
def ai_reply(message):
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

        if 'choices' in data and len(data['choices']) > 0:
            reply = data['choices'][0]['message']['content']
            bot.reply_to(message, reply.strip())
        else:
            bot.reply_to(message, "⚠️ AI didn't return a valid reply. Try again.")
    except Exception as e:
        bot.reply_to(message, f"⚠️ Error: {e}")

# 🔁 Set webhook
if __name__ == '__main__':
    server_url = "https://vtu-telegram-bot.onrender.com"  # your Render domain
    bot.remove_webhook()
    bot.set_webhook(url=f"{server_url}/{BOT_TOKEN}")
    port = int(os.environ.get("PORT", 10000))
    app.run(host="0.0.0.0", port=port)
