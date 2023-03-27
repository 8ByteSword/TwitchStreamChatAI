from dotenv import load_dotenv
from twitchio.ext import commands
import asyncio, os
import requests

from utils.audit_decorators import AuditBase

class TwitchChat(commands.Bot, AuditBase):

    def __init__(self, twitch_credentials, canal):
        super().__init__(
            token=twitch_credentials['token'],
            client_id=twitch_credentials['client_id'],
            client_secret=twitch_credentials['client_secret'],
            nick='8bytesword',
            prefix='!',
            initial_channels= ["8bytesword"]
        )
        self.chat_history = []
        self.canal = canal
        self.message_queue = asyncio.Queue()

    async def event_message(self, message):
        print(f"Message event {message}")
        await self.message_queue.put(message)

    async def get_message(self):
        while True:
            print("get_message")
            message = await self.message_queue.get()
            if message:
                yield message

    async def listen(self):
        print("listen")
        async for message in self.get_message():
            yield message

    async def event_ready(self):
        print(f'{self.nick} está conectado a Twitch!')

    def get_chat_history(self):
        return ' '.join(self.chat_history)

    async def send_message(self, message):
        await self.get_channel(self.canal).send(message)

async def escuchar_chat(bot):
        async for mensaje in bot.listen():
            print(mensaje)

if __name__ == "__main__":
    load_dotenv()
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
    token, client_id, client_secret = get_twitch_token()
    twitch_credentials = {'token': token, 'client_id': client_id, 'client_secret': client_secret}
    bot = TwitchChat(twitch_credentials, "chusommontero")
    asyncio.get_event_loop().run_until_complete(escuchar_chat(bot))