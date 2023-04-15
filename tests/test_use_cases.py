import pytest
from selenium.webdriver import Chrome

from spotify_bot.use_cases import (
    make_login, create_driver, register, listen_playlist
)
from spotify_bot.repositories import AccountRepository
from spotify_bot.domain import generate_email, Account


@pytest.fixture(scope='module')
def driver() -> Chrome:
    return create_driver(visible=True)


def test_make_login(driver: Chrome) -> None:
    assert make_login(
        driver,
        Account('richard.alexsander.guima@gmail.com', 'Richard23102019!'))


def test_register_with_existent_account(driver: Chrome) -> None:
    assert not register(
        driver,
        Account('richard.alexsander.guima@gmail.com', 'Richard23102019!'))


def test_register_with_non_existent_account(driver: Chrome) -> None:
    assert register(driver, Account(generate_email(), 'Ri12345678!'))


def test_listen_playlist() -> None:
    listen_playlist(AccountRepository().all()[:3],
                    'https://open.spotify.com/playlist/5iMQIGGlb10pH5qg87iZ6W')
