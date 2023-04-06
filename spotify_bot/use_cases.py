from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from dotenv import load_dotenv
from time import sleep


load_dotenv()

def create_driver() -> Chrome:
    options = Options()
    options.add_argument('-headless')
    return Chrome(options=options, service=Service(
        ChromeDriverManager().install())
    )


def make_login(driver: Chrome, username: str, password: str) -> None:
    driver.get('https://accounts.spotify.com/en/login')
    driver.find_element(By.CSS_SELECTOR, '#login-username').send_keys(username)
    driver.find_element(By.CSS_SELECTOR, '#login-password').send_keys(password)
    driver.find_element(By.CSS_SELECTOR, '#login-button').click()


def register(driver: Chrome, email: str, password: str) -> bool:
    driver.get('https://www.spotify.com/br-pt/signup')
    find_element(driver, '#email').send_keys(email)
    find_element(driver, '#confirm').send_keys(email)
    click(driver, '#password')
    find_element(driver, '#password').send_keys(password)
    find_element(driver, '#displayname').send_keys(email)
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
        find_element(driver, '.Linux__Container-owbdmj-0')
    except TimeoutException:
        return False
    return True


def listen_playlist(driver: Chrome, playlist_url: str, wait: int) -> None:
    driver.get(playlist_url)
    click(driver, 'span.ButtonInner-sc-14ud5tc-0')
    click(driver, 'span.ButtonInner-sc-14ud5tc-0')
    for c in range(len(find_elements(driver, '.h4HgbO_Uu1JYg5UGANeQ'))):
        sleep(wait)
        find_element(driver, 'button[aria-label=Next]').click()


def click(driver: Chrome, selector: str) -> None:
    driver.execute_script('arguments[0].click();', find_element(driver, selector))


def find_element(driver: Chrome, selector: str, wait: int = 20):
    return WebDriverWait(driver, wait).until(
        EC.presence_of_element_located((By.CSS_SELECTOR, selector))
    )


def find_elements(driver: Chrome, selector: str, wait: int = 20):
    return WebDriverWait(driver, wait).until(
        EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
    )
