import requests
from bs4 import BeautifulSoup
import time
import asyncio
from telegram import Bot
import os

URL = 'https://www.district.in/events/tata-ipl-2025-finals-match-in-ahmedabad-june03-buy-tickets'
CHECK_INTERVAL = 10  # seconds
BOT_TOKEN = '7722758245:AAHNticXObc67P5ayQTm2w2Yi6W0JIwIX_c'

bot = Bot(token=BOT_TOKEN)

def is_item_in_stock():
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(URL, headers=headers)
    soup = BeautifulSoup(response.text, 'html.parser')
    button = soup.find('button', string=lambda text: 'Coming Soon' in text if text else False)
    return button is None

async def send_notification():
    message = f"🚨 Item is back in stock!\n👉 Book Now: {URL}"
    if not os.path.exists('subscribers.txt'):
        print("No subscribers yet.")
        return
    with open('subscribers.txt', 'r') as f:
        chat_ids = [line.strip() for line in f.readlines()]
    for chat_id in chat_ids:
        for _ in range(15):
            try:
                await bot.send_message(chat_id=chat_id, text=message)
                await asyncio.sleep(1)
            except Exception as e:
                print(f"❌ Failed to send to {chat_id}: {e}")

def main():
    notified = False
    while True:
        try:
            if is_item_in_stock():
                if not notified:
                    asyncio.run(send_notification())
                    notified = True
                    print("✅ In stock. Notified.")
            else:
                notified = False
                print("❌ Out of stock.")
        except Exception as e:
            print(f"Error: {e}")
        time.sleep(CHECK_INTERVAL)

if __name__ == "__main__":
    main()
