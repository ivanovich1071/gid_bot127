import aiohttp
from aiogram import Router, types
from aiogram.filters import Command
from services.weather_service import get_weather

from services.audio_service import create_voice_message

#from services.audio_service import create_audio_message
from services.image_service import get_weather_image

router = Router()


# Хендлер для команды /weather, запрашивает у пользователя название города
@router.message(Command("weather"))
async def weather_command(message: types.Message):
    await message.reply("Введите название города для получения погоды:")


# Хендлер для обработки сообщений с названием города
@router.message(lambda message: not message.text.startswith("/"))
async def send_weather(message: types.Message):
    city_name = message.text.strip()

    # Получение данных о погоде
    weather_info = await get_weather(city_name)

    if weather_info is None:
        await message.reply("Не удалось получить информацию о погоде. Проверьте название города и попробуйте снова.")
        return

    # Отправка текстового сообщения с погодой
    weather_text = (
        f"Погода в городе {city_name}:\n"
        f"Температура: {weather_info['temperature']}°C\n"
        f"Описание: {weather_info['description']}\n"
        f"Скорость ветра: {weather_info['wind_speed']} м/с"
    )
    await message.reply(weather_text)

    # Отправка изображения с погодой
    weather_image = get_weather_image(weather_info['description'])
    await message.answer_photo(photo=weather_image)

    # Создание и отправка голосового сообщения
    audio_file_path = await create_audio_message(weather_text)
    await message.answer_voice(voice=audio_file_path)

    # Приглашение пользователя к запросу информации о городе
    await message.reply(
        f"Хотите узнать больше об этом городе, {city_name}? "
        "Введите ваш запрос для получения информации:"
    )


# Хендлер для обработки запросов пользователя о городе после получения погоды
@router.message(lambda message: not message.text.startswith("/"))
async def city_info_after_weather(message: types.Message):
    text_parts = message.text.split(maxsplit=1)

    if len(text_parts) == 1:
        await message.reply("Пожалуйста, введите запрос в формате: <город> <запрос>")
        return

    city_name, user_query = text_parts
    info = await get_city_info(city_name, user_query)

    await message.reply(info)
