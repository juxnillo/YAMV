import requests

def search_anime_api(query):
    """Hace la petición a la API de Jikan y devuelve los datos o None si falla"""
    url = f"https://api.jikan.moe/v4/anime?q={query}&limit=5"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return response.json().get("data", [])
        return None
    except Exception as e:
        print(f"Error de red en el modelo: {e}")
        return None
