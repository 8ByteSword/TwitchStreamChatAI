import requests
import os
from dotenv import load_dotenv


def get_twitch_token(client_id=None, client_secret=None):
    load_dotenv()
    url = "https://id.twitch.tv/oauth2/token"
    client_id = os.environ("TWITCH_CLIENT_ID")
    client_secret = os.environ("TWITCH_CLIENT_SECRET")
    payload = {
        "client_id": client_id,
        "client_secret": client_secret,
        "grant_type": "client_credentials",
    }
    response = requests.post(url, params=payload)
    if response.status_code == 200:
        data = response.json()
        return data["access_token"], client_id, client_secret
    else:
        print("Error obteniendo el token de acceso:", response.status_code)
        return None