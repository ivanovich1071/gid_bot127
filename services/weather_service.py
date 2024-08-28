import aiohttp
from config import WEATHER_API_KEY

async def get_weather(city_name):
    async with aiohttp.ClientSession() as session:
        url = f"http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={WEATHER_API_KEY}&units=metric&lang=ru"
        async with session.get(url) as response:
            if response.status == 200:
                weather_data = await response.json()
                if "main" in weather_data:
                    return weather_data
                else:
                    return None
            else:
                return None

