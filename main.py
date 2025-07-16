import requests
from bs4 import BeautifulSoup
import telegram
import schedule
import time
from datetime import datetime

BOT_TOKEN = "8173650773:AAH5QE4ZPLc6Zr4rF-tlSM3MCu6WIrk2N9o"
CHANNEL_ID = "@TradeHub_University"

def get_forex_news():
    url = 'https://www.forexfactory.com/calendar'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    soup = BeautifulSoup(response.content, 'html.parser')
    rows = soup.find_all('tr', class_='calendar__row')
    today = datetime.utcnow().date()
    message = f"📊 اخبار مهم فارکس - {today}:\n\n"
    for row in rows:
        imp = row.find('td', class_='calendar__impact')
        if not imp: continue
        span = imp.find('span')
        impact = span.get('title', '').lower() if span else ''
        time_text = row.find('td', class_='calendar__time').text.strip()
        currency = row.find('td', class_='calendar__currency').text.strip()
        event = row.find('td', class_='calendar__event').text.strip()
        forecast = row.find('td', class_='calendar__forecast').text.strip()
        previous = row.find('td', class_='calendar__previous').text.strip()

        if 'high' in impact:
            icon = "🔴 High"
        elif 'medium' in impact:
            icon = "🟠 Medium"
        elif "bank holiday" in event.lower():
            icon = "🏦 Bank Holiday"
        else:
            continue

        message += f"{icon}\n🕐 {time_text} | 🌍 {currency}\n📰 {event}\n📊 Forecast: {forecast} | 📈 Previous: {previous}\n----------------------------\n"
    return message

def send_news():
    bot = telegram.Bot(token=BOT_TOKEN)
    news = get_forex_news()
    if news:
        bot.send_message(chat_id=CHANNEL_ID, text=news)

schedule.every().day.at("21:31").do(send_news)  # معادل 00:01 تهران
send_news()

while True:
    schedule.run_pending()
    time.sleep(30)
