#!/bin/bash

# Crear las carpetas
mkdir -p src/audio
mkdir -p src/chat
mkdir -p src/utils
mkdir -p tests
mkdir -p features

# Mover archivos a las carpetas correspondientes
mv audio_processor.py src/audio/
mv twitch_audio.py src/audio/
touch src/audio/__init__.py

mv chat_with_gpt.py src/chat/
mv twitch_chat.py src/chat/
touch src/chat/__init__.py

mv utils.py src/utils/
touch src/utils/__init__.py

mv bot_twitch.py src/

mv test_new_features.py tests/

mv new_features.py features/

# El resto de los archivos como README.md, version.txt, chromedriver, env y help ya están en la ubicación correcta.
