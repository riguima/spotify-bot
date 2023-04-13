from dotenv import load_dotenv
import os

from spotify_bot.repositories import AccountRepository
from spotify_bot.use_cases import make_login, listen_playlist, create_driver


if __name__ == '__main__':
    load_dotenv()
    driver = create_driver()
    for account in AccountRepository().all():
        for i in range(10):
            login = make_login(driver, account)
            if login:
                listen_playlist(driver, os.getenv('PLAYLIST_URL'), 60)
            else:
                break
    driver.quit()
