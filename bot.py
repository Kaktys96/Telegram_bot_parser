import time
import telebot
import sys
from flashbot2 import enter_site, check_score

TELEGRAM_TOKEN = "6308284018:AAFcvYUPwN8b2LUYJfmgmQbW5e-0tVPag_s"
bot = telebot.TeleBot(TELEGRAM_TOKEN)
channel = '@flashscore_bot_my'

all_send_url = []


def run():
    try:
        match = enter_site()
        a = check_score(match)
        for i in a:
            if i is not None:
                if i not in all_send_url:
                    bot.send_message(channel, i)
                    all_send_url.append(i)
                    time.sleep(1)
        else:
            run()
    except Exception as exc:
        print(exc, 'ERROR ЧТО-ТО ПОШЛО НЕ ТАК, СКРИПТ ПЕРЕЗАПУСТИЛСЯ!')
    finally:
        run()



if __name__ == '__main__':

    sys.setrecursionlimit(10000)
    run()
    bot.polling()
