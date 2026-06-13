import requests
from PySide6.QtGui import QPixmap, QIcon
from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem, QWidget, QLabel
from PySide6.QtCore import Qt, QSize
from models.anime_model import search_anime_api
from ui import card_widget

class ResultCard(QWidget):
    def __init__(self, title, anime_type, score, image_url):
        super().__init__()

        layout = QHBoxLayout()
        layout.setContentsMargins(10, 10, 10, 10)
        layout.setSpacing(15)

        self.img_label = QLabel()
        self.img_label.setFixedSize(60, 85)
        self.img_label.setStyleSheet("border-radius: 4px; background-color: #2c2c2e;")
        self.img_label.setAlignment(Qt.AlignCenter)

        pixmap = QPixmap()
        try:
            headers = {"User-Agent": "Mozilla/5.0"}
            img_data = requests.get(image_url, headers=headers, timeout=5).content
            pixmap.loadFromData(img_data)
            self.img_label.setPixmap(pixmap.scaled(60, 85, Qt.KeepAspectRatioByExpanding, Qt.SmoothTransformation))
        except:
            self.img_label.setText("No Img")

        text_layout = QVBoxLayout()
        self.title_label = QLabel(f"<b>{title}</b>")
        self.title_label.setStyleSheet("color: white; font-size: 14px;")
        self.title_label.setWordWrap(True)

        self.info_label = QLabel(f"{anime_type}  ·  ⭐ {score}/10")
        self.info_label.setStyleSheet("color: #8e8e93; font-size: 12px;")

        text_layout.addWidget(self.title_label)
        text_layout.addWidget(self.info_label)
        text_layout.addStretch()

        layout.addWidget(self.img_label)
        layout.addLayout(text_layout)
        self.setLayout(layout)

class AddWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Buscar en MyAnimeList")
        self.resize(500, 600)

        self.setStyleSheet("""
                    QDialog {
                        background-color: #1c1c1e;
                        font-family: 'Segoe UI', Helvetica, Arial, sans-serif;
                    }

                    QLineEdit {
                        background-color: #2c2c2e;
                        color: white;
                        border: 1px solid #3a3a3c;
                        border-radius: 6px;
                        padding: 8px 12px;
                        font-size: 13px;
                    }
                    QLineEdit:focus {
                        border: 1px solid #0a84ff;
                    }

                    QPushButton {
                        background-color: #3a3a3c;
                        color: white;
                        font-weight: bold;
                        padding: 8px 16px;
                        border-radius: 6px;
                        border: none;
                        font-size: 13px;
                    }
                    QPushButton:hover {
                        background-color: #48484a;
                    }
                    QPushButton:pressed {
                        background-color: #2c2c2e;
                    }

                    QPushButton:disabled {
                        background-color: #2c2c2e;
                        color: #545456;
                    }

                    QPushButton[text="Añadir a coleccion"] {
                        background-color: #30d158;
                        color: white;
                    }
                    QPushButton[text="Añadir a coleccion"]:hover {
                        background-color: #34c759;
                    }

                    # Lista de Resultados #
                    QListWidget {
                        background-color: #242426;
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
                        background-color: #2c2c2e;
                        color: white;
                    }
                    QListWidget::item:selected {
                        background-color: #0a84ff;
                        color: white;
                        font-weight: bold;
                    }
                """)

        layout = QVBoxLayout()
        layout.setContentsMargins(20, 20, 20, 20)
        layout.setSpacing(12)

        search_layout = QHBoxLayout()
        search_layout.setSpacing(8)

        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nombre del anime...")

        # Boton Buscar
        self.search_button = QPushButton("Buscar")
        self.search_button.setCursor(Qt.PointingHandCursor)
        self.search_button.clicked.connect(self.search_anime)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        # Boton Guardar
        self.save_button = QPushButton("Añadir a coleccion")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.selected_title = ""
        self.selected_type = ""
        self.selected_image = ""
        self.selected_score = 0

        self.results_list.itemClicked.connect(self.on_item_selected)

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
                score = int(api_score) if api_score and not isinstance(api_score, dict) else 0
                images_dict = anime.get("images", {})
                jpg_dict = images_dict.get("jpg", {})
                image_url = jpg_dict.get("image_url", "")

                item = QListWidgetItem(self.results_list)
                card_widget = ResultCard(title, anime_type, score, image_url)
                item.setSizeHint(QSize(0, 105))
                item.setData(Qt.UserRole, {"title": title, "type": anime_type, "image": image_url, "score": score})
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

        raw_score = data.get("score", 0)
        if isinstance(raw_score, dict):
            self.selected_score = int(raw_score.get("value", 0) or 0)
        else:
            self.selected_score = int(raw_score or 0)

        self.save_button.setEnabled(True)
