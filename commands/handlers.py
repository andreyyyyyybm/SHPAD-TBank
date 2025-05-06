import os

from aiogram import F, Router
from aiogram.filters import CommandStart, StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import BufferedInputFile, CallbackQuery, Message

import commands.keyboards as kb

router = Router()


@router.message(CommandStart())
async def start(message: Message):
    await message.reply(text="f", reply_markup=kb.keryboard_main)


@router.callback_query(lambda call: call.data == "system")
async def system_setting(callback: CallbackQuery):
    await callback.message.reply(
        text="А ВОТ ТУТ КЛАВИАТУРУ НЕ СДЕЛАЛИ...(бить того кто кнопки делал)"
    )


@router.callback_query(lambda call: call.data == "travel")
async def menu_travel(callback: CallbackQuery):
    await callback.message.reply(
        text="Ну типа привет?", reply_markup=kb.keyboard_trip
    )


@router.callback_query(lambda call: call.data == "prioritires")
async def menu_prioritires(callback: CallbackQuery):
    await callback.message.reply(text="f", reply_markup=kb.prioritires)


@router.callback_query(lambda call: call.data == "white_list")
async def preferences_w(callback: CallbackQuery):
    await callback.message.reply(
        text="1. Сходить в бар(онли Яндекс) \n 2. См. пункт 1",
        reply_markup=kb.keyboard_pr_white,
    )


@router.callback_query(lambda call: call.data == "black_list")
async def preferences_b(callback: CallbackQuery):
    await callback.message.reply(text="f", reply_markup=kb.keryboard_pr_black)


@router.callback_query(lambda call: call.data == "interests")
async def interests(callback: CallbackQuery):
    await callback.message.reply(
        text="Я ХЗ ЧТО ПИСАТЬ!!", reply_markup=kb.keyboard_interests
    )


@router.callback_query(lambda call: call.data == "buget")
async def buget(callback: CallbackQuery):
    await callback.message.reply(
        text="Ваш минимальный бюджет <budget_min>, максимальный <budget_max>.",
        reply_markup=kb.keryboard_budget,
    )


@router.callback_query(lambda call: call.data == "responsibility")
async def task_manager(callback: CallbackQuery):
    await callback.message.reply(
        text="тут типа админ добавит :)", reply_markup=kb.keyboard_task
    )
