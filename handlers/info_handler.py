from aiogram import Router, types
from aiogram.filters import Command
from services.openai_service import get_city_info

router = Router()


# Хендлер для получения информации о городе через OpenAI
@router.message(Command("info"))
async def info_command(message: types.Message):
    await message.reply("Введите название города для получения информации:")


@router.message(lambda message: not message.text.startswith("/"))
async def city_info(message: types.Message):
    city_name = message.text.split()[0]
    user_query = ' '.join(message.text.split()[1:])

    if city_name:
        info = await get_city_info(city_name, user_query)
        await message.reply(info)
    else:
        await message.reply("Пожалуйста, введите название города.")
