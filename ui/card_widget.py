import requests
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget


def create_card(media_id, title, media_type, year, score, image_path, click_callback):
    card = QWidget()
    card.setCursor(Qt.PointingHandCursor)
    card.setFixedWidth(150)

    layout = QVBoxLayout()
    layout.setContentsMargins(5, 5, 5, 5)
    layout.setSpacing(6)

    image_label = QLabel()
    image_label.setFixedSize(140, 200)
    image_label.setAlignment(Qt.AlignCenter)

    pixmap = QPixmap()

    if image_path.startswith("https://") or image_path.startswith("htpps://"):
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
            }
            img_data = requests.get(image_path, headers=headers).content
            pixmap.loadFromData(img_data)
        except Exception as e:
            print(f"Error descargando imagen: {e}")
            pixmap.load("images/default.png")
    else:
        pixmap.load(image_path)

    if pixmap.isNull():
        pixmap.load("images/default.png")

    image_label.setPixmap(
        pixmap.scaled(140, 200, Qt.KeepAspectRatio, Qt.SmoothTransformation)
    )

    short_title = title if len(title) < 20 else title[:17] + "..."
    display_year = f"({year})" if year and year != 0 else ""

    text = QLabel(
        f"<div style='line-height: 120%;'>"
        f"  <b style='color: #ffffff; font-size: 12px;'>{short_title}</b><br>"
        f"  <span style='color: #8a8a8f; font-size: 11px;'>{media_type}</span><br>"
        f"  <span style='color: #8a8a8f; font-size: 11px;'>{display_year}</span><br>"
        f"  <span style='color: #ffcc00; font-size: 11px;'>⭐ {score}/10</span>"
        f"</div>"
    )
    text.setAlignment(Qt.AlignCenter)
    text.setWordWrap(True)
    text.setFixedWidth(140)

    card.setObjectName("AnimeCard")
    layout.addWidget(image_label)
    layout.addWidget(text)
    card.setLayout(layout)
    card.setStyleSheet("""
            QWidget#AnimeCard {
                background-color: #21222c;
                border-radius: 10px;
                border: 1px solid #2c2c2e;
            }
            QWidget#AnimeCard:hover {
                background-color: #313244;
                border: 1px solid #585b70;
            }
            QLabel {
                background-color: transparent;
                border: none;
            }
        """)

    card.mousePressEvent = lambda event, m=media_id, t=title: click_callback(m, t)

    return card
