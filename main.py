from dotenv import load_dotenv

from spotify_bot.repositories import AccountRepository
from spotify_bot.use_cases import listen_playlist


if __name__ == '__main__':
    load_dotenv()
    playlist_url = input('Digite a url da playlist: ')
    drivers_amount = int(input('Rodar em quantos navegadores? '))
    accounts = AccountRepository().all()
    for i in range(len(accounts) // drivers_amount):
        listen_playlist(
            accounts[i * drivers_amount:i * drivers_amount + drivers_amount],
            playlist_url)
