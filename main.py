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
    QStackedWidget
)

from database.db import add_media, create_table, delete_media, get_media
from ui.add_window import AddWindow
from ui.card_widget import create_card

def go_to_search():
    stacked_widget.setCurrentIndex(1)

def go_back_to_main():
    if search_panel.selected_title:
        title = str(search_panel.selected_title)
        media_type = str(search_panel.selected_type)
        image = str(search_panel.selected_image)

        try:
            score = int(search_panel.selected_score)
        except (TypeError, ValueError):
            score = 0

        try:
            year = int(search_panel.selected_year)
        except (TypeError, ValueError):
            year = 0

        add_media(title, media_type, "", year, image, score)

        search_panel.selected_title= ""
        search_panel.save_button.setEnabled(False)
        search_panel.search_input.clear()
        search_panel.results_list.clear()

    refresh_grid()
    stacked_widget.setCurrentIndex(0)

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

    free_width = scroll.width()
    card_width = 150
    spacing = 15

    COLUMNS_MAX = max(1, free_width // (card_width + spacing))

    for index, row in enumerate(get_media()):
        fila = index // COLUMNS_MAX
        columna = index % COLUMNS_MAX

        card_widget = create_card(
            row[0], row[1], row[2], row[4], row[6], row[5], on_card_clicked
        )
        cards_grid.addWidget(card_widget, fila, columna)

    cards_grid.setColumnStretch(COLUMNS_MAX, 1)

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

# -- Layout --
layout = QVBoxLayout()
layout.setContentsMargins(20, 20, 20, 20)

# -- Scroll --
scroll = QScrollArea()
scroll.setWidgetResizable(True)
scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

# -- Content --
content = QWidget()
content.setStyleSheet("background-color: transparent;")
content_layout = QVBoxLayout(content)
content_layout.setContentsMargins(0, 0, 0, 0)

# -- Grid --
cards_grid = QGridLayout()
cards_grid.setSpacing(15)
content_layout.addLayout(cards_grid)
content_layout.addStretch(1)

scroll.setWidget(content)

button = QPushButton("Buscar y Añadir")
button.setFixedWidth(140)
button.clicked.connect(go_to_search)

bottom_layout = QHBoxLayout()
bottom_layout.addStretch(1)
bottom_layout.addWidget(button)

layout.addWidget(scroll)
layout.addSpacing(10)
layout.addLayout(bottom_layout)

# -- MainPage --
main_page = QWidget()
main_page.setLayout(layout)
search_panel = AddWindow(on_back_callback=go_back_to_main)

stacked_widget = QStackedWidget()
stacked_widget.addWidget(main_page)
stacked_widget.addWidget(search_panel)
root_layout = QVBoxLayout(window)
root_layout.setContentsMargins(0, 0, 0, 0)
root_layout.addWidget(stacked_widget)

window.resizeEvent = lambda event: refresh_grid()

refresh_grid()
window.show()
sys.exit(app.exec())
