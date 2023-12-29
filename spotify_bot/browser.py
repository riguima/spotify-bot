import random
from time import sleep

import pyautogui
from faker import Faker
from selenium.common.exceptions import TimeoutException
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.wait import WebDriverWait
from webdriver_manager.chrome import ChromeDriverManager

from spotify_bot.database import Session
from spotify_bot.exceptions import InvalidLoginError, RegistrationError
from spotify_bot.models import Account


class Browser:
    def __init__(self, headless=True):
        options = Options()
        options.add_argument("--start-maximized")
        if headless:
            options.add_argument("--headless")
            options.add_argument("--no-sandbox")
        self.fake = Faker("pt_BR")
        self.driver = Chrome(
            service=Service(ChromeDriverManager().install()), options=options
        )

    def register(self):
        self.driver.get("https://www.spotify.com/br-pt/signup")
        email = self.fake.email()
        password = self.fake.password()
        self.fill_email_and_password(email, password)
        self.fill_account_info()
        self.accept_terms()
        self.solve_captcha()
        for i in range(5):
            try:
                self.find_element(".mh-profile-title", wait=1)
                sleep(1)
            except TimeoutException:
                if i == 4:
                    raise RegistrationError()
        with Session() as session:
            account = Account(email=email, password=password)
            session.add(account)
            session.commit()
        return email, password

    def fill_email_and_password(self, email, password):
        self.find_element("#username").send_keys(email)
        sleep(1)
        self.find_element('button[data-testid="submit"]').click()
        self.find_element("#new-password").send_keys(password)
        sleep(1)
        self.find_element('button[data-testid="submit"]').click()

    def fill_account_info(self):
        self.find_element("#displayName").send_keys(self.fake.name())
        try:
            self.find_element("#day", wait=5)
        except TimeoutException:
            self.find_element('button[data-testid="submit"]').click()
        birth_date = self.fake.date_of_birth(minimum_age=18)
        self.find_element("#day").send_keys(str(birth_date.day))
        select = Select(self.find_element("#month"))
        select.select_by_value(str(birth_date.month + 1))
        self.find_element("#year").send_keys(str(birth_date.year))
        self.find_elements(".Indicator-sc-hjfusp-0")[random.randint(0, 1)].click()
        self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        sleep(1)
        self.find_element('button[data-testid="submit"]').click()

    def accept_terms(self):
        marketing, _, terms = self.find_elements(".Indicator-sc-1airx73-0")
        marketing.click()
        terms.click()
        sleep(1)
        self.find_element('button[data-testid="submit"]').click()

    def solve_captcha(self):
        found_captcha = False
        for _ in range(10):
            try:
                location = pyautogui.locateOnScreen(
                    "screenshots/captcha.png", confidence=0.9
                )
                center = pyautogui.center(location)
                pyautogui.click(center.x, center.y)
                found_captcha = True
                break
            except pyautogui.ImageNotFoundException:
                sleep(.5)
        if not found_captcha:
            return
        sleep(1)
        while True:
            try:
                pyautogui.locateOnScreen("screenshots/continue.png", confidence=0.9)
                break
            except pyautogui.ImageNotFoundException:
                continue
        sleep(1)
        self.find_element("button[name=solve]").click()

    def make_login(self, email, password):
        self.driver.get("https://accounts.spotify.com/pt-BR/login")
        self.find_element("#login-username").send_keys(email)
        self.find_element("#login-password").send_keys(password)
        self.find_element("#login-button").click()
        for _ in range(5):
            try:
                self.find_element("#login-button", wait=1)
                sleep(1)
            except TimeoutException:
                return
        raise InvalidLoginError()

    def logout(self):
        self.driver.get("https://open.spotify.com")
        self.find_element('button[data-testid="user-widget-link"]').click()
        self.find_element('button[data-testid="user-widget-dropdown-logout"]').click()
        sleep(3)

    def listen_playlist(self, url):
        self.driver.get(url)
        self.find_element(".onetrust-close-btn-handler").click()
        add_button = self.find_element('.dAlRsJ[data-testid="add-button"]')
        if add_button.get_attribute("aria-checked") == "false":
            add_button.click()
        for _ in range(2):
            self.find_elements('button[data-testid="play-button"]')[1].click()
        for i in range(len(self.find_elements('div[data-testid="tracklist-row"]'))):
            if i != 0:
                self.find_element('button[data-testid="control-button-skip-forward"]').click()
            sleep(random.uniform(1.5, 2) * 60)

    def listen_playlist_song(self, url, song_index):
        self.driver.get(url)
        self.find_element(".onetrust-close-btn-handler").click()
        add_button = self.find_element('.dAlRsJ[data-testid="add-button"]')
        if add_button.get_attribute("aria-checked") == "false":
            add_button.click()
        for _ in range(2):
            self.find_elements('button[data-testid="play-button"]')[1].click()
        for _ in range(song_index):
            self.find_element('button[data-testid="control-button-skip-forward"]').click()
        sleep(random.uniform(1.5, 2) * 60)

    def find_element(self, selector, element=None, wait=30):
        element = element or self.driver
        return WebDriverWait(element, wait).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, selector))
        )

    def find_elements(self, selector, element=None, wait=30):
        element = element or self.driver
        return WebDriverWait(element, wait).until(
            EC.presence_of_all_elements_located((By.CSS_SELECTOR, selector))
        )

    def __del__(self):
        self.driver.quit()
