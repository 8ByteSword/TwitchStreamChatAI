import os
import requests
from dotenv import load_dotenv

def get_twitch_token(client_id=None, client_secret=None):
    load_dotenv()
    url = "https://id.twitch.tv/oauth2/token"
    client_id = os.environ["TWITCH_CLIENT_ID"]
    client_secret = os.environ["TWITCH_CLIENT_SECRET"]
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

def test_twitch_credentials(client_id, token, username):
    url = "https://api.twitch.tv/helix/users"

    headers = {
        "Client-ID": client_id,
        "Authorization": f"Bearer {token}"
    }

    params = {
        "login": username
    }

    response = requests.get(url, headers=headers, params=params)

    if response.status_code == 200:
        print("Las credenciales son correctas.")
        data = response.json()
        print("Información del usuario:", data)
    else:
        print("Error en las credenciales:", response.status_code)
        print("Detalles del error:", response.json())

if __name__ == "__main__":
    load_dotenv()
    client_id = os.environ["TWITCH_CLIENT_ID"]
    token, client_id, client_secret = get_twitch_token()
    print(token)
    test_twitch_credentials(client_id, token, "chusommontero")
