import asyncio
import requests

from yandex_cloud_ml_sdk import YCloudML
import os
from dotenv import load_dotenv
import json
import codecs
from datetime import datetime
import ml.format_message
from ml.links_search import build_travel_links
from ml.web_search import web_search_transport, web_search_resident
from ml.price_extract import price_extract
from aiogram import Router
import re

router = Router()

load_dotenv()

with codecs.open("ml/promt.txt", "r", "utf-8") as promt_:
    promt = promt_.read()

folder_id = os.environ["FOLDER_ID"]
api_key = os.environ["API_KEY"]


async def find_trip(data_prev):
    sdk = YCloudML(
        folder_id=folder_id, auth=api_key
    )

    model = sdk.models.completions("yandexgpt", model_version="rc")
    model = model.configure(temperature=0.3)
    result = model.run(
        [
            {"role": "system",
             "text": "Ты ассистент для планирования путешествий. Ты должен предоставить ответ строго в предоставленном формате json:"
                     f"{promt}"
             },
            {
                "role": "user",
                "text": f"У тебя есть список данных для поездки. В них может быть бюджет поездки, желаемые места и так далее. Ты должен на основе этих данных составить план путешествия, найти туры, гостиницы, билеты и так далее. Тебе необязательно планировать путешествие со всеми интересами и желаниями. Приводи актуальные цены на еду и транспорт. Ты не должен выходить за лимит суммы, но и не должен тратить её всю. Дай подроный ответ с планом путшествия, ценой, датами и так далее.\n\n"
                        f"Бюджет: от {data_prev["min_cost"]} до {data_prev["max_cost"]}\n\n"
                        f"Город отправления: {data_prev["city_from"]}\n\n"
                        f"Приоритетные места: {data_prev["white_list"]}\n\n"
                        f"Черный список мест: {data_prev["black_list"]}\n\n"
                        f"Интересы путешественников: {data_prev["pref"]}\n\n"
                        f"Cвободные даты: c {data_prev["with_dates"]} по {data_prev["end_dates"]}\n\n"
            },
        ]
    )

    for alternative in result:
        try:
            trip_data = alternative.text
            trip_data = trip_data.replace("`", """""")
            data = json.loads(trip_data)
        except json.JSONDecodeError as e:
            print('error_json')
            print(trip_data)
        # Загружаем JSON
        trip = data["trip"]
        # Формируем текст
        real_pricing_rent_dict = {}
        real_pricing_transport_dict = {}
        for destination in trip['destinations']:
            temp_price_ = price_extract(web_search_resident(destination['city']))
            # temp_price_ = "3421 рублей"
            temp_price_ = temp_price_.replace(" ", "")

            real_pricing_rent_dict[destination['city']] = int(*re.findall(r'\d+', temp_price_))
            print(real_pricing_rent_dict)
        for transport in trip['transport']:
            temp_price_ = price_extract(
                web_search_transport(transport['departure']['city'], transport['arrival']['city']).replace(" ", ""))
            # temp_price_ = "11113 рублей"
            temp_price_ = temp_price_.replace(" ", "")
            real_pricing_transport_dict[f'{transport['departure']['city']}-{transport['arrival']['city']}'] = int(
                *re.findall(r'\d+', temp_price_))

        real_pricing_rent = trip['budget']['expenses'][0]['amount']
        real_pricing_transport = trip['budget']['expenses'][1]['amount']
        print((datetime.strptime(data_prev["end_dates"], '%Y-%m-%d') - datetime.strptime(data_prev["with_dates"],'%Y-%m-%d')))
        try:
            if sum(real_pricing_rent_dict.values()) * (datetime.strptime(data_prev["end_dates"], '%Y-%m-%d') - datetime.strptime(data_prev["with_dates"],'%Y-%m-%d')).days < trip['budget']['total']:
                trip['budget']['expenses'][1]['amount'] = sum(real_pricing_rent_dict.values()) * (
                            datetime.strptime(data_prev["end_dates"], '%Y-%m-%d') - datetime.strptime(
                        data_prev["with_dates"], '%Y-%m-%d')).days
            if sum(real_pricing_transport_dict.values()) < trip['budget']['total']:
                trip['budget']['expenses'][0]['amount'] = sum(real_pricing_transport_dict.values())
        except Exception as e:
            print("error in real_pricing", e)

        return await ml.format_message.format_message(trip, data_prev, real_pricing_rent_dict,
                                                      real_pricing_transport_dict)
