import datetime
import re
from yandex_cloud_ml_sdk import YCloudML

import os
from dotenv import load_dotenv


load_dotenv()

folder_id = os.environ["FOLDER_ID"]
api_key = os.environ["API_KEY"]
def trip_input(raw_text) -> dict:
    sdk = YCloudML(
        folder_id=folder_id,
        auth=api_key
    )
    model = sdk.models.completions("yandexgpt-lite", model_version="rc")
    model = model.configure(temperature=0.0)

    system_prompt = (
        "Ты бот для разбора пользовательского ввода. "
        "Верни строго Python-словарь с ключами:\n"
        "  min_budget: int\n"
        "  max_budget: int\n"
        "  city_from: str  # место\n"
        "  whitelist: str  # места через пробел\n"
        "  blacklist: str  # места через пробел\n"
        "  preferences: str\n"
        "  with_dates: datetime.datetime\n"
        "  end_dates: datetime.datetime\n"
        "Без Markdown-оформления, только literal-dict."
    )
    user_prompt = f"RAW_INPUT:\n{raw_text}"

    response_iter = model.run([
        {"role": "system", "text": system_prompt},
        {"role": "user",   "text": user_prompt},
    ])
    alt = next(iter(response_iter), None)

    raw = alt.text

    # Убираем markdown-кодовые блоки, если есть
    raw = re.sub(r"^```(?:\w+)?\s*", "", raw.strip())
    raw = re.sub(r"\s*```$", "", raw, flags=re.MULTILINE)
    raw = raw.strip()

    try:
        parsed = eval(raw, {"datetime": datetime})
    except Exception as e:
        print("Ошибка при разборе eval:", e)
        return None

    return [parsed.get("min_budget"), parsed.get("max_budget"), parsed.get("city_from"), parsed.get("whitelist"), parsed.get("blacklist"),
            parsed.get("preferences"), parsed.get("with_dates"), parsed.get("end_dates")]


if __name__ == "__main__":
    example_input = (
        "Бюджет: от 500 до 1500\n"
        "Приоритетные места: Москва, Санкт-Петербург, Казань\n"
        "Черный список мест: Тула, Ярославль\n"
        "Интересы путешественников: музеи, гастрономия\n"
        "Примерные даты: 2025-06-10 — 2025-06-20"
    )

    out = trip_input(example_input)
    if out:
        print(out)