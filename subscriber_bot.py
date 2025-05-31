from telegram.ext import Updater, CommandHandler
import os

BOT_TOKEN = '7722758245:AAHNticXObc67P5ayQTm2w2Yi6W0JIwIX_c'

def start(update, context):
    chat_id = str(update.message.chat_id)
    if not os.path.exists('subscribers.txt'):
        with open('subscribers.txt', 'w') as f:
            pass
    with open('subscribers.txt', 'r') as f:
        subscribers = f.read().splitlines()
    if chat_id not in subscribers:
        with open('subscribers.txt', 'a') as f:
            f.write(chat_id + '\n')
        update.message.reply_text("✅ You've been subscribed for stock alerts!")
    else:
        update.message.reply_text("ℹ️ You're already subscribed.")

updater = Updater(BOT_TOKEN, use_context=True)
dp = updater.dispatcher
dp.add_handler(CommandHandler("start", start))

# Keep alive with web server
from flask import Flask
app = Flask('')

@app.route('/')
def home():
    return "Bot is running!"

import threading
threading.Thread(target=app.run, kwargs={'host':'0.0.0.0','port':8080}).start()

updater.start_polling()
updater.idle()
