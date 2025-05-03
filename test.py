from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.options import Options
import time


def enter_site():
    chrome_options = Options()
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--headless")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.headless = True
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
    list_nums = [str(x) for x in range(30, 75)] + ['Перерыв']

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
    list_match = []
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

enter_site()