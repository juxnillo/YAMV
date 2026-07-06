from jikanpy import Jikan
from jikanpy.exceptions import APIException

def search_anime_api(query):

    jikan = Jikan()

    try:
        response = jikan.search('anime', query, parameters={'limit': 5})
        return response.get('data', [])

    except APIException as e:
        print(f"Error de red en el modelo: {e}")
        return None

    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
