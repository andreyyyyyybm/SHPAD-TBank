import asyncio
import requests

from yandex_cloud_ml_sdk import YCloudML
import os
from dotenv import load_dotenv
import json
import codecs
from aiogram.types import Message

load_dotenv()

with codecs.open("ml/promt.txt","r","utf-8") as promt_:
    promt = promt_.read()

folder_id = os.environ["FOLDER_ID"]
api_key = os.environ["API_KEY"]
def find_trip():
    # br = do_utils.BudgetRepository()
    min_cost = 100_000
    max_cost = 200_000
    white_list = "Italy, France"
    black_list = "Rome"
    pref = "Skiing,diving in a warm sea"
    with_dates = ""
    end_dates = ""


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
                "text": f"У тебя есть список данных для поездки. В них может быть бюджет поездки, желаемые места и так далее. Ты должен на основе этих данных составить план путешествия, найти туры, гостиницы, билеты и так далее. Тебе необязательно планировать путешествие со всеми интересами и желаниями. Дай подроный ответ с планом путшествия, ценой, датами и так далее.\n\n"
                f"Бюджет: от {min_cost} до {max_cost}\n\n"
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
        trip = data["trip"]
        # Формируем текст
        text_message = f"""
        📌 Планирование путешествия: *{trip['name']}*

        🗓 Даты: {trip['start_date']} — {trip['end_date']}
        📍 Описание: {trip['description']}

        💰 Бюджет: {trip['budget']['total']} {trip['budget']['currency']}
        """ + "\n".join([f"- {expense['category']}: {expense['amount']} {trip['budget']['currency']}" for expense in
                         trip['budget']['expenses']])

        # Добавляем маршрут
        for destination in trip['destinations']:
            text_message += f"""
        🌍 Маршрут:
        {destination['city']}, {destination['country']} ({destination['arrival_date']} — {destination['departure_date']})
           - Проживание: {destination['accommodation']['name']} ({destination['accommodation']['type']}), {destination['accommodation']['cost_per_night']} {trip['budget']['currency']}/ночь
           - Активности:""" + "\n".join([
                                                                                                                                                                                                                                                                                                                                                                               f"     - {act['name']} ({act['date']} {act['time']}), стоимость: {act['cost']} {trip['budget']['currency']}"
                                                                                                                                                                                                                                                                                                                                                                               for
                                                                                                                                                                                                                                                                                                                                                                               act
                                                                                                                                                                                                                                                                                                                                                                               in
                                                                                                                                                                                                                                                                                                                                                                               destination[
                                                                                                                                                                                                                                                                                                                                                                                   'activities']])

        # Добавляем транспорт
        text_message += "\n\n✈️ Транспорт:"
        for transport in trip['transport']:
            text_message += f"""
        - {transport['type']}: {transport['departure']['city']} → {transport['arrival']['city']} ({transport['departure']['date']} {transport['departure']['time']})
          - Бронь: {transport['booking_reference']}, стоимость: {transport['cost']} {trip['budget']['currency']}"""

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
