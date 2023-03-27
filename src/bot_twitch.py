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

from utils.audit_decorators import AuditBase
from src.utils.custom_logger import CustomLogger

CustomLogger.setup_custom_logging()
import logging

from dotenv import load_dotenv

class TwitchBot(AuditBase):
    def __init__(self, twitch_credentials, chatgpt_credentials, google_credentials_file, chromedriver_path, nombre_del_streamer, log_level=None):
        self.twitch_chat = TwitchChat(twitch_credentials, nombre_del_streamer)
        #self.audio_processor = AudioProcessor(google_credentials_file)
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

    # Ejecutar las dos corutinas de forma concurrente.
    await asyncio.gather(
        escuchar_chat_wrapper(),
        #escuchar_audio_wrapper()
    )

if __name__ == '__main__':
    asyncio.run(main())
