import pytest
from sqlalchemy import select

from spotify_bot.config import get_config
from spotify_bot.database import Session, db
from spotify_bot.main_window import MainWindow
from spotify_bot.models import Account, Base, Command


@pytest.fixture(scope="function")
def session():
    Base.metadata.drop_all(db)
    Base.metadata.create_all(db)
    return Session()


def test_add_to_queue(qtbot, session):
    widget = MainWindow()
    qtbot.addWidget(widget)
    widget.playlist_url_input.setText(get_config()["PLAYLIST_URL"])
    widget.add_to_queue_button.click()
    assert widget.message_box.isVisible()
    assert get_config()["PLAYLIST_URL"] == widget.playlist_url_input.text()
    command = session.scalars(select(Command)).all()[-1]
    assert command.playlist_url == get_config()["PLAYLIST_URL"]
    assert command.song_index is None
    assert command.amount == 1
    assert command.order == 0


def test_add_to_queue_with_song_index_and_amount(qtbot, session):
    widget = MainWindow()
    qtbot.addWidget(widget)
    assert widget.playlist_url_input.text() == get_config()["PLAYLIST_URL"]
    widget.song_index_input.setText("2")
    widget.amount_input.setText("1000")
    widget.add_to_queue_button.click()
    assert widget.message_box.isVisible()
    assert not widget.song_index_input.text()
    assert not widget.amount_input.text()
    command = session.scalars(select(Command)).all()[-1]
    assert command.playlist_url == get_config()["PLAYLIST_URL"]
    assert command.song_index == 1
    assert command.amount == 1000
    assert command.order == 0


def test_register(qtbot, session):
    widget = MainWindow()
    qtbot.addWidget(widget)
    widget.registrations_amount_input.setText("2")
    widget.register_button.click()
    assert widget.message_box.isVisible()
    assert len(session.scalars(select(Account)).all()) == 2


def test_queue_table(qtbot, session):
    widget = MainWindow()
    qtbot.addWidget(widget)
    widget.playlist_url_input.setText(get_config()["PLAYLIST_URL"])
    widget.song_index_input.setText("5")
    widget.amount_input.setText("500")
    assert widget.queue_table.model()._data[0] == ["" for _ in range(5)]
    widget.add_to_queue_button.click()
    data = widget.queue_table.model()._data[0]
    assert data == [1, get_config()["PLAYLIST_URL"], 5, 500, 0]
