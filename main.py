from dotenv import load_dotenv

from spotify_bot.repositories import AccountRepository
from spotify_bot.use_cases import listen_playlist, make_login


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
                make_logins = [make_login(a) for a in listen_accounts]
                if make_logins.count(False) > 0:
                    del accounts[make_logins.index(False)]
                else:
                    break
            listen_playlist(listen_accounts, playlist_url)
