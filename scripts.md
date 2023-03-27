## bot_twitch.py

```python
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import asyncio
from src.audio.audio_processor import AudioProcessor
from src.audio.twitch_audio import TwitchAudio
from src.chat.chat_with_gpt import ChatWithGPT
from src.chat.twitch_chat import TwitchChat
from src.utils.utils import get_twitch_token
from summarizer import extract_keywords, generate_summary

from dotenv import load_dotenv

class TwitchBot:
    def __init__(self, twitch_credentials, chatgpt_credentials, google_credentials_file, chromedriver_path, nombre_del_streamer):
        self.twitch_chat = TwitchChat(twitch_credentials, nombre_del_streamer)
        
        self.twitch_audio = TwitchAudio(nombre_del_streamer, chromedriver_path)
        self.chatgpt = ChatWithGPT(chatgpt_credentials)

    async def escuchar_chat(self):
        async for mensaje in self.twitch_chat.listen():
            if self.chatgpt.is_command(mensaje):
                await self.chatgpt.handle_command(self.twitch_chat, mensaje)

    async def resumir_chat(self):
        chat_history = self.twitch_chat.get_chat_history()
        keywords = extract_keywords(chat_history)
        summary = await self.chatgpt.generate_summary(keywords)
        await self.twitch_chat.send_message(summary)

    async def escuchar_audio(self):
        async for audio_data in self.audio_processor.listen():
            transcript = await self.audio_processor.process_audio(audio_data)
            if self.chatgpt.is_direct_question(transcript):
                answer = await self.chatgpt.answer_question(self.twitch_chat, transcript)
                await self.twitch_chat.send_message(answer)

async def main():
    load_dotenv()
    token, client_id, client_secret = get_twitch_token()
    twitch_credentials = {'token': token, 'client_id': client_id, 'client_secret': client_secret}
    chatgpt_credentials = {'api_key': os.environ["CHATGPT_API_KEY"]}
    google_credentials_file = 'path/to/your/google_credentials.json'
    chromedriver_path = 'chromedriver'
    nombre_del_streamer = os.environ["TWITCH_STREAMER_NAME"]

    bot = TwitchBot(twitch_credentials, chatgpt_credentials, google_credentials_file, chromedriver_path, nombre_del_streamer)

    async def escuchar_chat_wrapper():
        try:
            await bot.escuchar_chat()
        except Exception as e:
            print(f"Error en escuchar_chat: {e}")

    async def escuchar_audio_wrapper():
        try:
            await bot.escuchar_audio()
        except Exception as e:
            print(f"Error en escuchar_audio: {e}")

    
    await asyncio.gather(
        escuchar_chat_wrapper(),
        
    )

if __name__ == '__main__':
    asyncio.run(main())
```

## new_features.py

```python
class NewFeatures:
    def __init__(self, twitch_bot):
        self.twitch_bot = twitch_bot

    def chistes_contextualizados(self):
        
        pass
    def trivia_interactiva(self):
        
        pass
    def comentarios_eventos_tiempo_real(self):
        
        pass
    def preguntas_respuestas(self):
        
        pass
    def encuestas_votaciones(self):
        
        pass
    def integracion_otros_servicios(self):
        
        pass
    def asistente_moderacion(self):
        
        pass
    def aprendizaje_adaptativo_personalizacion(self):
        
        pass
    def integracion_juegos_aplicaciones(self):
        
        pass
    def retransmision_mensajes_destacados(self):
        
        pass
```

## __init__.py

```python

```

## twitch_audio.py

```python
import time
from pyvirtualdisplay import Display
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

class TwitchAudio:
    def __init__(self, streamer, chromedriver_path):
        self.streamer = streamer
        self.chromedriver_path = chromedriver_path
        self.browser = None

    def start(self):
        display = Display(visible=0, size=(800, 600))
        display.start()

        chrome_options = Options()
        chrome_options.add_argument("--use-fake-ui-for-media-stream")

        self.browser = webdriver.Chrome(executable_path=self.chromedriver_path, options=chrome_options)
        self.browser.get(f'https://www.twitch.tv/{self.streamer}')

        
        time.sleep(10)
```

## audio_processor.py

```python
from pydub import AudioSegment
from google.cloud import speech_v1p1beta1 as speech

class AudioProcessor:
    def __init__(self, google_credentials_file):
        self.client = speech.SpeechClient.from_service_account_json(google_credentials_file)

    def process_audio(self, audio_file_path):
        audio_data = self._read_audio_file(audio_file_path)
        transcript = self._convert_speech_to_text(audio_data)
        return transcript

    def _read_audio_file(self, audio_file_path):
        audio = AudioSegment.from_file(audio_file_path, format="mp3")
        audio = audio.set_frame_rate(16000).set_channels(1)
        return audio.raw_data

    def _convert_speech_to_text(self, audio_data):
        config = speech.RecognitionConfig(
            encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
            sample_rate_hertz=16000,
            language_code="en-US",
            enable_automatic_punctuation=True,
        )

        response = self.client.recognize(config=config, audio=speech.RecognitionAudio(content=audio_data))
        transcript = ""
        for result in response.results:
            transcript += result.alternatives[0].transcript

        return transcript
```

## __init__.py

```python

```

## utils.py

```python
import requests
import os
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
```

## __init__.py

```python

```

## chat_with_gpt.py

```python
import openai

class ChatWithGPT:
    def __init__(self, credentials):
        self.api_key = credentials['api_key']
        openai.api_key = self.api_key
        self.prefix = '!'

    def chat(self, prompt):
        response = openai.Completion.create(
            engine="text-davinci-002",
            prompt=prompt,
            max_tokens=150,
            n=1,
            stop=None,
            temperature=0.5,
        )

        message = response.choices[0].text.strip()
        return message

    def is_command(self, message):
        return message.content.startswith(self.prefix)

    async def handle_command(self, twitch_chat, message):
        command = message.content[1:]  
        prompt = f"Responde al comando: {command}"
        response = self.chat(prompt)

        await twitch_chat.send_message(response)
```

## twitch_chat.py

```python
from dotenv import load_dotenv
from twitchio.ext import commands
import asyncio, os
import requests

class TwitchChat(commands.Bot):

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
```

## __init__.py

```python

```

