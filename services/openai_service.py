import openai
from config import OPENAI_API_KEY

openai.api_key = OPENAI_API_KEY

async def get_city_info(city_name, user_query):
    prompt = (
        f"Ты-гид по городу {city_name}ты все знаешь про этот город,историю,географию,культурные события, музеи и памятники, гостиницы,достопримечательности т.е. абсолютно все про город .Ты отвечаешь на вопросы пользователя конкретно по городской теме. Ты-веселый гид.у тебя есть шутки про этот город. Отвечай пользователю только на вопросы про этот город."
        f"Вот запрос пользователя: {user_query}"
    )
    response = openai.ChatCompletion.create(
        model="gpt-3.5",
        messages=[
            {"role": "system", "content": prompt},
            {"role": "user", "content": user_query}
        ]
    )
    return response.choices[0].message["content"]
