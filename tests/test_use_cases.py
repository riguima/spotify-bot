import pytest
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep

from spotify_bot.use_cases import (
    make_login, create_driver, find_element, register, listen_playlist
)
from spotify_bot.domain import generate_email, generate_password


@pytest.fixture(scope='function')
def driver() -> Chrome:
    return Chrome(service=Service(ChromeDriverManager().install()))
    #return create_driver()


def test_make_login(driver) -> None:
    make_login(driver, 'richard.alexsander.guima@gmail.com', 'Richard23102019')
    find_element(driver, '#account-settings-link')
    assert 'Richard Alexsander' in driver.page_source
    driver.close()


def test_register(driver) -> None:
    assert not register(driver, 'richard.alexsander.guima@gmail.com',
                        'Richard23102019')
    assert register(driver, generate_email(), generate_password())
    driver.close()


def test_listen_playlist(driver) -> None:
    make_login(driver, 'richard.alexsander.guima@gmail.com', 'Richard23102019')
    find_element(driver, '#account-settings-link')
    listen_playlist(driver,
                    'https://open.spotify.com/album/1ZIOn3boIPlcctKdVNNHRm', 5)
    sleep(5)
    assert find_element(driver, 'span[draggable=true] a').text == 'O Que Falta Em Você Sou Eu'
    driver.close()
