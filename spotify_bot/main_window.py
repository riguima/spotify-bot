import toml
from PySide6 import QtCore, QtGui, QtWidgets

from spotify_bot.browser import Browser
from spotify_bot.config import get_config
from spotify_bot.database import Session
from spotify_bot.models import Command


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(600, 300)
        self.setWindowTitle("Spotify Bot")
        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.message_box = QtWidgets.QMessageBox()

        self.playlist_url_label = QtWidgets.QLabel("Playlist:")
        self.playlist_url_input = QtWidgets.QLineEdit()
        self.playlist_url_input.setText(get_config().get("PLAYLIST_URL", ""))
        self.playlist_url_input.setValidator(
            QtGui.QRegularExpressionValidator(
                r"https?:\/\/(www\.)?[-a-zA-Z0-9@:%._\+~#=]{1,256}\.[a-zA-Z0-9()]{1,6}\b([-a-zA-Z0-9()@:%_\+.~#?&//=]*)"
            )
        )
        self.playlist_url_layout = QtWidgets.QHBoxLayout()
        self.playlist_url_layout.addWidget(self.playlist_url_label)
        self.playlist_url_layout.addWidget(self.playlist_url_input)

        self.song_index_label = QtWidgets.QLabel("Música:")
        self.song_index_input = QtWidgets.QLineEdit()
        self.song_index_input.setValidator(QtGui.QIntValidator())
        self.song_index_layout = QtWidgets.QHBoxLayout()
        self.song_index_layout.addWidget(self.song_index_label)
        self.song_index_layout.addWidget(self.song_index_input)

        self.amount_label = QtWidgets.QLabel("Quantidade:")
        self.amount_input = QtWidgets.QLineEdit()
        self.amount_input.setValidator(QtGui.QIntValidator())
        self.amount_layout = QtWidgets.QHBoxLayout()
        self.amount_layout.addWidget(self.amount_label)
        self.amount_layout.addWidget(self.amount_input)

        self.add_to_queue_button = QtWidgets.QPushButton("Adicionar a Fila")
        self.add_to_queue_button.clicked.connect(self.add_to_queue)

        self.registrations_amount_label = QtWidgets.QLabel("Quantidade de Contas:")
        self.registrations_amount_input = QtWidgets.QLineEdit()
        self.registrations_amount_input.setValidator(QtGui.QIntValidator())
        self.registrations_amount_layout = QtWidgets.QHBoxLayout()
        self.registrations_amount_layout.addWidget(self.registrations_amount_label)
        self.registrations_amount_layout.addWidget(self.registrations_amount_input)

        self.register_button = QtWidgets.QPushButton("Registrar")
        self.register_button.clicked.connect(self.register)

        self.main_layout = QtWidgets.QVBoxLayout(self)
        self.main_layout.addLayout(self.playlist_url_layout)
        self.main_layout.addLayout(self.song_index_layout)
        self.main_layout.addLayout(self.amount_layout)
        self.main_layout.addWidget(self.add_to_queue_button)
        self.main_layout.addLayout(self.registrations_amount_layout)
        self.main_layout.addWidget(self.register_button)

    @QtCore.Slot()
    def add_to_queue(self):
        with Session() as session:
            song_index = self.song_index_input.text() or None
            amount = self.amount_input.text() or 1
            command = Command(
                playlist_url=self.playlist_url_input.text(),
                song_index=song_index if song_index is None else int(song_index) - 1,
                amount=int(amount),
            )
            session.add(command)
            session.commit()
        for line_edit in [self.song_index_input, self.amount_input]:
            line_edit.setText("")
        config_copy = get_config()
        config_copy["PLAYLIST_URL"] = self.playlist_url_input.text()
        toml.dump(
            config_copy,
            open(
                ".config.toml" if config_copy.get("TESTING") else ".test_config.toml",
                "w",
            ),
        )
        self.message_box.setText("Adicionado a Fila")
        self.message_box.show()

    @QtCore.Slot()
    def register(self):
        browser = Browser(headless=False)
        for _ in range(int(self.registrations_amount_input.text())):
            browser.register()
            browser.logout()
        self.message_box.setText("Conta(s) adicionada(s)")
        self.message_box.show()
