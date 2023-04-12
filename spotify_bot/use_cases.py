from selenium.webdriver import Remote
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.action_chains import ActionChains
from dotenv import load_dotenv
from time import sleep
import re

from spotify_bot.domain import Account


load_dotenv()


def create_driver() -> Remote:
    options = Options()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')
    return Remote(
        command_executor='http://localhost:4444/wd/hub',
        options=options
    )


def make_logins(driver: Remote, accounts: list[Account]) -> bool:
    for i in range(len(accounts)):
        find_element(driver, 'body').send_keys(Keys.COMMAND + 't')
    for i, window in enumerate(driver.window_handles):
        driver.switch_to.window(window)
        make_login(driver, accounts[i])
        try:
            find_element(driver, '#account-settings-link')
        except TimeoutException:
            return False
    return True


def make_login(driver: Remote, account: Account) -> bool:
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


def register(driver: Remote, account: Account) -> bool:
    driver.delete_all_cookies()
    driver.get('https://www.spotify.com/br-pt/signup')
    find_element(driver, '#email').send_keys(account.email)
    try:
        find_element(driver, '#confirm').send_keys(account.email)
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
        find_element(driver, '.Linux__Container-owbdmj-0')
    except TimeoutException:
        return False
    return True


def listen_playlist(driver: Remote, playlist_url: str, wait: int) -> None:
    driver.get(playlist_url)
    hover = ActionChains(driver).move_to_element(
        find_element(driver, 'div[aria-rowindex="2"]')
    )
    hover.perform()
    find_element(driver, '.RfidWIoz8FON2WhFoItU').click()
    regex = re.compile(r'(\d{1,}) songs')
    for c in range(int(regex.findall(driver.page_source)[0]) - 1):
        sleep(wait)
        click(driver, 'button[aria-label=Next]')


def click(driver: Remote, selector: str) -> None:
    driver.execute_script('arguments[0].click();',
                          find_element(driver, selector))


def find_element(driver: Remote, selector: str, wait: int = 20):
    return WebDriverWait(driver, wait).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def find_elements(driver: Remote, selector: str, wait: int = 20):
    return WebDriverWait(driver, wait).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
