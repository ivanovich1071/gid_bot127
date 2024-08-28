import os
from gtts import gTTS
from datetime import datetime

def create_voice_message(text, lang='ru'):
    # Создаем директорию 'audio', если она не существует
    audio_dir = "audio"
    os.makedirs(audio_dir, exist_ok=True)

    # Генерация уникального имени файла
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
    voice_file_path = os.path.join(audio_dir, f"voice_message_{timestamp}.mp3")

    # Создание голосового сообщения
    tts = gTTS(text=text, lang=lang)
    tts.save(voice_file_path)

    return voice_file_path

