import asyncio, os
from chat_with_gpt import ChatWithGPT
from twitch_chat import TwitchChat
from audio_processor import AudioProcessor
from summarizer import extract_keywords, generate_summary
from twitch_audio import TwitchAudio
from utils import get_twitch_token
from dotenv import load_dotenv

class TwitchBot:
    def __init__(self, twitch_credentials, chatgpt_credentials, google_credentials_file, chromedriver_path, nombre_del_streamer):
        self.twitch_chat = TwitchChat(twitch_credentials)
        self.audio_processor = AudioProcessor(google_credentials_file)
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
    chatgpt_credentials = {'api_key': os.environ("CHATGPT_API_KEY")}
    google_credentials_file = 'path/to/your/google_credentials.json'
    chromedriver_path = 'chromedriver'
    nombre_del_streamer = os.environ("TWITCH_STREAMER_NAME") or "chusommontero"

    bot = TwitchBot(twitch_credentials, chatgpt_credentials, google_credentials_file, chromedriver_path, nombre_del_streamer)

    # Ejecutar las dos corutinas de forma concurrente.
    await asyncio.gather(
        bot.escuchar_chat(),
        bot.escuchar_audio()
    )

if __name__ == '__main__':
    asyncio.run(main())
