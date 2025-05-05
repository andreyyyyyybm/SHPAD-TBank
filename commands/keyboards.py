from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

keryboard_settings = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Системные", callback_data="system")],
        [InlineKeyboardButton(text="Путеществие", callback_data="travel")],
    ], 
)


keryboard_alerts = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Включить", callback_data="alerts_on"),
         InlineKeyboardButton(text="Выключить", callback_data="alerts_off")]
    ], 
)

keyboard_trip = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Приоритеты", callback_data=  "prioritires")], 
        [InlineKeyboardButton(text="Бюджет", callback_data="buget")],
        [InlineKeyboardButton(text="Интересы", callback_data="interests")],
        [InlineKeyboardButton(text="Отвественность", callback_data="responsibility")],
    ],
)

keyboard_priorities = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Мои предпочтения", callback_data=  "white_list"), 
        InlineKeyboardButton(text="Исключить направление", callback_data="black_list")],
        [InlineKeyboardButton(text="Мне без разницы куда ехать", callback_data="no_matter")],
    ],
)

keyboard_interests = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Посмотреть интересы", callback_data="wathc_int")],
        [InlineKeyboardButton(text="Добавить", callback_data=  "add_int"), 
        InlineKeyboardButton(text="Удалить", callback_data="del_int")],
    ],
)



button_names = ["Путешествия", "Музыка", "Программирование"]

keyboard_task = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text=name, callback_data=f"task{idx+1}")]
        for idx, name in enumerate(button_names)
    ]
)


keyboard_comp = InlineKeyboardMarkup(
    inline_keyboard=[
        [InlineKeyboardButton(text="Выполнено", callback_data="alerts_on"),
         InlineKeyboardButton(text="Не выполлнено", callback_data="alerts_off")]
    ], 
)

button_names = ["Путешествия", "Музыка", "Программирование", "Спорт"]

keyboard_groups = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text=button_names[i], callback_data=f"group{i+1}"),
            InlineKeyboardButton(text=button_names[i+1], callback_data=f"group{i+2}")
        ] for i in range(0, len(button_names) - 1, 2)
    ] + (
        [[InlineKeyboardButton(text=button_names[-1], callback_data=f"group{len(button_names)}")]]
        if len(button_names) % 2 else []
    )
)