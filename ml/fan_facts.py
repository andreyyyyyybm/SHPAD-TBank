import datetime
import re
from yandex_cloud_ml_sdk import YCloudML

import os
from dotenv import load_dotenv


load_dotenv()

folder_id = os.environ["FOLDER_ID"]
api_key = os.environ["API_KEY"]
def fan_fact(place):
    sdk = YCloudML(
        folder_id=folder_id,
        auth=api_key
    )
    model = sdk.models.completions("yandexgpt", model_version="rc")
    model = model.configure(temperature=0.3)

    system_prompt = (
        "Ты бот для создания интересных фактов про города, чтобы привлекать внимание туристов к нему. Ты должен предоставить факт только про тот город, который тебе дают. Опираться на интернет и другие источники. Факт должен быть небольшим по размеру."
    )
    user_prompt = f"Напиши факт про город {place} "

    response_iter = model.run([
        {"role": "system", "text": system_prompt},
        {"role": "user",   "text": user_prompt},
    ])
    result = model.run(response_iter)
    for alternative in result:
        print(alternative)
        return alternative.text