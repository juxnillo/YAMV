import requests
from PySide6.QtCore import QSize, Qt
from PySide6.QtGui import QIcon, QPixmap
from PySide6.QtWidgets import (
    QDialog,
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
from ui import card_widget

class ResultCard(QWidget):
    def __init__(self, title, anime_type, score, image_url, year):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        self.img_label = QLabel()
        self.img_label.setFixedSize(60, 85)
        self.img_label.setStyleSheet("border-radius: 4px; background-color: #2c2c2e;")
        self.img_label.setAlignment(Qt.AlignCenter)

        pixmap = QPixmap()
        if image_url.startswith("http"):
                    try:
                        headers = {"User-Agent": "Mozilla/5.0"}
                        img_data = requests.get(image_url, headers=headers, timeout=3).content
                        pixmap.loadFromData(img_data)
                        self.img_label.setPixmap(
                            pixmap.scaled(
                                60, 85, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation
                            )
                        )
                    except Exception:
                        self.img_label.setText("No Img")
        else:
            self.img_label.setText("🍿")

        text_layout = QVBoxLayout()
        self.title_label = QLabel(f"<b>{title}</b>")
        self.title_label.setStyleSheet("color: white; font-size: 14px;")
        self.title_label.setWordWrap(True)
        display_year = f"({year})" if year and year != 0 else ""

        self.info_label = QLabel(f"{anime_type} {display_year} ·  ⭐ {score}/10")
        self.info_label.setStyleSheet("color: #8e8e93; font-size: 12px;")

        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.info_label)
        text_layout.addStretch()

        layout.addWidget(self.img_label)
        layout.addLayout(text_layout)
        self.setLayout(layout)

class AddWindow(QWidget):
    def __init__(self, on_back_callback):
        super().__init__()
        self.on_back_callback = on_back_callback
        self.setStyleSheet("""
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
                        background-color: #5500bb;
                        border-radius: 16px;
                        padding: 0px;
                    }

                    QPushButton#BackBtn:hover {
                         background-color: #313244;
                    }
                    QPushButton#BackBtn:pressed {
                         background-color: #5500bb;
                    }

                    QPushButton#SearchBtn {
                        background-color: #5500bb;
                        border-radius: 11px;
                    }

                    QPushButton#SearchBtn:hover {
                         background-color: #313244;
                    }
                    QPushButton#SearchBtn:pressed {
                         background-color: #5500bb;
                    }

                    QPushButton#SaveBtn {
                        background-color: #5500bb;
                        border-radius: 16px;
                        color: white;
                    }
                    QPushButton#SaveBtn:hover {
                        background-color: #313244;
                    }

                    QListWidget {
                        background-color: #1e1e2e;
                        color: #e5e5ea;
                        border: 1px solid #2c2c2e;
                        border-radius: 8px;
                        padding: 5px;
                        font-size: 13px;
                    }
                    QListWidget::item {
                        padding: 10px;
                        border-bottom: 1px solid #2c2c2e;
                        border-radius: 4px;
                    }
                    QListWidget::item:hover {
                        background-color: #32324c;
                        color: white;
                    }
                    QListWidget::item:selected {
                        background-color: #32324c;
                        color: white;
                        font-weight: bold;
                    }
                """)

        # -- Layout --
        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        # -- BackBtn --
        icon_back = QIcon("icons/chevron-left.svg")
        self.back_button = QPushButton()
        self.back_button.setObjectName("BackBtn")
        self.back_button.setCursor(Qt.PointingHandCursor)
        self.back_button.setIcon(icon_back)
        self.back_button.setIconSize(QSize(20, 20))

        self.back_button.setFixedSize(40, 40)
        self.back_button.clicked.connect(self.on_back_callback)
        layout.addWidget(self.back_button)

        # -- SearchBar --
        search_layout = QHBoxLayout()
        search_layout.setSpacing(8)
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nombre del anime...")

        # -- SearchBtn --
        icon_search = QIcon("icons/search.svg")
        self.search_button = QPushButton()
        self.search_button.setObjectName("SearchBtn")
        self.search_button.setCursor(Qt.PointingHandCursor)
        self.search_button.setIcon(icon_search)
        self.search_button.setIconSize(QSize(20, 20))
        self.search_button.setFixedSize(40, 40)
        self.search_button.clicked.connect(self.search_anime)
        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        # -- SearchResults --
        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        # -- SaveBtn --
        icon_save = QIcon("icons/device-floppy.svg")
        self.save_button = QPushButton()
        self.save_button.setObjectName("SaveBtn")
        self.save_button.setCursor(Qt.PointingHandCursor)
        self.save_button.setIcon(icon_save)
        self.save_button.setIconSize(QSize(20, 20))
        self.save_button.setFixedSize(40, 40)
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.save_and_close)

        # -- LayoutBtn --
        buttons_layout = QHBoxLayout()
        buttons_layout.addWidget(self.back_button)   # Se queda a la izquierda
        buttons_layout.addStretch(1)                  # Hace de muelle en medio
        buttons_layout.addWidget(self.save_button)

        layout.addLayout(buttons_layout)

        self.setLayout(layout)

        self.selected_title = ""
        self.selected_type = ""
        self.selected_image = ""
        self.selected_score = 0
        self.selected_year = 0

        self.results_list.itemClicked.connect(self.on_item_selected)

    def save_and_close(self):
        self.on_back_callback()

    def search_anime(self):
        query = self.search_input.text().strip()
        if not query:
            return

        self.results_list.clear()
        self.save_button.setEnabled(False)

        data = search_anime_api(query)

        if data is not None:
            for anime in data:
                title = anime.get("title")
                anime_type = anime.get("type", "TV")
                api_score = anime.get("score")
                anime_year = anime.get("year") or 0
                score = (
                    int(api_score)
                    if api_score and not isinstance(api_score, dict)
                    else 0
                )
                images_dict = anime.get("images", {})
                jpg_dict = images_dict.get("jpg", {})
                image_url = jpg_dict.get("image_url", "")

                item = QListWidgetItem(self.results_list)
                card_widget = ResultCard(
                    title, anime_type, score, image_url, anime_year
                )
                item.setSizeHint(QSize(0, 105))
                item.setData(
                    Qt.UserRole,
                    {
                        "title": title,
                        "type": anime_type,
                        "image": image_url,
                        "score": score,
                        "year": anime_year,
                    },
                )
                self.results_list.addItem(item)
                self.results_list.setItemWidget(item, card_widget)
        else:
            self.results_list.addItem("Error al conectar con el servidor o en la red")

    def on_item_selected(self, item):
        data = item.data(Qt.UserRole)
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
