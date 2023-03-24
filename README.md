# Twitch Chat GPT Bot

Este proyecto implementa un bot para interactuar en un chat de Twitch utilizando la API de ChatGPT de OpenAI y la API de reconocimiento de voz de Google Cloud. El bot puede escuchar el chat, procesar comandos, resumir el chat, y responder a preguntas directas del streamer.

## Archivos del proyecto

- `bot_twitch.py`: Archivo principal que contiene la implementación de la clase `TwitchBot`. Coordina la interacción con el chat de Twitch y el procesamiento de audio.
- `chat_with_gpt.py`: Clase `ChatWithGPT` que se encarga de interactuar con la API de ChatGPT de OpenAI para generar respuestas a comandos y preguntas.
- `audio_processor.py`: Clase `AudioProcessor` que utiliza la API de reconocimiento de voz de Google Cloud para procesar el audio y convertirlo en texto.
- `summarizer.py`: Contiene funciones para extraer palabras clave y generar resúmenes de la conversación del chat.
- `twitch_audio.py`: Clase `TwitchAudio` que se encarga de extraer el audio del stream de Twitch para ser procesado.
- `twitch_chat.py`: Clase `TwitchChat` que se encarga de la conexión y la interacción con el chat de Twitch.
- `utils.py`: Contiene funciones de utilidad, como la obtención del token de Twitch.
- `new_features.py`: Archivo que contiene ideas y propuestas para nuevas funcionalidades que podrían ser implementadas en el futuro.
- `test_new_features.py`: Archivo que contiene tests unitarios para las nuevas funcionalidades propuestas en `new_features.py`.

## Configuración

1. Instalar las dependencias del proyecto utilizando un entorno virtual:
   
python -m venv env
source env/bin/activate # En Windows: env\Scripts\activate
pip install -r requirements.txt


2. Obtener las credenciales para la API de ChatGPT de OpenAI y guardarlas en un archivo `.env` en la raíz del proyecto:

CHATGPT_API_KEY=tu_api_key


3. Obtener las credenciales para la API de Google Cloud y guardarlas en un archivo JSON en la raíz del proyecto.

4. Obtener las credenciales para la API de Twitch siguiendo las instrucciones en [este enlace](https://dev.twitch.tv/docs/authentication/getting-tokens-oauth). Añadir las credenciales al archivo `.env`:

TWITCH_CLIENT_ID=tu_client_id
TWITCH_CLIENT_SECRET=tu_client_secret
TWITCH_ACCESS_TOKEN=tu_access_token
TWITCH_REFRESH_TOKEN=tu_refresh_token
TWITCH_STREAMER_NAME=nombre_del_streamer


5. Descargar y configurar el [ChromeDriver](https://sites.google.com/a/chromium.org/chromedriver/downloads) correspondiente a tu versión de Chrome. Colocar el ejecutable en la raíz del proyecto.

6. Ejecutar el bot:

python bot_twitch.py


## Contribuciones

Siéntete libre de contribuir con nuevas funcionalidades o mejoras al proyecto. Asegúrate de añadir tests unitarios en `test_new_features.py` para las nuevas funcionalidades propuestas.

Este README cubre la descripción de los archivos, cómo configurar y ejecutar el proyecto, y cómo contribuir con nuevas funcionalidades o mejoras. Asegúrate de seguir las instrucciones para configurar las credenciales y las dependencias del proyecto antes de ejecutar el bot.
