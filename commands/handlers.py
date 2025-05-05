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
    await message.reply(
        text="f",
        reply_markup=kb.keyboard_main
    )
