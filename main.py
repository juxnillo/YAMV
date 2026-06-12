from database.db import create_table, get_media, add_media

from PySide6.QtWidgets import (
    QApplication,
    QWidget,
    QVBoxLayout,
    QPushButton,
    QLabel,
    QHBoxLayout,
    QScrollArea,
    QDialog,
    QLineEdit,
    QComboBox,
    QSpinBox,
    QFileDialog
)
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt


class AddWindow(QDialog):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Añadir")

        layout = QVBoxLayout()

        self.title = QLineEdit()
        self.title.setPlaceholderText("Título")

        self.type = QComboBox()
        self.type.addItems([
            "Anime",
            "Serie",
            "Pelicula"
        ])

        self.score = QSpinBox()
        self.score.setRange(0, 10)

        self.image_path = ""

        image_button = QPushButton("Seleccionar Portada")
        image_button.clicked.connect(self.select_image)

        self.image_label = QLabel("Sin Imagen")

        save = QPushButton("Guardar")

        save.clicked.connect(self.accept)

        layout.addWidget(self.title)
        layout.addWidget(self.type)
        layout.addWidget(self.score)
        layout.addWidget(image_button)
        layout.addWidget(self.image_label)
        layout.addWidget(save)
        self.setLayout(layout)

    def select_image(self):

        file, _ = QFileDialog.getOpenFileName(self, "Seleccionar Portada", "", "Imagenes(*.png .jpg .jpeg")
        if file:
            self.image_path = file
            self.image_label.setText(file.split("/")[-1])


def open_form():
    dialog = AddWindow()

    if dialog.exec():
        title = dialog.title.text()
        media_type = dialog.type.currentText()
        score = dialog.score.value()
        image = dialog.image_path

        add_media(
            title,
            media_type,
            "",
            2025,
            image,
            score
        )

        cards.addWidget(create_card(title, media_type, score, image))

def create_card(title, media_type, score, image_path):
    card = QWidget()

    layout = QHBoxLayout()

    image = QLabel()
    image.setFixedSize(120, 180)

    pixmap = QPixmap(image_path)
    if pixmap.isNull():
        pixmap = QPixmap("images/default.png")

    image.setPixmap(pixmap.scaled(120, 180))

    text = QLabel(f"{title}\n{media_type}\n⭐{score}")

    layout.addWidget(image)
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

button = QPushButton("Añadir")

button.clicked.connect(open_form)

layout.addWidget(button)
layout.addWidget(scroll)

window.setLayout(layout)

for row in get_media():
    # 1 Titulo - 2 Tipo - 3 genero - 4 Año - 5 Portada - 6 Rating
    cards.addWidget(create_card(row[1], row[2], row[6], row[5]))


window.show()

app.exec()
