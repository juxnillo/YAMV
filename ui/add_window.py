from PySide6.QtWidgets import QDialog, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QListWidget, QListWidgetItem
from PySide6.QtCore import Qt
from models.anime_model import search_anime_api

class AddWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Buscar en MyAnimeList")
        self.resize(400, 500)

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

                item = QListWidgetItem(f"{title} ({anime_type}) - ⭐{score}")
                item.setData(Qt.UserRole, {"title": title, "type": anime_type, "image": image_url, "score": score})
                self.results_list.addItem(item)
        else:
            self.results_list.addItem("Error al conectar con el servidor o en la red")

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
