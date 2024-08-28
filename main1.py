import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram.filters import Command
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
import openai
import requests
from gtts import gTTS

# Загрузка переменных окружения
load_dotenv()

TOKEN = os.getenv('TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')

# Создание экземпляра бота
bot = Bot(token=TOKEN)

# Создание диспетчера
dp = Dispatcher(storage=MemoryStorage())

openai.api_key = OPENAI_API_KEY

# Создание кнопок
stop_button = KeyboardButton(text='Остановить диалог')
keyboard = ReplyKeyboardMarkup(
    keyboard=[[stop_button]],  # Передача кнопки в виде вложенного списка
    resize_keyboard=True
)


# Функция для создания голосового сообщения
def create_voice_message(text):
    tts = gTTS(text, lang='ru')
    voice_message_path = "voice_message.ogg"
    tts.save(voice_message_path)
    return voice_message_path


# Функция для получения погоды
async def get_weather(city_name):
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None


# Функция для взаимодействия с OpenAI и сохранения диалога
async def get_city_info(city_name, user_query, user_dialogue):
    system_prompt = (
        f"Ты-гид по городу {city_name}. Ты всё знаешь про этот город: историю, географию, культурные события, музеи, памятники, гостиницы и достопримечательности. "
        "Отвечай на вопросы пользователя только по теме города. Ты весёлый гид с чувством юмора. "
        "Если пользователь задаёт вопрос не по теме города, отвечай: «Вы отвлеклись от темы разговора»."
    )

    messages = [{"role": "system", "content": system_prompt}]
    if user_dialogue:
        messages.extend(user_dialogue)
    messages.append({"role": "user", "content": user_query})

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=messages
    )

    reply = response.choices[0].message["content"]
    user_dialogue.append({"role": "assistant", "content": reply})

    return reply


# Хендлер команды /start
@dp.message(Command("start"))
async def start_command(message: types.Message):
    user_name = message.from_user.first_name
    await message.reply_voice(voice=types.FSInputFile(create_voice_message(f"Привет, {user_name}!")),
                              reply_markup=keyboard)
    await message.reply("О каком городе вы хотите узнать? Введите название или скажите его.")


# Хендлер команды /city
@dp.message(Command("city"))
async def city_command(message: types.Message):
    await message.reply("Введите название города:")


# Хендлер получения погоды и информации о городе
@dp.message(lambda message: message.text or message.voice)
async def get_city_weather_and_info(message: types.Message):
    user_id = message.from_user.id

    # Проверка, текстовое сообщение или голосовое
    if message.voice:
        voice_file = await message.voice.get_file()
        file_path = f"https://api.telegram.org/file/bot{TOKEN}/{voice_file.file_path}"
        audio_content = requests.get(file_path).content
        user_query = openai.Audio.transcribe("whisper-1", audio_content).get('text')
    else:
        user_query = message.text

    # Проверка на команду остановки диалога
    if user_query.lower() == 'остановить диалог':
        await message.reply("Диалог остановлен.", reply_markup=types.ReplyKeyboardRemove())
        return

    # Получение погоды
    weather_data = await get_weather(user_query)
    if weather_data:
        city_name = weather_data["name"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]

        weather_text = (f"В городе {city_name} температура - {temperature}°C\n"
                        f"Влажность воздуха - {humidity}%\n"
                        f"Атмосферное давление - {pressure} мм рт. ст.")

        voice_message_path = create_voice_message(weather_text)
        await message.reply_voice(voice=types.FSInputFile(voice_message_path))
        await message.reply(weather_text)

        # Инициализация диалога для пользователя, если его еще нет
        if not hasattr(message.from_user, 'dialogue'):
            message.from_user.dialogue = []

        # Получение информации о городе через OpenAI
        city_info = await get_city_info(city_name, user_query, message.from_user.dialogue)
        if city_info:
            await message.reply(city_info)
            voice_message_path = create_voice_message(city_info)
            await message.reply_voice(voice=types.FSInputFile(voice_message_path))
        else:
            await message.reply("Не удалось получить информацию о городе через OpenAI.")
    else:
        await message.reply(
            "Не удалось найти погоду для указанного города. Пожалуйста, проверьте правильность написания города.")


# Запуск бота
async def main():
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
