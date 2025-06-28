import os
import telebot
from flask import Flask, request

API_TOKEN = os.getenv("BOT_TOKEN")
WEBHOOK_URL = os.getenv("RENDER_EXTERNAL_URL")

bot = telebot.TeleBot(API_TOKEN)
app = Flask(__name__)

@app.route(f"/{API_TOKEN}", methods=['POST'])
def webhook():
    json_str = request.get_data().decode('UTF-8')
    update = telebot.types.Update.de_json(json_str)
    bot.process_new_updates([update])
    return "", 200

@app.route("/healthz")
def health_check():
    return "OK", 200

@app.route("/")
def index():
    return "Bot is live", 200

@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.reply_to(message, "Welcome! Bot is running via webhook on Render.")

if __name__ == "__main__":
    bot.remove_webhook()
    bot.set_webhook(url=f"{WEBHOOK_URL}/{API_TOKEN}")
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
    
