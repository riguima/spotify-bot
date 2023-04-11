import pytest
from selenium.webdriver import Remote
from time import sleep

from spotify_bot.use_cases import (
    make_login, create_driver, find_element, register, listen_playlist
)
from spotify_bot.domain import generate_email, generate_password


@pytest.fixture(scope='function')
def driver() -> Remote:
    return create_driver()


def test_make_login(driver: Remote) -> None:
    make_login(driver, 'richard.alexsander.guima@gmail.com', 'Richard23102019')
    find_element(driver, '#account-settings-link')
    assert 'Richard Alexsander' in driver.page_source
    driver.quit()


def test_register_with_existent_account(driver: Remote) -> None:
    assert not register(driver, 'richard.alexsander.guima@gmail.com',
                        'Richard23102019')
    driver.quit()


def test_register_with_non_existent_account(driver: Remote) -> None:
    assert register(driver, generate_email(), generate_password())
    driver.quit()


def test_listen_playlist(driver: Remote) -> None:
    make_login(driver, 'richard.alexsander.guima@gmail.com', 'Richard23102019')
    listen_playlist(driver,
                    'https://open.spotify.com/playlist/5iMQIGGlb10pH5qg87iZ6W?si=moVJZ21jQUSdJ7OtvkyAjw&dd=1&nd=1',
                    10)
    sleep(5)
    assert find_element(driver, 'span[draggable=true] a').text == 'Perfume de Mulher'
    driver.quit()
