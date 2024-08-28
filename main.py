from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import Update

from config import TOKEN
from handlers import start_handler, weather_handler, info_handler
from utils.storage import init_db

init_db()

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())

# Регистрация хендлеров
dp.include_router(start_handler.router)
dp.include_router(weather_handler.router)
dp.include_router(info_handler.router)
@dp.errors()
async def error_handler(update: Update, error: Exception):
    print(f"Произошла ошибка: {error}")
    return True


if __name__ == "__main__":
    dp.run_polling(bot)
