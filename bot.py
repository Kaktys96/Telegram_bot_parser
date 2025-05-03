import time
import telebot
import threading
from flashbot2 import enter_site, check_score
from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_TOKEN = os.getenv("TELEGRAM_TOKEN")
bot = telebot.TeleBot(TELEGRAM_TOKEN)
channel = '@flashscore_bot_my'
sent_urls_file = 'sent_urls.txt'


def load_sent_urls():
    try:
        with open(sent_urls_file, 'r') as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()


def save_sent_url(url):
    with open(sent_urls_file, 'a') as f:
        f.write(url + '\n')


all_send_url = load_sent_urls()


def run():
    while True:
        try:
            print("Сканирование началось...")
            match = enter_site()
            if not match:
                print("Нет матчей")
                time.sleep(60)
                continue

            good_matches = check_score(match)
            if not good_matches:
                print("Подходящие матчи не найдены")
                time.sleep(60)
                continue

            for url in good_matches:
                if url not in all_send_url:
                    bot.send_message(channel, url)
                    save_sent_url(url)
                    all_send_url.add(url)
                    print("Отправлено:", url)
                    time.sleep(1)

        except Exception as exc:
            print("Ошибка в основном цикле:", exc)

        time.sleep(60)


if __name__ == '__main__':
    threading.Thread(target=run).start()
    bot.polling(none_stop=True)
