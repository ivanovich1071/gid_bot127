import sqlite3
from aiogram import Router, types
from aiogram.filters import Command
from services.weather_service import get_weather
from services.audio_service import create_voice_message
from services.image_service import choose_image_by_temperature
from services.openai_service import get_city_info

router = Router()

# Хендлер для регистрации города
@router.message(Command("city"))
async def city_command(message: types.Message):
    await message.reply("Введите название города:")

# Хендлер для получения и отправки погоды с изображением и голосовым сообщением
@router.message(lambda message: not message.text.startswith("/"))
async def get_city_weather(message: types.Message):
    city_name = message.text
    weather_data = await get_weather(city_name)

    if weather_data:
        city = weather_data["name"]
        temperature = weather_data["main"]["temp"]
        humidity = weather_data["main"]["humidity"]
        pressure = weather_data["main"]["pressure"]

        # Сохранение города в БД
        conn = sqlite3.connect("users.db")
        cursor = conn.cursor()
        cursor.execute("SELECT requested_cities FROM users WHERE chat_id = ?", (message.chat.id,))
        cities = cursor.fetchone()[0]
        if cities:
            cities = cities + f", {city_name}"
        else:
            cities = city_name
        cursor.execute("UPDATE users SET requested_cities = ? WHERE chat_id = ?", (cities, message.chat.id))
        conn.commit()
        conn.close()

        weather_text = (f"В городе {city} температура - {temperature}°C\n"
                        f"Влажность воздуха - {humidity}%\n"
                        f"Атмосферное давление - {pressure} мм рт. ст.")

        # Создаем голосовое сообщение
        voice_message_path = create_voice_message(weather_text)

        # Отправка голосового сообщения
        await message.reply_voice(voice=types.FSInputFile(voice_message_path))

        # Выбор и отправка изображения в зависимости от температуры
        image_path = choose_image_by_temperature(temperature)
        if image_path:
            await message.answer_photo(photo=types.FSInputFile(image_path))

        await message.reply(weather_text)

        # Получение дополнительной информации о городе через OpenAI
        city_info = await get_city_info(city_name)
        if city_info:
            await message.reply(f"Информация о городе {city_name}:\n{city_info}")
        else:
            await message.reply("Не удалось получить информацию о городе через OpenAI.")

    else:
        await message.reply("Не удалось найти погоду для указанного города. Пожалуйста, проверьте правильность написания города.")
