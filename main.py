from database.db import create_table, get_media, add_media

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QListWidget,
    QDialog,
    QLineEdit,
    QComboBox,
    QSpinBox
)


class AddWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Añadir")

        layout = QVBoxLayout()

        self.title = QLineEdit()
        self.title.setPlaceholderText("Título")

        save = QPushButton("Guardar")

        save.clicked.connect(self.accept)

        layout.addWidget(self.title)
        layout.addWidget(save)

        self.setLayout(layout)


def open_form():
    dialog = AddWindow()

    if dialog.exec():
        title = dialog.title.text()

        add_media(
            title,
            "Anime",
            "",
            2025,
            "",
            0
        )

        media_list.addItem(title)


create_table()

app = QApplication([])

window = QWidget()
window.setWindowTitle("YAMV")

layout = QVBoxLayout()

media_list = QListWidget()

button = QPushButton("Añadir")

button.clicked.connect(open_form)

layout.addWidget(button)
layout.addWidget(media_list)

window.setLayout(layout)

for row in get_media():
    media_list.addItem(row[1])

window.show()

app.exec()
