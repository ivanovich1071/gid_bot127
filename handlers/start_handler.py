import sqlite3
from aiogram import Router, types
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from keyboards.main_keyboard import registration_keyboard

router = Router()

# Состояния регистрации
class RegistrationStates(StatesGroup):
    waiting_for_name = State()
    waiting_for_age = State()
    waiting_for_city = State()

# Хендлер для команды /start
@router.message(Command("start"))
async def start_command(message: types.Message, state: FSMContext):
    user_id = message.from_user.id
    username = message.from_user.username
    await message.reply("Добро пожаловать! Давайте начнем регистрацию. Как вас зовут?", reply_markup=types.ReplyKeyboardRemove())
    await state.set_state(RegistrationStates.waiting_for_name)

    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("INSERT OR IGNORE INTO users (username, chat_id) VALUES (?, ?)", (username, message.chat.id))
    conn.commit()
    conn.close()

# Хендлер для регистрации имени
@router.message(RegistrationStates.waiting_for_name)
async def register_name(message: types.Message, state: FSMContext):
    name = message.text
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET registration_name = ? WHERE chat_id = ?", (name, message.chat.id))
    conn.commit()
    conn.close()
    await message.reply("Спасибо! Теперь укажите ваш возраст:")
    await state.set_state(RegistrationStates.waiting_for_age)

# Хендлер для регистрации возраста
@router.message(RegistrationStates.waiting_for_age)
async def register_age(message: types.Message, state: FSMContext):
    if not message.text.isdigit():
        await message.reply("Пожалуйста, введите ваш возраст числом.")
        return
    age = int(message.text)
    conn = sqlite3.connect("users.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE users SET age = ? WHERE chat_id = ?", (age, message.chat.id))
    conn.commit()
    conn.close()
    await message.reply("Отлично! Теперь укажите город, в котором вы проживаете:")
    await state.set_state(RegistrationStates.waiting_for_city)
