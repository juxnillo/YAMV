from jikanpy import Jikan
from jikanpy.exceptions import APIException, BadResponseException

def search_anime_api(query):

    jikan = Jikan()

    try:
        response = jikan.search('anime', query, parameters={'limit': 5})
        return response.get('data', [])
    except BadResponseException as e:
        print(f"La API de Jikan funciona, pero MAL no responde: {e}")
        return None
    except APIException as e:
        print(f"Error de red en el modelo: {e}")
        return None
    except Exception as e:
        print(f"Error inesperado: {e}")
        return None
