from spotify_bot.repositories import AccountRepository
from spotify_bot.use_cases import make_login, listen_playlist, create_driver

from dotenv import load_dotenv


if __name__ == '__main__':
    load_dotenv()
    playlist_url = input('Digite a url da playlist: ')
    for i in range(10):
        for account in AccountRepository().all():
            driver = create_driver()
            print(account)
            try:
                login = make_login(driver, account)
                print(login)
                listen_playlist(driver, playlist_url, 60)
            except Exception:
                continue
            driver.quit()
    driver.quit()
