from jikanpy import Jikan
from jikanpy.exceptions import APIException

# -- Constantes --
SEARCH_LIMIT = 5

# -- API --
jikan = Jikan()


def search_anime_api(query: str) -> list | None:

    try:
        response = jikan.search("anime", query, parameters={"limit": SEARCH_LIMIT})
        return response.get("data", [])

    except APIException as e:
        print(f"Error de red en el modelo: {e}")
        return None

    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
