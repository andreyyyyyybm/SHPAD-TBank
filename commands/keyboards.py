from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keyboard_main = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Информация", callback_data="info")],
        [InlineKeyboardButton(text="Настройки", callback_data="seting")],
    ],
)

keyboard_budget = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Минимальный бюджет", callback_data="min_bud")],
        [InlineKeyboardButton(text="Максимальный бюджет", callback_data="max_bud")],
    ],
)