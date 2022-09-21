from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

welcome_btns_block = InlineKeyboardMarkup(row_width=2) \
    .add(
    InlineKeyboardButton(text=f'📖 останні мої витрати', callback_data=f'expenses_cb_btn')).row(
    InlineKeyboardButton(text=f'🔒 статистика за сьогодні', callback_data=f'today_cb_btn'),
    InlineKeyboardButton(text=f'🔒 статистика за місяць', callback_data=f'month_cb_btn')
).row(
    InlineKeyboardButton(text=f'✏️ задати бюджет', callback_data=f'set_budget_cb_btn'),
    InlineKeyboardButton(text=f'🔎 актуальний бюджет', callback_data=f'get_budget_cb_btn')
).row(
    InlineKeyboardButton(text=f'🧩 категорії витрат', callback_data=f'categories_cb_btn'),
    InlineKeyboardButton(text=f'💭 додаткова інфа', callback_data=f'help_cb_btn')
)

welcome_btns_unblocked = InlineKeyboardMarkup() \
    .add(
    InlineKeyboardButton(text=f'📖 останні мої витрати', callback_data=f'expenses_cb_btn')).row(
    InlineKeyboardButton(text=f'📈 статистика за сьогодні', callback_data=f'today_cb_btn'),
    InlineKeyboardButton(text=f'📉 статистика за місяць', callback_data=f'month_cb_btn')
).row(
    InlineKeyboardButton(text=f'✏️ задати бюджет', callback_data=f'set_budget_cb_btn'),
    InlineKeyboardButton(text=f'🔎 актуальний бюджет', callback_data=f'get_budget_cb_btn')
).row(
    InlineKeyboardButton(text=f'🧩 категорії витрат', callback_data=f'categories_cb_btn'),
    InlineKeyboardButton(text=f'💭 додаткова інфа', callback_data=f'help_cb_btn')
)

back_to_main_btn = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text=f'📌 головне меню', callback_data=f'main_menu')
)

back_to_main_and_set_budjet_btn = InlineKeyboardMarkup().add(
    InlineKeyboardButton(text=f'✏️ задати місячний бюджет', callback_data=f'set_budget_cb_btn')
).row(
    InlineKeyboardButton(text=f'📌 головне меню', callback_data=f'main_menu'),
    InlineKeyboardButton(text=f'💭 додаткова інфа', callback_data=f'help_cb_btn')
)

static_and_back_main_menu = InlineKeyboardMarkup().row(
    InlineKeyboardButton(text=f'📖 останні мої витрати', callback_data=f'expenses_cb_btn'),
    InlineKeyboardButton(text=f'✏️ задати місячний бюджет', callback_data=f'set_budget_cb_btn')) \
    .row(
    InlineKeyboardButton(text=f'📈 статистика за сьогодні', callback_data=f'today_cb_btn'),
    InlineKeyboardButton(text=f'📉 статистика за місяць', callback_data=f'month_cb_btn')
).add(
    InlineKeyboardButton(text=f'📌 головне меню', callback_data=f'main_menu')
)
