import time
import telebot
import threading
from flashbot2 import enter_site, check_score

TELEGRAM_TOKEN = "6308284018:AAFcvYUPwN8b2LUYJfmgmQbW5e-0tVPag_s"
bot = telebot.TeleBot(TELEGRAM_TOKEN)
channel = '@flashscore_bot_my'
sent_urls_file = 'sent_urls.txt'

# Загружаем уже отправленные ссылки из файла
def load_sent_urls():
    try:
        with open(sent_urls_file, 'r') as f:
            return set(f.read().splitlines())
    except FileNotFoundError:
        return set()

# Сохраняем новые ссылки
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

        time.sleep(60)  # Пауза перед следующим запуском


if __name__ == '__main__':
    threading.Thread(target=run).start()
    bot.polling(none_stop=True)
