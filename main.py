from dotenv import load_dotenv

from spotify_bot.repositories import AccountRepository
from spotify_bot.use_cases import listen_playlist, make_login, create_driver


if __name__ == '__main__':
    load_dotenv()
    playlist_url = input('Digite a url da playlist: ')
    drivers_amount = int(input('Rodar em quantos navegadores? '))
    accounts = AccountRepository().all()
    for _ in range(10):
        for i in range(len(accounts) // drivers_amount):
            while True:
                listen_accounts = accounts[
                    i * drivers_amount:i * drivers_amount + drivers_amount]
                driver = create_driver(visible=True)
                make_logins = [make_login(driver, a) for a in listen_accounts]
                driver.quit()
                if make_logins.count(False) == 0:
                    break
                for e, login in enumerate(make_logins):
                    if not login:
                        del accounts[e]
            listen_playlist(listen_accounts, playlist_url)
