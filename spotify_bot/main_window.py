import toml
import os
from PySide6 import QtCore, QtGui, QtWidgets
from sqlalchemy import select

from spotify_bot.browser import Browser
from spotify_bot.config import get_config
from spotify_bot.database import Session
from spotify_bot.models import Command


class TableModel(QtCore.QAbstractTableModel):
    def __init__(self, parent, data, headers, *args):
        super().__init__(parent, *args)
        self._data = data
        self._headers = headers

    def data(self, index, role=QtCore.Qt.DisplayRole):
        if role == QtCore.Qt.DisplayRole:
            return self._data[index.row()][index.column()]

    def rowCount(self, index=None):
        return len(self._data)

    def columnCount(self, index=None):
        return len(self._data[0])

    def headerData(self, column, orientation, role):
        if orientation == QtGui.Qt.Horizontal and role == QtGui.Qt.DisplayRole:
            return self._headers[column]
        return None


class QueueTableKeyPressFilter(QtCore.QObject):
    def eventFilter(self, widget, event):
        if event.type() == QtCore.QEvent.Type.KeyPress:
            scan_code = event.nativeScanCode()
            scan_codes = [328, 336] if os.name == 'nt' else [111, 116]
            if scan_code in scan_codes:
                try:
                    data = widget.model()._data[widget.selectedIndexes()[0].row()]
                    with Session() as session:
                        model = session.get(Command, data[0])
                        if scan_code == scan_codes[0] and data[4] != 0:
                            query = select(Command).where(
                                Command.order == model.order - 1
                            )
                            old_model = session.scalars(query).first()
                            old_model.order += 1
                            model.order -= 1
                        elif (
                            scan_code == scan_codes[1]
                            and data[4] != len(widget.model()._data) - 1
                        ):
                            query = select(Command).where(
                                Command.order == model.order + 1
                            )
                            old_model = session.scalars(query).first()
                            old_model.order -= 1
                            model.order += 1
                        session.commit()
                    self.parent().update_queue_table()
                except IndexError:
                    pass
        return False


class MainWindow(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()
        self.setFixedSize(1000, 400)
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

        self.inputs_layout = QtWidgets.QVBoxLayout()
        self.inputs_layout.addLayout(self.playlist_url_layout)
        self.inputs_layout.addLayout(self.song_index_layout)
        self.inputs_layout.addLayout(self.amount_layout)
        self.inputs_layout.addWidget(self.add_to_queue_button)
        self.inputs_layout.addLayout(self.registrations_amount_layout)
        self.inputs_layout.addWidget(self.register_button)

        self.queue_table_label = QtWidgets.QLabel(
            "Fila", alignment=QtCore.Qt.AlignmentFlag.AlignCenter
        )
        self.queue_table_label.setStyleSheet("font-weight: bold;")
        self.queue_table = QtWidgets.QTableView()
        self.update_queue_table()
        self.queue_table.setColumnHidden(0, True)
        self.queue_table.setColumnHidden(4, True)
        self.queue_table.installEventFilter(QueueTableKeyPressFilter(parent=self))
        self.remove_from_queue_button = QtWidgets.QPushButton("Remover da Fila")
        self.remove_from_queue_button.clicked.connect(self.remove_from_queue)
        self.queue_table_layout = QtWidgets.QVBoxLayout()
        self.queue_table_layout.addWidget(self.queue_table_label)
        self.queue_table_layout.addWidget(self.queue_table)
        self.queue_table_layout.addWidget(self.remove_from_queue_button)

        self.main_layout = QtWidgets.QHBoxLayout(self)
        self.main_layout.addLayout(self.inputs_layout)
        self.main_layout.addLayout(self.queue_table_layout)

    @QtCore.Slot()
    def add_to_queue(self):
        with Session() as session:
            song_index = self.song_index_input.text() or None
            amount = self.amount_input.text() or 1
            command = Command(
                playlist_url=self.playlist_url_input.text(),
                song_index=song_index if song_index is None else int(song_index) - 1,
                amount=int(amount),
                order=len(session.scalars(select(Command)).all()),
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
        self.update_queue_table()
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

    @QtCore.Slot()
    def remove_from_queue(self):
        with Session() as session:
            for index in self.queue_table.selectedIndexes():
                model = session.get(
                    Command, self.queue_table.model()._data[index.row()][0]
                )
                session.delete(model)
            session.commit()
        self.update_queue_table()

    def update_queue_table(self):
        headers = ["ID", "Playlist URL", "Música", "Quantidade", "Ordem"]
        data = []
        with Session() as session:
            for command in session.scalars(select(Command)).all():
                song_index = 0 if command.song_index is None else command.song_index + 1
                data.append(
                    [
                        command.id,
                        command.playlist_url,
                        song_index,
                        command.amount,
                        command.order,
                    ]
                )
        if not data:
            data = [["" for _ in headers]]
        data.sort(key=lambda r: r[4])
        self.queue_table.setModel(TableModel(self, data, headers))
