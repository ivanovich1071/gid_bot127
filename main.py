from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand
from config import TOKEN
from handlers import start_handler, weather_handler, info_handler

# Создаем основные объекты
bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Регистрируем хендлеры
dp.include_router(start_handler.router)
dp.include_router(weather_handler.router)
dp.include_router(info_handler.router)

async def on_startup():
    await set_bot_commands()

async def set_bot_commands():
    commands = [
        BotCommand(command="/start", description="Начало работы"),
        BotCommand(command="/city", description="Узнать погоду в городе"),
        BotCommand(command="/info", description="Узнать информацию о городе")
    ]
    await bot.set_my_commands(commands)

if __name__ == "__main__":
    dp.run_polling(bot, on_startup=on_startup)
