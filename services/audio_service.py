import os
from gtts import gTTS

def create_voice_message(text, lang='ru'):
    voice_file_path = os.path.join("audio", "voice_message.ogg")
    tts = gTTS(text=text, lang=lang)
    tts.save(voice_file_path)
    return voice_file_path
