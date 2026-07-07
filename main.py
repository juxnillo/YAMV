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
    QStackedWidget,
)

from database.db import add_media, create_table, delete_media, get_media
from ui.add_window import AddWindow
from ui.card_widget import create_card

# -- Constantes --
WINDOW_TITLE = "YAMV"
WINDOW_SIZE = (700, 600)
CARD_WIDTH = 150
CARD_SPACING = 15
SEARCH_BUTTON_WIDTH = 140

MAIN_STYLE = """
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
"""


class MainWindow(QWidget):

    def __init__(self):
        super().__init__()
        self.setWindowTitle(WINDOW_TITLE)
        self.resize(*WINDOW_SIZE)
        self.setStyleSheet(MAIN_STYLE)

        self.search_panel = AddWindow(on_back_callback=self.go_back_to_main)
        self.cards_grid = QGridLayout()
        self.scroll_area = QScrollArea()

        self.build_ui()
        self.resizeEvent = lambda event: self.refresh_grid()
        self.refresh_grid()

    def build_ui(self):
        main_page = self.build_main_page()

        self.stacked_widget = QStackedWidget()
        self.stacked_widget.addWidget(main_page)
        self.stacked_widget.addWidget(self.search_panel)

        root_layout = QVBoxLayout(self)
        root_layout.setContentsMargins(0, 0, 0, 0)
        root_layout.addWidget(self.stacked_widget)

    def build_main_page(self):
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(
            Qt.ScrollBarPolicy.ScrollBarAlwaysOff
        )

        content = QWidget()
        content.setStyleSheet("background-color: transparent;")
        content_layout = QVBoxLayout(content)
        content_layout.setContentsMargins(0, 0, 0, 0)

        self.cards_grid.setSpacing(CARD_SPACING)
        content_layout.addLayout(self.cards_grid)
        content_layout.addStretch(1)

        self.scroll_area.setWidget(content)

        search_button = QPushButton("Buscar y Añadir")
        search_button.setFixedWidth(SEARCH_BUTTON_WIDTH)
        search_button.clicked.connect(self.go_to_search)

        bottom_layout = QHBoxLayout()
        bottom_layout.addStretch(1)
        bottom_layout.addWidget(search_button)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.addWidget(self.scroll_area)
        layout.addSpacing(10)
        layout.addLayout(bottom_layout)

        main_page = QWidget()
        main_page.setLayout(layout)

        return main_page

    def go_to_search(self):
        self.stacked_widget.setCurrentIndex(1)

    def go_back_to_main(self):
        if self.search_panel.selected_title:
            self.save_selected_media()
            self.reset_search_panel()

        self.refresh_grid()
        self.stacked_widget.setCurrentIndex(0)

    def save_selected_media(self):
        title = str(self.search_panel.selected_title)
        media_type = str(self.search_panel.selected_type)
        image = str(self.search_panel.selected_image)

        try:
            score = int(self.search_panel.selected_score)
        except TypeError, ValueError:
            score = 0

        try:
            year = int(self.search_panel.selected_year)
        except TypeError, ValueError:
            year = 0

        add_media(title, media_type, "", year, image, score)

    def reset_search_panel(self):
        self.search_panel.selected_title = ""
        self.search_panel.save_button.setEnabled(False)
        self.search_panel.search_input.clear()
        self.search_panel.results_list.clear()

    # -- Grid de tarjetas --
    def on_card_clicked(self, media_id, title):
        confirm = QMessageBox()
        confirm.setWindowTitle("Gestionar Anime")
        confirm.setText(f"Que quieres hacer con: \n\n {title}?")

        delete_btn = confirm.addButton(
            "Eliminar", QMessageBox.ButtonRole.DestructiveRole
        )
        confirm.addButton("Cancelar", QMessageBox.ButtonRole.RejectRole)

        confirm.exec()

        if confirm.clickedButton() == delete_btn:
            delete_media(media_id)
            self.refresh_grid()

    def refresh_grid(self):
        self.clear_grid()

        columns = self.columns_that_fit()
        for index, row in enumerate(get_media()):
            row_index = index // columns
            col_index = index % columns
            card_widget = create_card(
                row[0], row[1], row[2], row[4], row[6], row[5], self.on_card_clicked
            )
            self.cards_grid.addWidget(card_widget, row_index, col_index)

        self.cards_grid.setColumnStretch(columns, 1)

    def clear_grid(self):
        while self.cards_grid.count():
            item = self.cards_grid.takeAt(0)
            if item is not None:
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()

    def columns_that_fit(self):
        free_width = self.scroll_area.width()
        return max(1, free_width // (CARD_WIDTH + CARD_SPACING))


def main():
    create_table()

    app = QApplication(sys.argv)
    app.setStyle("Fusion")

    window = MainWindow()
    window.show()

    sys.exit(app.exec())


if __name__ == "__main__":
    main()
