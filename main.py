import sys
from database.db import create_table, get_media, add_media, delete_media
from ui.add_window import AddWindow
from ui.card_widget import create_card

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QScrollArea,
    QGridLayout,
    QMessageBox,
)
from PySide6.QtCore import Qt


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

        add_media(
            title,
            media_type,
            "",
            2026,
            image,
            score
        )
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
        widget = item.widget()
        if widget is not None:
            widget.deleteLater()
    COLUMNS_MAX = 4

    for index, row in enumerate(get_media()):
        fila = index // COLUMNS_MAX
        columna = index % COLUMNS_MAX

        card_widget = create_card(row[0], row[1], row[2], row[6], row[5], on_card_clicked)
        cards_grid.addWidget(card_widget, fila, columna)

create_table()

app = QApplication([])
app.setStyle("Fusion")

window = QWidget()
window.setWindowTitle("YAMV")
window.resize(700, 600)
window.setStyleSheet("QWidget { background-color: #1e1e1e; color: white; } QPushButton { background-color: #3e3e3e; padding: 8px; border-radius: 4px; }")

layout = QVBoxLayout()
scroll = QScrollArea()
content = QWidget()
cards_grid = QGridLayout()
cards_grid.setSpacing(15)
cards_grid.setAlignment(Qt.AlignTop | Qt.AlignLeft)

content.setLayout(cards_grid)
scroll.setWidget(content)
scroll.setWidgetResizable(True)

button = QPushButton("Buscar y Añadir")
button.clicked.connect(open_form)

layout.addWidget(button)
layout.addWidget(scroll)

window.setLayout(layout)

refresh_grid()
window.show()
sys.exit(app.exec())
