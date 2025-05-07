import os
from langchain_google_community import GoogleSearchAPIWrapper
from langchain_core.tools import Tool


def web_search(city_from, to_city):
    # Установи переменные
    os.environ["GOOGLE_API_KEY"] = "AIzaSyBLmm2Y4myjPmvZ-id7EUhag8Vg5Z156pw"
    os.environ["GOOGLE_CSE_ID"] = "2115f8b93d67f4c0b"

    # Создай обёртку поиска
    search = GoogleSearchAPIWrapper()

    tool = Tool(
        name="google_search",
        description="Поиск в Google",
        func=search.run,
    )

    # Пример запроса
    _ = tool.run(f"посмотри примерную цену на билет от {city_from} до {to_city}")
    print(_)
    return _
