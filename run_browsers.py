import random
import sys
import threading
from time import sleep

from sqlalchemy import select

from spotify_bot.browser import Browser
from spotify_bot.config import get_config
from spotify_bot.database import Session
from spotify_bot.models import Account, Command

running_commands = []


def run_command(command, min_sleep, max_sleep):
    global running_commands
    with Session() as session:
        try:
            account = random.choice(session.scalars(select(Account)).all())
        except IndexError:
            return
        browser = Browser(headless=False)
        browser.make_login(account.email, account.password)
        if command.song_index is None:
            browser.listen_playlist(command.playlist_url, min_sleep, max_sleep)
        else:
            browser.listen_playlist_song(
                command.playlist_url, command.song_index, min_sleep, max_sleep
            )
        running_commands.remove(command)


def main(min_sleep=90, max_sleep=120):
    global running_commands
    with Session() as session:
        while True:
            query = select(Command).where(Command.amount == 0)
            for command in session.scalars(query).all():
                if not running_commands:
                    session.delete(command)
                    session.commit()
            query = select(Command).order_by(Command.order)
            command = session.scalars(query).first()
            if command:
                num_threads = len(threading.enumerate())
                for _ in range(
                    min(
                        command.amount,
                        get_config()['BROWSERS_COUNT'] - (num_threads - 1),
                    )
                ):
                    command.amount -= 1
                    session.commit()
                    running_commands.append(command)
                    threading.Thread(
                        target=run_command,
                        args=[command, min_sleep, max_sleep],
                    ).start()


if __name__ == '__main__':
    if len(sys.argv) == 3:
        min_sleep, max_sleep = sys.argv[1:]
        main(int(min_sleep), int(max_sleep))
    else:
        main()
