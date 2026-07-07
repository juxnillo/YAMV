import requests
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QLineEdit,
    QListWidget,
    QListWidgetItem,
    QPushButton,
    QVBoxLayout,
    QWidget,
)

from models.anime_model import search_anime_api

# -- Stylesheet --
ADD_WINDOW_STYLE = """
            QWidget {
                background-color: #1e1e2e;
                font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
            }

            QLineEdit {
                background-color: #1e1e2e;
                color: white;
                border-radius: 6px;
                padding: 8px 12px;
                font-size: 13px;
            }
            QLineEdit:focus {
                border: 1px solid #853cdd;
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

            QPushButton:disabled {
                background-color: #853cdd;
                color: #545456;
            }

            QPushButton#BackBtn {
                background-color: #853cdd;
                border-radius: 16px;
                padding: 0px;
            }

            QPushButton#BackBtn:hover {
                 background-color: #5500bb;
            }
            QPushButton#BackBtn:pressed {
                 background-color: #29015a;
            }

            QPushButton#SearchBtn {
                background-color: #853cdd;
                border-radius: 11px;
            }

            QPushButton#SearchBtn:hover {
                 background-color: #5500bb;
            }
            QPushButton#SearchBtn:pressed {
                 background-color: #29015a;
            }

            QPushButton#SaveBtn {
                background-color: #853cdd;
                border-radius: 16px;
                color: white;
            }
            QPushButton#SaveBtn:hover {
                background-color: #5500bb;
            }
            QPushButton#SaveBtn:pressed {
                background-color: #29015a;
            }

            QListWidget {
                background-color: #1e1e2e;
                color: #e5e5ea;
                border: none;
                border-radius: 8px;
                outline: none;
                padding: 5px;
                font-size: 13px;
                show-decoration-selected: 1;
            }
            QListWidget::item {
                margin: 5px 0px;
                padding: 8px;
                background-color: transparent;
                border-radius: 8px;
                border: 1px solid transparent;
            }
            QListWidget::item:hover {
                background-color: #2a2a3c;
            }
            QListWidget::item:selected {
                background-color: #313244;
                color: white;
                border: 1px solid #853cdd;
            }
        """

# -- Constantes de layout --
CARD_IMG_SIZE = (60, 85)
CARD_ITEM_HEIGHT = 105
ICON_SIZE = QSize(20, 20)
NAV_BTN_SIZE = 40


class ResultCard(QWidget):
    """Resultado de la busqueda: imagen + titulo/info."""

    def __init__(self, title, anime_type, score, image_url, year):
        super().__init__()
        self.setStyleSheet("background-color: transparent;")
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        self.image_label = self.build_image_label(image_url)
        text_layout = self.build_text_layout(title, anime_type, score, year)

        layout.addWidget(self.image_label)
        layout.addLayout(text_layout)
        self.setLayout(layout)

    def build_image_label(self, image_url):
        label = QLabel()
        label.setFixedSize(*CARD_IMG_SIZE)
        label.setStyleSheet("border-radius: 4px; background-color: transparent;")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        if image_url.startswith("http"):
            pixmap = self.download_pixmap(image_url)
            if pixmap is not None:
                label.setPixmap(
                    pixmap.scaled(
                        *CARD_IMG_SIZE,
                        Qt.AspectRatioMode.KeepAspectRatio,
                        Qt.TransformationMode.SmoothTransformation,
                    )
                )
            else:
                label.setText("No Img")
        else:
            label.setText("🍿")

        return label

    @staticmethod
    def download_pixmap(image_url):
        """Fetch de imagen a QPixmap"""
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            img_data = requests.get(image_url, headers=headers, timeout=3).content
        except Exception:
            return None

        pixmap = QPixmap()
        pixmap.loadFromData(img_data)
        return pixmap

    @staticmethod
    def build_text_layout(title, anime_type, score, year):
        text_layout = QVBoxLayout()

        title_label = QLabel(f"<b>{title}</b>")
        title_label.setStyleSheet(
            "color: white; font-size: 14px; background-color: transparent;"
        )
        title_label.setWordWrap(True)

        display_year = f"({year})" if year else ""

        info_label = QLabel(f"{anime_type} {display_year} ·  ⭐ {score}/10")
        info_label.setStyleSheet(
            "color: #8e8e93; font-size: 12px; background-color: transparent;"
        )

        text_layout.addWidget(title_label)
        text_layout.addWidget(info_label)
        text_layout.addStretch()
        return text_layout


class AddWindow(QWidget):
    """Ventana de busqueda de anime y guardado del resultado"""

    def __init__(self, on_back_callback):
        super().__init__()
        self.on_back_callback = on_back_callback
        self.setStyleSheet(ADD_WINDOW_STYLE)

        self.selected_title = ""
        self.selected_type = ""
        self.selected_image = ""
        self.selected_score = 0
        self.selected_year = 0

        self.build_ui()

    # -- Construccion del UI --
    def build_ui(self):

        # -- Layout --
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        layout.addWidget(self.build_back_button())
        layout.addLayout(self.build_search_bar())

        self.results_list = QListWidget()
        self.results_list.itemClicked.connect(self.on_item_selected)
        layout.addWidget(self.results_list)

        layout.addLayout(self.build_bottom_buttons())
        self.setLayout(layout)

    def build_back_button(self):
        self.back_button = QPushButton()
        self.back_button.setObjectName("BackBtn")
        self.back_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.back_button.setIcon(QIcon("icons/chevron-left.svg"))
        self.back_button.setIconSize(ICON_SIZE)
        self.back_button.setFixedSize(NAV_BTN_SIZE, NAV_BTN_SIZE)
        self.back_button.clicked.connect(self.on_back_callback)
        return self.back_button

    def build_search_bar(self):
        search_layout = QHBoxLayout()
        search_layout.setSpacing(8)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nombre del anime...")

        self.search_button = QPushButton()
        self.search_button.setObjectName("SearchBtn")
        self.search_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.search_button.setIcon(QIcon("icons/search.svg"))
        self.search_button.setIconSize(ICON_SIZE)
        self.search_button.setFixedSize(NAV_BTN_SIZE, NAV_BTN_SIZE)
        self.search_button.clicked.connect(self.search_anime)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        return search_layout

    def build_bottom_buttons(self):
        self.save_button = QPushButton()
        self.save_button.setObjectName("SaveBtn")
        self.save_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.save_button.setIcon(QIcon("icons/device-floppy.svg"))
        self.save_button.setIconSize(ICON_SIZE)
        self.save_button.setFixedSize(NAV_BTN_SIZE, NAV_BTN_SIZE)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_and_close)

        buttons_layout = QHBoxLayout()
        buttons_layout.addStretch(1)
        buttons_layout.addWidget(self.save_button)
        return buttons_layout

    def save_and_close(self):
        self.on_back_callback()

    def search_anime(self):
        query = self.search_input.text().strip()
        if not query:
            return

        self.results_list.clear()
        self.save_button.setEnabled(False)

        data = search_anime_api(query)
        if data is None:
            self.results_list.addItem("Error al conectar con el servidor o en la red")
            return

        for anime in data:
            self.add_result_item(anime)

    def add_result_item(self, anime):
        title = anime.get("title")
        anime_type = anime.get("type", "TV")
        anime_year = anime.get("year") or 0

        api_score = anime.get("score")
        score = int(api_score) if api_score and not isinstance(api_score, dict) else 0

        image_url = anime.get("images", {}).get("jpg", {}).get("image_url", "")

        item = QListWidgetItem(self.results_list)
        item.setSizeHint(QSize(0, CARD_ITEM_HEIGHT))
        item.setData(
            Qt.ItemDataRole.UserRole,
            {
                "title": title,
                "type": anime_type,
                "image": image_url,
                "score": score,
                "year": anime_year,
            },
        )

        card_widget = ResultCard(title, anime_type, score, image_url, anime_year)
        self.results_list.addItem(item)
        self.results_list.setItemWidget(item, card_widget)

    def on_item_selected(self, item):
        data = item.data(Qt.ItemDataRole.UserRole)
        if not data:
            return

        self.selected_title = data["title"]
        self.selected_type = data["type"]
        self.selected_image = data["image"]
        self.selected_year = int(data.get("year", 0) or 0)

        raw_score = data.get("score", 0)
        if isinstance(raw_score, dict):
            self.selected_score = int(raw_score.get("value", 0) or 0)
        else:
            self.selected_score = int(raw_score or 0)

        self.save_button.setEnabled(True)
