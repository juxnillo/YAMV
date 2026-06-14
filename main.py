import sys

from PySide6.QtCore import Qt
from PySide6.QtWidgets import (
    QApplication,
    QGridLayout,
    QHBoxLayout,
    QMessageBox,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)

from database.db import add_media, create_table, delete_media, get_media
from ui.add_window import AddWindow
from ui.card_widget import create_card


def open_form():
    dialog = AddWindow()

    if dialog.exec():
        title = str(dialog.selected_title)
        media_type = str(dialog.selected_type)
        image = str(dialog.selected_image)

        try:
            score = int(dialog.selected_score)
        except (TypeError, ValueError):
            score = 0

        try:
            year = int(dialog.selected_year)
            if year == 0:
                year = 0000
        except (TypeError, ValueError):
            year = 0

        add_media(title, media_type, "", year, image, score)
        refresh_grid()


def on_card_clicked(media_id, title):
    confirm = QMessageBox()
    confirm.setWindowTitle("Gestionar Anime")
    confirm.setText(f"Que quieres hacer con: \n\n {title}?")

    delete_btn = confirm.addButton("Eliminar", QMessageBox.DestructiveRole)
    cancel_btn = confirm.addButton("Cancelar", QMessageBox.RejectRole)

    confirm.exec()

    if confirm.clickedButton() == delete_btn:
        delete_media(media_id)
        refresh_grid()


def refresh_grid():
    while cards_grid.count():
        item = cards_grid.takeAt(0)
        if item is not None:
            widget = item.widget()
            if widget is not None:
                widget.deleteLater()
    COLUMNS_MAX = 4

    for index, row in enumerate(get_media()):
        fila = index // COLUMNS_MAX
        columna = index % COLUMNS_MAX

        card_widget = create_card(
            row[0], row[1], row[2], row[4], row[6], row[5], on_card_clicked
        )
        cards_grid.addWidget(card_widget, fila, columna)
        cards_grid.setColumnStretch(columna, 1)


create_table()

app = QApplication([])
app.setStyle("Fusion")

window = QWidget()
window.setWindowTitle("YAMV")
window.resize(700, 600)
window.setStyleSheet("""
    QWidget {
        background-color: #1e1e2e;
        color: #ffffff;
        font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
    }

    QPushButton {
        background-color: #853cdd;
        color: #cdd6f4;
        font-weight: bold;
        font-size: 13px;
        padding: 10px;
        border-radius: 6px;
        border: none;
    }
    QPushButton:hover {
        background-color: #5500bb;
    }
    QPushButton:pressed {
        background-color: #5500bb;
    }

    QScrollArea {
        border: none;
        background-color: transparent;
    }
""")

layout = QVBoxLayout()
layout.setContentsMargins(20, 20, 20, 20)
scroll = QScrollArea()
content = QWidget()
content.setStyleSheet("background-color: transparent;")
cards_grid = QGridLayout()
cards_grid.setSpacing(18)
cards_grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)

content_layout = QHBoxLayout()
content_layout.setContentsMargins(0, 0, 0, 0)
content.setLayout(cards_grid)
content_layout.addStretch(1)
content.setLayout(content_layout)

scroll.setWidget(content)
scroll.setWidgetResizable(True)

button = QPushButton("Buscar y Añadir")
button.clicked.connect(open_form)

layout.addWidget(scroll)
layout.addSpacing(10)
layout.addWidget(button)
window.setLayout(layout)

refresh_grid()
window.show()
sys.exit(app.exec())
