from spotify_bot.repositories import AccountRepository
from spotify_bot.use_cases import make_login, listen_playlist, create_driver

from dotenv import load_dotenv


if __name__ == '__main__':
    driver = create_driver()
    load_dotenv()
    for account in AccountRepository.all():
        make_login(account.email, account.password)
        listen_playlist(driver, os.getenv('PLAYLIST_URL'), 60)
