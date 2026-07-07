import requests
from PySide6.QtCore import Qt
from PySide6.QtGui import QPixmap
from PySide6.QtWidgets import QLabel, QVBoxLayout, QWidget

# -- Constantes --
CARD_WIDTH = 150
CARD_IMG_SIZE = (134, 190)
TEXT_WIDTH = 140
TITLE_MAX_LEN = 28
DEFAULT_IMAGE_PATH = "images/default.png"

USER_AGENT = (
    "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 "
    "(KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)
CARD_STYLE = """
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
    """

# -- Cache de pixmaps --
CACHE_IMAGENES = {}


# -- Helper imagen --
def download_pixmap(image_url, title):
    """Descarga la imagen y la devuelve a pixmap"""

    try:
        headers = {"User-Agent": USER_AGENT}
        img_data = requests.get(image_url, headers=headers, timeout=3).content
    except Exception as e:
        print(f"Error descargando imagen para {title}: {e}")
        return None

    pixmap = QPixmap()
    pixmap.loadFromData(img_data)
    return pixmap if not pixmap.isNull() else None


def load_pixmap(image_path, title):
    """Resuelve la imagen de la tarjeta"""

    is_remote = image_path.startswith("https://") or image_path.startswith("http://")

    if is_remote:
        if image_path in CACHE_IMAGENES:
            return CACHE_IMAGENES[image_path]

        pixmap = download_pixmap(image_path, title)
        if pixmap is not None:
            CACHE_IMAGENES[image_path] = pixmap
            return pixmap
    else:
        pixmap = QPixmap()
        pixmap.load(image_path)
        if not pixmap.isNull():
            return pixmap

    fallback = QPixmap()
    fallback.load(DEFAULT_IMAGE_PATH)
    return fallback


# -- Construccion de la tarjeta --
def build_image_label(image_path, title):
    label = QLabel()
    label.setFixedSize(*CARD_IMG_SIZE)
    label.setAlignment(Qt.AlignmentFlag.AlignCenter)
    label.setStyleSheet("border-radius: 6px; background-color: #11111b;")

    pixmap = load_pixmap(image_path, title)
    label.setPixmap(
        pixmap.scaled(
            *CARD_IMG_SIZE,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation,
        )
    )
    return label


def build_text_label(title, media_type, year, score):
    short_title = (
        title if len(title) < TITLE_MAX_LEN else title[: TITLE_MAX_LEN - 3] + "..."
    )
    display_year = f"({year})" if year else ""

    text = QLabel(
        f"<div style='line-height: 120%;'>"
        f"  <b style='color: #ffffff; font-size: 12px;'>{short_title}</b><br>"
        f"  <span style='color: #8a8a8f; font-size: 11px;'>{media_type}</span><br>"
        f"  <span style='color: #8a8a8f; font-size: 11px;'>{display_year}</span><br>"
        f"  <span style='color: #ffcc00; font-size: 11px;'>⭐ {score}/10</span>"
        f"</div>"
    )
    text.setAlignment(Qt.AlignmentFlag.AlignCenter)
    text.setWordWrap(True)
    text.setFixedWidth(TEXT_WIDTH)
    return text


def create_card(media_id, title, media_type, year, score, image_path, click_callback):
    card = QWidget()
    card.setObjectName("AnimeCard")
    card.setCursor(Qt.CursorShape.PointingHandCursor)
    card.setFixedWidth(CARD_WIDTH)
    card.setStyleSheet(CARD_STYLE)

    layout = QVBoxLayout()
    layout.setContentsMargins(8, 8, 8, 8)
    layout.setSpacing(6)
    layout.addWidget(build_image_label(image_path, title))
    layout.addWidget(build_text_label(title, media_type, year, score))
    card.setLayout(layout)

    card.mousePressEvent = lambda event, m=media_id, t=title: click_callback(m, t)
    return card
