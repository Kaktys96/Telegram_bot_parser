import telebot
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time


def enter_site():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    # chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.headless = False
    browser = webdriver.Chrome(options=chrome_options)
    browser.get('https://www.flashscore.com.ua/')
    time.sleep(0.5)

    click_live = browser.find_element(by=By.XPATH, value="//div[@class='filters__tab']")
    click_live.click()
    time.sleep(0.5)
    get_all_play = browser.find_elements(by=By.XPATH, value="//div[@class='event__info']")
    button_cookie = browser.find_elements(by=By.XPATH, value="//div[@id='onetrust-button-group']")
    browser.set_window_size(7680, 4320)
    for bt in button_cookie:
        bt.click()
    for open_play in get_all_play:
        if open_play:
            open_play.click()
        else:
            actions = ActionChains(browser)
            actions.move_to_element(open_play).perform()
    browser.execute_script("window.scrollTo(0,0)")

    time.sleep(0.5)

    get_time = browser.find_elements(by=By.XPATH, value="//div[@class='event__stage--block']")


    time.sleep(0.5)
    count_game = 0
    list_nums = [str(x) for x in range(1, 90)] + ['Перерыв']

    list_match = []
    for minutes in get_time:
        try:
            if str(minutes.text[0:2]) in list_nums:
                minutes.click()
                time.sleep(0.5)
                count_game += 1
                print(count_game)
            else:
                actions = ActionChains(browser)
                actions.move_to_element(minutes).perform()
        except Exception as ex:
            browser.execute_script("window.scrollTo(250, document.body.scrollHeight);")

    try:
        for i in range(1, count_game + 1):
            browser.switch_to.window(browser.window_handles[i])
            list_match.append(browser.current_url)
        time.sleep(0.5)
    except Exception as _ex:
        print(_ex, 'Игры отсутствуют')
    print(list_match)
    browser.close()
    browser.quit()
    return list_match


def check_score(match):
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.headless = True
    browser = webdriver.Chrome(options=chrome_options)
    browser.set_window_size(7680, 4320)
    stats_1 = 'Опасные атаки'
    stats_2 = 'Удары в створ'
    stats_3 = 'Удары'
    stats_4 = 'Атаки'
    all_good_match = []

    for i in match:
        browser.get(i)
        get_score = browser.find_elements(by=By.XPATH, value="//div[@class='detailScore__wrapper detailScore__live']")
        for score in get_score:
            button_stats = browser.find_elements(by=By.XPATH, value="//button[@class='filter__filter']")

            if int(score.text[0]) == 0 and int(score.text[4]) == 0:  # Проверка на счет 0:0
                try:
                    j = 1  # Это значение что бы не перескакивало со статистики на составы
                    for button in button_stats:
                        stat_name = browser.find_elements(by=By.XPATH, value="//div[@class='stat__categoryName']")  # название строк в статистики
                        stat_home = browser.find_elements(by=By.XPATH, value="//div[@class='stat__homeValue']")  # занчение статистики домашних
                        stat_away = browser.find_elements(by=By.XPATH, value="//div[@class='stat__awayValue']")  # значение статистики гостей
                        good_match = []
                        list_name = [None]  # Список всех имен в таблице статистики
                        value_1 = [None]  # Список для значений таблицы домашних
                        value_2 = [None]  # Список для значений таблицы гостей
                        if j == 1 and button.text != 'СОСТАВЫ':
                            button.click()
                            time.sleep(0.5)
                            j += 1
                        for name in stat_name:  # получение имен, и значеений для домашних и гостей со статистики
                            list_name.append(name.text)

                        for home in stat_home:
                            value_1.append(home.text)

                        for away in stat_away:
                            value_2.append(away.text)

                            # Находим по названию индекс его в статистики и затем по индексу слажживаем два значения и печатаем
                        try:
                            index_value_1 = list_name.index(stats_1)
                            stat_value_1 = int(value_1[index_value_1]) + int(value_2[index_value_1])
                            index_value_2 = list_name.index(stats_2)
                            stat_value_2 = int(value_1[index_value_2]) + int(value_2[index_value_2])
                            index_value_3 = list_name.index(stats_3)
                            stat_value_3 = int(value_1[index_value_3]) + int(value_2[index_value_3])
                            index_value_4 = list_name.index(stats_4)
                            stat_value_4 = int(value_1[index_value_4]) + int(value_2[index_value_4])
                            good_match.append(browser.current_url)  # добавляем ссылку на матч к списку на отправку

                            if stat_value_1 >= 35 and stat_value_2 >= 4 and stat_value_3 >= 10 and stat_value_4 >= 80 and 'Красные карточки' not in list_name:
                                all_good_match.append(browser.current_url)  # в верхний список добавляем главный списко
                                print(all_good_match)
                        except Exception as exc:
                            pass


                except Exception as exc:
                    pass

        time.sleep(0.5)
    if all_good_match == [None]:
        print('Нет подходящего матча!')
    else:
        if all_good_match == []:
            print(f'Матчи отсутствуют')
        return all_good_match
