import random
import threading

from sqlalchemy import select

from spotify_bot.browser import Browser
from spotify_bot.config import get_config
from spotify_bot.database import Session
from spotify_bot.models import Account, Command


def run_command(command):
    with Session() as session:
        account = random.choice(session.scalars(select(Account)).all())
        browser = Browser(headless=False)
        browser.make_login(account.email, account.password)
        if command.song_index is None:
            browser.listen_playlist(command.playlist_url)
        else:
            browser.listen_playlist_song(command.playlist_url, command.song_index)
        command.amount -= 1
        session.commit()


if __name__ == "__main__":
    with Session() as session:
        while True:
            query = select(Command).where(Command.amount == 0)
            for command in session.scalars(query).all():
                session.delete(command)
                session.commit()
            for command in session.scalars(select(Command)).all():
                for _ in range(command.amount):
                    while True:
                        if len(threading.enumerate()) <= get_config()["BROWSERS_COUNT"]:
                            threading.Thread(target=run_command, args=[command]).start()
                            break
