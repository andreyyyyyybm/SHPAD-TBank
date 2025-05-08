import os

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter, Command
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile, CallbackQuery, Message

import commands.keyboards as kb
from ml import find_trip, message_processing, fan_facts
from db import database


db = database.Database()
router = Router()

# messages: dict[int, str] = {}
messages = {}
data_proc = ["не установлено" for x in range(6)]


async def history_for_chat_id(chat_id: int, db: database.Database) -> str:
    """
    Получает историю чата из базы данных и форматирует ее в строку.

    Args:
        chat_id: ID чата, историю которого нужно получить.
        db: Экземпляр класса Database для взаимодействия с базой данных.

    Returns:
        Строка с отформатированной историей чата.
    """
    history_list = await db.get_history(chat_id)
    history_text = ""
    if history_list:
        for item in history_list:
            history_text += f"{item.text}\n"
    return history_text


@router.message(CommandStart())
async def start(message: Message):
    await message.reply(text= """👋 Привет! Я — бот команды Т-БАНКА, и моя задача — сделать организацию совместных поездок простой и приятной.

✈️ Я помогу:

учесть интересы участников,
рассчитать бюджет,
распределить ответственность (кто покупает билеты, кто ищет жильё),
составить план и предложить лучшие направления.
🛠 Всё настраивается — от уведомлений до личных задач. Просто общайтесь, а я позабочусь о деталях!""", reply_markup=kb.keryboard_main)




@router.callback_query(lambda call: call.data == "system")
async def system_setting(callback: CallbackQuery):
    await callback.message.reply(
        text="Настройка уведомлений и т.д."
    )
    await callback.message.answer_photo("https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcQWxglAFKIZSP9XMDTNhZjXbh83o54vplMTEw&s")
    await callback.answer("", show_alert=True)

@router.callback_query(lambda call: call.data == "listen")
async def listen_setting(callback: CallbackQuery):
    await callback.message.reply(
        text="Выберите режим отслеживания сообщений", reply_markup=kb.keryboard_listen
    )
    await callback.answer("", show_alert=True)



@router.message(lambda message: message.text == "Включить")
async def listen_on(message: Message):
    chat_id = message.chat.id
    print(chat_id)
    if chat_id not in messages.keys():
        messages[chat_id] = ""
        await message.reply(
            text="""🎙 Я начал прослушку чата!

        Теперь просто поговорите в чате:
— Расскажите, какие у вас интересы и хобби
— Куда хотелось бы поехать, а куда точно не хотите
— Укажите бюджет: минимальный и максимальный
— Перечислите, что бы вы хотели сделать в поездке (например: море, музеи, еда, природа)

        Когда будете готовы — нажмите «Остановить прослушку».
        📩 После этого я соберу всё, что вы написали, и пришлю вам готовое предложение для совместного путешествия!"""
            , reply_markup=kb.keryboard_listen
        )
        await message.answer_photo("https://thumbs.dreamstime.com/b/%D1%87%D0%B5%D0%BB%D0%BE%D0%B2%D0%B5%D1%87%D0%B5%D1%81%D0%BA%D0%BE%D0%B5-%D1%83%D1%85%D0%BE-%D0%BD%D0%B0-%D0%B1%D0%B5%D0%BB%D0%BE%D0%BC-%D1%84%D0%BE%D0%BD%D0%B5-%D1%81%D0%B8%D0%BC%D0%B2%D0%BE%D0%BB-%D0%B2%D0%B5%D0%BA%D1%82%D0%BE%D1%80-%D0%B8%D0%BB%D0%BB%D1%8E%D1%81%D1%82%D1%80%D0%B0%D1%86%D0%B8%D1%8F-%D0%B2%D0%B5%D0%BA%D1%82%D0%BE%D1%80%D0%B0-211926595.jpg")
    else:
        await message.answer("Прослушка уже активна.")
@router.message(F.text != "Выключить")
async def collect_message(message: Message): #ОН РАБОТАЕТ ВСЕГДА. НЕЭФФЕКТИВНО. для презентации
    chat_id = message.chat.id
    if chat_id in messages.keys():
        messages[chat_id] = messages.get(chat_id,"") + f"\n{message.text}"


# @router.message(F.text)
# async def get_members(message: Message):
#     bot = message.bot  # Получаем бота из сообщения
#     members = []
#     async for member in bot.get_chat_member(message.chat.id):
#         members.append(member.user.full_name)
#     print(members)
#     # return members
#
#     await message.answer("\n".join(members))
@router.message(lambda message: message.text == "Выключить")
async def listen_off(message: Message):
    chat_id = message.chat.id
    if chat_id in messages:
        collected_text = messages[chat_id]
        #сделай обычные кнопки. инлайн уползет в истории, не найдешь.
        # здесь можно передать collected_text в анализ или email
        data_proc = message_processing.trip_input(collected_text)
        print(data_proc)
        if (data_proc):
            if data_proc[1] == None:
                data_proc[1] = data_proc[0]
            elif data_proc[0] == None:
                data_proc[0] = data_proc[1]

        if not(data_proc):
            await message.answer("Нужно прислать хоть что-нибудь содержательное")
            return None
        elif None in data_proc or (None, None) in data_proc:
            await message.answer("Слишком мало данных")
            return None
        del messages[chat_id]


        await message.reply(
            text=f"""⏳ Ваш тур почти готов!
            
Я уже подбираю лучшие маршруты, считаю бюджет и анализирую интересы команды.

А пока — вот интересный факт 🌍:

{fan_facts.fan_fact(data_proc[3])}"""
        )

        await message.reply(text=f"""🧳 Почти всё готово!
        
Мы уже знаем, что стоит искать туры в {", ".join(data_proc[3].split())} с суммой не более {data_proc[1]}₽.

📌 Подбираем лучший маршрут — осталось совсем немного!""")
        # print(messages)
        # members = message.bot.
        # print(members)
        temp_trip = find_trip.find_trip(data_proc)
        await db.history_add(chat_id, temp_trip)
        await message.answer(temp_trip, parse_mode="Markdown",reply_markup=kb.keryboard_main)
    else:
        await message.answer("Прослушка не была активна.")


@router.callback_query(lambda call: call.data == "travel")
async def menu_travel(callback: CallbackQuery):
    await callback.message.reply(
        text="Здесь ты можешь настроить основные параметры твоего путешествия!", reply_markup=kb.keyboard_trip
    )
    await callback.answer("", show_alert=True)



@router.callback_query(lambda call: call.data == "prioritires")
async def menu_prioritires(callback: CallbackQuery):
    await callback.message.reply(text=f"Ваши проиритеты: {data_proc[5]}"
                                 # , reply_markup=kb.prioritires
                                 )
    await callback.answer("", show_alert=True)


@router.callback_query(lambda call: call.data == "white_list")
async def preferences_w(callback: CallbackQuery):
    await callback.message.reply(
        text="Можешь добавить или убрать места из приоритета",
        reply_markup=kb.keyboard_pr_white,
    )
    await callback.answer("", show_alert=True)


@router.callback_query(lambda call: call.data == "black_list")
async def preferences_b(callback: CallbackQuery):
    await callback.message.reply(text="Можешь добавить или убрать места из черного списка", reply_markup=kb.keryboard_pr_black)
    await callback.answer("", show_alert=True)


@router.callback_query(lambda call: call.data == "past_trip")
async def past_trip(callback: CallbackQuery):

    await callback.message.reply(
        text=await history_for_chat_id(callback.message.chat.id, db),
        reply_markup=kb.keryboard_main,
        parse_mode="Markdown"
    )
    await callback.answer("", show_alert=True)


@router.callback_query(lambda call: call.data == "interests")
async def interests(callback: CallbackQuery):
    await callback.message.reply(
        text="Это - ваши интересы. И это прекрасно.", reply_markup=kb.keyboard_interests
    )
    await callback.message.answer_photo("https://i.pinimg.com/736x/97/6e/3d/976e3ddff4cf700b1449f262cf15865f.jpg")
    await callback.answer("", show_alert=True)


@router.callback_query(lambda call: call.data == "buget")
async def buget(callback: CallbackQuery):
    await callback.message.reply(
        text=f"Ваш минимальный бюджет - {data_proc[0]}, максимальный - {data_proc[1]}.",
        # reply_markup=kb.keryboard_budget,
    )
    await callback.answer("", show_alert=True)

@router.callback_query(lambda call: call.data == "responsibility")
async def task_manager(callback: CallbackQuery):
    await callback.message.reply(
        text="Чем выше бюджет, тем выше ответственность...", reply_markup=kb.keyboard_task
    )
    await callback.message.answer_photo("https://i.ytimg.com/vi/QmkSfc2If8Y/maxresdefault.jpg")
    await callback.answer("", show_alert=True)

# async def to_mess_proc(callback: CallbackQuery):




# async def trip_find(callback: CallbackQuery,data):
#     await callback.message.reply(text=f"{find_trip.find_trip(data)}")
