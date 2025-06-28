import os
import telebot
import openai

# Safely load your credentials
TELEGRAM_BOT_TOKEN = os.getenv("8026951635:AAGX8UhpvLBz8c12GoaScIcYDP_LMUnnkTg")
OPENAI_API_KEY = os.getenv("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")

# Initialize
bot = telebot.TeleBot(TELEGRAM_BOT_TOKEN)
openai.api_key = OPENAI_API_KEY

@bot.message_handler(func=lambda message: True)
def chat_with_gpt(message):
    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": message.text}]
        )
        bot.reply_to(message, response['choices'][0]['message']['content'])
    except Exception as e:
        bot.reply_to(message, f"Error: {str(e)}")

bot.polling()
