import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options

def enter_site():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(options=chrome_options)
    browser.set_window_size(1920, 1080)

    try:
        browser.get('https://www.flashscore.com.ua/')
        time.sleep(1)

        try:
            button_cookie = browser.find_element(By.ID, 'onetrust-accept-btn-handler')
            button_cookie.click()
        except:
            pass

        click_live = browser.find_element(By.XPATH, "//div[@class='filters__tab']")
        click_live.click()
        time.sleep(1)

        get_all_play = browser.find_elements(By.XPATH, "//div[@class='event__info']")
        actions = ActionChains(browser)

        for open_play in get_all_play:
            try:
                open_play.click()
                time.sleep(0.3)
            except:
                try:
                    actions.move_to_element(open_play).perform()
                except:
                    continue

        browser.execute_script("window.scrollTo(0,0)")
        time.sleep(1)

        get_time = browser.find_elements(By.XPATH, "//div[contains(@class, 'event__stage')]")

        count_game = 0
        list_nums = [str(x) for x in range(30, 75)] + ['Перерыв']
        for minutes in get_time:
            try:
                if str(minutes.text[0:2]) in list_nums:
                    minutes.click()
                    time.sleep(0.5)
                    count_game += 1
            except Exception as ex:
                browser.execute_script("window.scrollTo(250, document.body.scrollHeight);")

        list_match = []
        for i in range(1, count_game + 1):
            try:
                browser.switch_to.window(browser.window_handles[i])
                list_match.append(browser.current_url)
            except Exception as ex:
                print("Ошибка при переключении вкладки:", ex)

        return list_match

    finally:
        browser.quit()


def check_score(match):
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    browser = webdriver.Chrome(options=chrome_options)
    browser.set_window_size(1920, 1080)

    stats_1 = 'Опасные атаки'
    stats_2 = 'Удары в створ'
    stats_3 = 'Удары'
    stats_4 = 'Атаки'
    all_good_match = []

    try:
        for i in match:
            browser.get(i)
            time.sleep(1)

            get_score = browser.find_elements(By.XPATH, "//div[contains(@class,'detailScore__wrapper')]")
            for score in get_score:
                try:
                    if int(score.text[0]) == 0 and int(score.text[4]) == 0:
                        buttons = browser.find_elements(By.XPATH, "//button[contains(@class, 'filter__filter')]")
                        for button in buttons:
                            if button.text.strip() != 'СОСТАВЫ':
                                button.click()
                                time.sleep(0.5)
                                break

                        names = browser.find_elements(By.XPATH, "//div[@class='stat__categoryName']")
                        home = browser.find_elements(By.XPATH, "//div[@class='stat__homeValue']")
                        away = browser.find_elements(By.XPATH, "//div[@class='stat__awayValue']")

                        stat_names = [n.text for n in names]
                        home_values = [h.text for h in home]
                        away_values = [a.text for a in away]

                        def get_stat_sum(name):
                            idx = stat_names.index(name)
                            return int(home_values[idx]) + int(away_values[idx])

                        if all(name in stat_names for name in [stats_1, stats_2, stats_3, stats_4]):
                            s1 = get_stat_sum(stats_1)
                            s2 = get_stat_sum(stats_2)
                            s3 = get_stat_sum(stats_3)
                            s4 = get_stat_sum(stats_4)
                            if s1 >= 35 and s2 >= 4 and s3 >= 10 and s4 >= 80 and 'Красные карточки' not in stat_names:
                                all_good_match.append(i)
                                print("Найден матч:", i)
                except Exception as ex:
                    print("Ошибка в матче:", i, ex)
            time.sleep(0.5)
        return all_good_match

    finally:
        browser.quit()
