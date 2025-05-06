import asyncio
import requests

from yandex_cloud_ml_sdk import YCloudML

import json


async def find_trip(message: Message) -> None:
    folder_id = "b1g1l90farmtbr7v0bip"
    api_key = "AQVN0R0iast5Eu7MYm-zpyxE6Jo9AZnloa9STQuX"
    # br = do_utils.BudgetRepository()
    min_cost = BudgetRepository
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
            """
            {
              "trip": {
                "id": "unique_trip_id",
                "name": "Название путешествия",
                "description": "Описание поездки",
                "start_date": "YYYY-MM-DD",
                "end_date": "YYYY-MM-DD",
                "budget": {
                  "total": 1000,
                  "currency": "USD",
                  "expenses": [
                    {
                      "category": "Транспорт",
                      "amount": 300,
                      "notes": "Авиабилеты"
                    },
                    {
                      "category": "Проживание",
                      "amount": 400,
                      "notes": "Отель"
                    },
                    {
                      "category": "Еда",
                      "amount": 200,
                      "notes": "Рестораны и кафе"
                    }
                  ]
                },
                "destinations": [
                  {
                    "city": "Название города",
                    "country": "Страна",
                    "arrival_date": "YYYY-MM-DD",
                    "departure_date": "YYYY-MM-DD",
                    "accommodation": {
                      "name": "Название отеля/хостела",
                      "address": "Адрес",
                      "type": "Отель/Апартаменты",
                      "cost_per_night": 100
                    },
                    "activities": [
                      {
                        "name": "Экскурсия в музей",
                        "date": "YYYY-MM-DD",
                        "time": "HH:MM",
                        "cost": 20,
                        "notes": "Билеты нужно купить заранее"
                      },
                      {
                        "name": "Прогулка по парку",
                        "date": "YYYY-MM-DD",
                        "time": "HH:MM",
                        "cost": 0,
                        "notes": "Бесплатно"
                      }
                    ]
                  }
                ],
                "transport": [
                  {
                    "type": "Авиаперелёт",
                    "departure": {
                      "city": "Город вылета",
                      "date": "YYYY-MM-DD",
                      "time": "HH:MM"
                    },
                    "arrival": {
                      "city": "Город прилёта",
                      "date": "YYYY-MM-DD",
                      "time": "HH:MM"
                    },
                    "booking_reference": "ABC123",
                    "cost": 250
                  },
                  {
                    "type": "Поезд",
                    "departure": {
                      "city": "Город отправления",
                      "date": "YYYY-MM-DD",
                      "time": "HH:MM"
                    },
                    "arrival": {
                      "city": "Город назначения",
                      "date": "YYYY-MM-DD",
                      "time": "HH:MM"
                    },
                    "booking_reference": "XYZ456",
                    "cost": 50
                  }
                ],
                "participants": [
                  {
                    "name": "Имя участника",
                    "contact": "email/телефон",
                    "role": "организатор/участник"
                  }
                ],
                "checklist": [
                  {
                    "item": "Загранпаспорт",
                    "completed": false
                  },
                  {
                    "item": "Бронь отеля",
                    "completed": true
                  }
                ],
                "notes": "Дополнительные заметки о поездке"
              }
            }"""
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

        await message.answer(text_message)