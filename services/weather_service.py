import aiohttp
from config import WEATHER_API_KEY

async def get_weather(city_name):
    async with aiohttp.ClientSession() as session:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        async with session.get(url) as response:
            if response.status == 200:
                data = await response.json()
                # Обработка данных для удобства использования в коде
                weather_info = {
                    'temperature': data['main']['temp'],
                    'description': data['weather'][0]['description'],
                    'wind_speed': data['wind']['speed']
                }
                return weather_info
            else:
                return None

