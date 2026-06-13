import requests
from PySide6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PySide6.QtGui import QPixmap
from PySide6.QtCore import Qt

def create_card(media_id, title, media_type, score, image_path, click_callback):
    card = QWidget()
    card.setCursor(Qt.PointingHandCursor)

    layout = QVBoxLayout()
    layout.setContentsMargins(5, 5, 5, 5)

    image_label = QLabel()
    image_label.setFixedSize(140, 200)
    image_label.setAlignment(Qt.AlignCenter)

    pixmap = QPixmap()

    if image_path.startswith("https://") or image_path.startswith("htpps://"):
        try:
            headers = {"User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"}
            img_data = requests.get(image_path, headers=headers).content
            pixmap.loadFromData(img_data)
        except Exception as e:
            print(f"Error descargando imagen: {e}")
            pixmap.load("images/default.png")
    else:
        pixmap.load(image_path)

    if pixmap.isNull():
        pixmap.load("images/default.png")

    image_label.setPixmap(pixmap.scaled(140, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation))

    short_title = title if len(title) < 20 else title[:17] + "..."
    text = QLabel(f"{title}\n{media_type}\n⭐{score}")
    text.setAlignment(Qt.AlignCenter)
    text.setWordWrap(True)

    layout.addWidget(image_label)
    layout.addWidget(text)
    card.setLayout(layout)
    card.setStyleSheet("QWidget {background-color: #2b2b2b; border-radius: 8px; } QLabel { background-color: transparent; }")

    card.mousePressEvent = lambda event, m=media_id, t=title: click_callback(m, t)

    return card
