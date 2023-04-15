from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from webdriver_manager.chrome import ChromeDriverManager
from dotenv import load_dotenv
from time import sleep
import re

from spotify_bot.domain import Account


load_dotenv()


def create_driver(visible: bool = False) -> Chrome:
    options = Options()
    if not visible:
        options.add_argument('--headless')
        options.add_argument('--no-sandbox')
    return Chrome(options=options,
                  service=Service(ChromeDriverManager().install()))


def make_login(driver: Chrome, account: Account) -> bool:
    driver.delete_all_cookies()
    driver.get('https://accounts.spotify.com/en/login')
    find_element(driver, '#login-username').send_keys(account.email)
    find_element(driver, '#login-password').send_keys(account.password)
    find_element(driver, '#login-button').click()
    try:
        find_element(driver, '#account-settings-link')
    except TimeoutException:
        return False
    return True


def register(driver: Chrome, account: Account) -> bool:
    driver.delete_all_cookies()
    driver.get('https://www.spotify.com/br-pt/signup')
    find_element(driver, '#email').send_keys(account.email)
    try:
        find_element(driver, '#confirm', 5).send_keys(account.email)
    except TimeoutException:
        pass
    find_element(driver, '#password').send_keys(account.password)
    find_element(driver, '#displayname').send_keys(account.email)
    find_element(driver, '#day').send_keys('10')
    find_element(driver, '#year').send_keys('2000')
    click(driver, '#month')
    month = find_element(driver, '#month')
    month.send_keys('January')
    month.send_keys(Keys.RETURN)
    click(driver, '#gender_option_male')
    click(driver, '#marketing-opt-checkbox')
    click(driver, '#terms-conditions-checkbox')
    month.submit()
    try:
        click(driver, 'button[name=solve]')
    except TimeoutException:
        pass
    try:
        find_element(driver, '.Linux__Container-owbdmj-0', 5)
    except TimeoutException:
        return False
    return make_login(driver, account)


def listen_playlist(accounts: list[Account], playlist_url: str) -> None:
    drivers = [create_driver(visible=True) for i in range(len(accounts))]
    for i, account in enumerate(accounts):
        if make_login(drivers[i], account):
            drivers[i].get(playlist_url)
            hover = ActionChains(drivers[i]).move_to_element(
                find_element(drivers[i], 'div[aria-rowindex="2"]')
            )
            hover.perform()
            find_element(drivers[i], '.RfidWIoz8FON2WhFoItU').click()
    regex = re.compile(r'(\d+) min (\d+) sec')
    time = find_element(drivers[0], '.UyzJidwrGk3awngSGIwv').text
    minutes, seconds = regex.findall(time)[0]
    sleep(int(minutes) * 60 + int(seconds))
    for driver in drivers:
        driver.quit()


def click(driver: Chrome, selector: str) -> None:
    driver.execute_script('arguments[0].click();',
                          find_element(driver, selector))


def find_element(driver: Chrome, selector: str, wait: int = 20):
    return WebDriverWait(driver, wait).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def find_elements(driver: Chrome, selector: str, wait: int = 20):
    return WebDriverWait(driver, wait).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
