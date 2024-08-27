from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

# Клавиатура для регистрации
registration_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Начать регистрацию")]
    ],
    resize_keyboard=True
)

# Клавиатура для ввода города
city_keyboard = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text="Введите город")]
    ],
    resize_keyboard=True
)
