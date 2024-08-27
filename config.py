import os
from dotenv import load_dotenv

# Загрузка переменных из .env файла
load_dotenv()

TOKEN = os.getenv('TOKEN')
WEATHER_API_KEY = os.getenv('WEATHER_API_KEY')
OPENAI_API_KEY = os.getenv('OPENAI_API_KEY')
