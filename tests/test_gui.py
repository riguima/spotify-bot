from sqlalchemy import select

from spotify_bot.config import get_config
from spotify_bot.database import Session
from spotify_bot.main_window import MainWindow
from spotify_bot.models import Account, Command


def test_add_to_queue(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)
    widget.playlist_url_input.setText(get_config()["PLAYLIST_URL"])
    widget.add_to_queue_button.click()
    assert widget.message_box.isVisible()
    assert get_config()["PLAYLIST_URL"] == widget.playlist_url_input.text()
    with Session() as session:
        command = session.scalars(select(Command)).all()[-1]
        assert command.playlist_url == get_config()["PLAYLIST_URL"]
        assert command.song_index is None
        assert command.amount == 1


def test_add_to_queue_with_song_index_and_amount(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)
    assert widget.playlist_url_input.text() == get_config()["PLAYLIST_URL"]
    widget.song_index_input.setText("2")
    widget.amount_input.setText("1000")
    widget.add_to_queue_button.click()
    assert widget.message_box.isVisible()
    assert not widget.song_index_input.text()
    assert not widget.amount_input.text()
    with Session() as session:
        command = session.scalars(select(Command)).all()[-1]
        assert command.playlist_url == get_config()["PLAYLIST_URL"]
        assert command.song_index == 1
        assert command.amount == 1000


def test_register(qtbot):
    widget = MainWindow()
    qtbot.addWidget(widget)
    widget.registrations_amount_input.setText("2")
    widget.register_button.click()
    assert widget.message_box.isVisible()
    with Session() as session:
        assert len(session.scalars(select(Account)).all()) == 2
