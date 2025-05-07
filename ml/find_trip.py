import asyncio
import requests

from yandex_cloud_ml_sdk import YCloudML
import os
from dotenv import load_dotenv
import json
import codecs
from ml.links_search import build_travel_links
from ml.web_search import web_search_transport, web_search_resident
from ml.price_extract import price_extract
from aiogram import F, Router

router = Router()
from aiogram import F, Router
from aiogram import F, Router
from aiogram.types import Message

import commands.handlers


load_dotenv()

with codecs.open("ml/promt.txt","r","utf-8") as promt_:
    promt = promt_.read()

folder_id = os.environ["FOLDER_ID"]
api_key = os.environ["API_KEY"]
def find_trip(data):
    # br = do_utils.BudgetRepository()
    print(data)
    min_cost, max_cost, city_from, white_list, black_list, pref, with_dates, end_dates = data


    sdk = YCloudML(
        folder_id=folder_id, auth=api_key
    )

    model = sdk.models.completions("yandexgpt", model_version="rc")
    model = model.configure(temperature=0.3)
    result = model.run(
        [
            {"role": "system", "text": "Ты ассистент для планирования путешествий. Ты должен предоставить ответ строго в предоставленном формате json:"
            f"{promt}"
             },
            {
                "role": "user",
                "text": f"У тебя есть список данных для поездки. В них может быть бюджет поездки, желаемые места и так далее. Ты должен на основе этих данных составить план путешествия, найти туры, гостиницы, билеты и так далее. Тебе необязательно планировать путешествие со всеми интересами и желаниями. Не старайся потратить всю сумму. Дай подроный ответ с планом путшествия, ценой, датами и так далее.\n\n"
                f"Бюджет: от {min_cost} до {max_cost}\n\n"
                f"Город отправления: {city_from}\n\n"
                f"Приоритетные места: {white_list}\n\n"
                f"Черный список мест: {black_list}\n\n"
                f"Интересы путешественников: {pref}\n\n"
                f"Cвободные даты: c {with_dates} по {end_dates}\n\n"
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

        # travel_json = alternative.text
        # data = json.loads(alternative.text)
        # Загружаем JSON

        # data = json.loads(travel_json)
        # data = json.loads(travel_json)
        print(data)
        trip = data["trip"]
        white_list = [x for x in white_list.split()]
        if len(white_list) != 1:
            to_city = white_list[0]
        else:
            to_city = white_list
        # links = build_travel_links(city_from, to_city, with_dates, end_dates)
        # Формируем текст
        text_message = f"""
        📌 Планирование путешествия: *{trip['name']}*

🗓 Даты: {trip['start_date']} — {trip['end_date']}
📍 Описание: {trip['description']}

💰 Бюджет: {trip['budget']['total']} {trip['budget']['currency']}""" + "\n".join([f"- {expense['category']}: {expense['amount']} {trip['budget']['currency']}" for expense in
trip['budget']['expenses']])

        text_liv = "Проживание:"

        for destination in trip['destinations']:
            text_message += f"""
🌍 Маршрут:
{destination['city']}, {destination['country']} ({destination['arrival_date']} — {destination['departure_date']})
- [{text_liv}]({build_travel_links(city_from, destination['city'], with_dates, end_dates)["booking"]}) {price_extract(web_search_resident(destination['city']))}/ночь
- Активности:""" + "\n" + "\n".join([
       f"- {act['name']} ({act['date']} {act['time']}), стоимость: {act['cost']} {trip['budget']['currency']}"
       for
       act
       in
       destination[
           'activities']])

        # Добавляем транспорт
        text_message += f"\n\n✈️ Транспорт:"
        # text_message += f"\n\n✈️ [{text_dr}]({links["google_flights"]}):"

        for transport in trip['transport']:
            text_message += f"""
- [{transport['type']}]({build_travel_links(transport['departure']['city'], transport['arrival']['city'], with_dates, end_dates)["google_flights"]}): {transport['departure']['city']} → {transport['arrival']['city']} ({transport['departure']['date']} {transport['departure']['time']})
- Примерная стоимость: {price_extract(web_search_transport(transport['departure']['city'],transport['arrival']['city']))} {trip['budget']['currency']}"""
        # participant = [callback.get_chat_member(callback.message.chat.id)]
        # print(participant)
        # Добавляем участников




        text_message += "\n\n👥 Участники:"
        for participant in trip['participants']:
            text_message += f"\n- {participant['name']} ({participant['role']}, контакт: {participant['contact']})"

        # Добавляем чеклист
        text_message += "\n\n✅ Чеклист:"
        for item in trip['checklist']:
            status = "✓" if item['completed'] else " "
            text_message += f"\n- [{status}] {item['item']}"

        # Добавляем заметки
        text_message += f"\n\n📝 Заметки:\n{trip['notes']}"
        return text_message
# СДЕЛАЙ ИМПОРТ ТАЙМ ТЕКУЩИЙ