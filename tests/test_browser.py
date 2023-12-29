import random

import pytest
from sqlalchemy import select

from spotify_bot.browser import Browser
from spotify_bot.config import get_config
from spotify_bot.database import Session
from spotify_bot.exceptions import InvalidLoginError
from spotify_bot.models import Account


@pytest.fixture(scope="function")
def browser():
    return Browser(headless=False)


def test_make_login(browser):
    browser.make_login(get_config()["EMAIL"], get_config()["PASSWORD"])
    browser.driver.get("https://www.spotify.com/br-pt/account/overview/")
    browser.find_element(".mh-profile-title")


def test_logout(browser):
    browser.make_login(get_config()["EMAIL"], get_config()["PASSWORD"])
    browser.logout()
    browser.make_login(get_config()["EMAIL"], get_config()["PASSWORD"])


def test_make_login_with_invalid_login(browser):
    with pytest.raises(InvalidLoginError):
        browser.make_login("invalidemail@gmail.com", "123456")


def test_register(browser):
    email, password = browser.register()
    with Session() as session:
        query = select(Account).where(Account.email == email)
        model = session.scalars(query).first()
        browser.logout()
        browser.make_login(email, password)
        assert model


def test_listen_playlist(browser):
    browser.make_login(get_config()["EMAIL"], get_config()["PASSWORD"])
    browser.listen_playlist(get_config()["PLAYLIST_URL"])
    last_song = browser.find_elements('div[data-testid="tracklist-row"]')[-1]
    browser.find_element(".RfidWIoz8FON2WhFoItU", wait=5, element=last_song)


def test_listen_playlist_song(browser):
    browser.make_login(get_config()["EMAIL"], get_config()["PASSWORD"])
    browser.driver.get(get_config()["PLAYLIST_URL"])
    songs = browser.find_elements('div[data-testid="tracklist-row"]')
    song_index = random.randint(0, len(songs) - 1)
    song_index = 0
    browser.listen_playlist_song(get_config()["PLAYLIST_URL"], song_index)
    song = browser.find_elements('div[data-testid="tracklist-row"]')[song_index]
    browser.find_element(".RfidWIoz8FON2WhFoItU", wait=5, element=song)
