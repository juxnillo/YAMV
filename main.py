from requests.models import Response

from database.db import create_table, get_media, add_media
import requests

from PySide6.QtWidgets import (
    QApplication,
    QListWidget,
    QListWidgetItem,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QScrollArea,
    QDialog,
    QLineEdit,
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class AddWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Buscar en MyAnimeList")
        self.resize(400,500)

        layout = QVBoxLayout()

        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Nombre del anime...")
        self.search_button = QPushButton()
        self.search_button.clicked.connect(self.search_anime)

        search_layout.addWidget(self.search_input)
        search_layout.addWidget(self.search_button)
        layout.addLayout(search_layout)

        self.results_list = QListWidget()
        layout.addWidget(self.results_list)

        self.save_button = QPushButton("Añadir a coleccion")
        self.save_button.setEnabled(False)
        self.save_button.clicked.connect(self.accept)
        layout.addWidget(self.save_button)

        self.setLayout(layout)

        self.selected_title = ""
        self.selected_type = "Anime"
        self.selected_image = ""
        self.selected_score = 0

        self.results_list.itemClicked.connect(self.on_item_selected)

    def search_anime(self):
        query = self.search_input.text().strip()
        if not query:
            return

        self.results_list.clear()
        self.save_button.setEnabled(False)

        url = f"https://api.jikan.moe/v4/anime?q={query}&limit=5"

        try:
            response = requests.get(url)
            if response.status_code == 200:
                data = response.json().get("data", [])

                for anime in data:
                    title = anime.get("title")
                    anime_type = anime.get("type", "TV")
                    api_score = anime.get("score")
                    score = int(api_score) if api_score and not isinstance(api_score, dict) else 0
                    image_url = anime.get("images", {}.get("jpg", {}.get("image_url", "")))

                    item = QListWidgetItem(f"{title} ({anime_type}) - ⭐{score}")
                    item.setData(Qt.UserRole, {"title": title, "type": anime_type, "image": image_url, "score": score})
                    self.results_list.addItem(item)
            else:
                self.results_list.addItem("Error al conectar con el servidor")
        except Exception as e:
            self.results_list.addItem(f"Error de red: {e}")

    def on_item_selected(self, item):
        data = item.data(Qt.UserRole)
        self.selected_title = data["title"]
        self.selected_type = data["type"]
        self.selected_image = data["image"]

        raw_score = data.get("score", 0)
        if isinstance(raw_score, dict):
            self.selected_score = int(raw_score.get("value", 0) or 0)
        else:
            self.selected_score = int(raw_score or 0)

        self.save_button.setEnabled(True)

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

        cards.addWidget(create_card(title, media_type, score, image))

def create_card(title, media_type, score, image_path):
    card = QWidget()

    layout = QHBoxLayout()
    image_label = QLabel()
    image_label.setFixedSize(120, 180)
    pixmap = QPixmap()

    if image_path.startswith("https://") or image_path.startswith("htpps://"):
        try:
            img_data = requests.get(image_path).content
            pixmap.loadFromData(img_data)
        except:
            pixmap.load("images/default.png")
    else:
        pixmap.load(image_path)
    if pixmap.isNull():
        pixmap.load("images/default.png")

    image_label.setPixmap(pixmap.scaled(120, 180, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    text = QLabel(f"{title}\n{media_type}\n⭐{score}")

    layout.addWidget(image_label)
    layout.addWidget(text)

    card.setLayout(layout)

    return card

create_table()

app = QApplication([])

window = QWidget()
window.setWindowTitle("YAMV")

layout = QVBoxLayout()
scroll = QScrollArea()
content = QWidget()
cards = QVBoxLayout()

content.setLayout(cards)
scroll.setWidget(content)
scroll.setWidgetResizable(True)

button = QPushButton("Buscar y Añadir")
button.clicked.connect(open_form)

layout.addWidget(button)
layout.addWidget(scroll)

window.setLayout(layout)

for row in get_media():
    # 1 Titulo - 2 Tipo - 3 genero - 4 Año - 5 Portada - 6 Rating
    cards.addWidget(create_card(row[1], row[2], row[6], row[5]))


window.show()

app.exec()
