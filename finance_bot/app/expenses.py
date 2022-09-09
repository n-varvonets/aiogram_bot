""" Работа с расходами — их добавление, удаление, статистики"""
import datetime
import re

from typing import NamedTuple, Optional
from db import db

from exceptions import exceptions
from finance_bot.app.categories import Categories


class Message(NamedTuple):
    """Структура распаршенного сообщения о новом расходе"""
    amount: int
    category_text: str


class Expense(NamedTuple):
    """Структура добавленного в БД нового расхода"""
    id: Optional[int]
    amount: int
    category_name: str


def add_expense(raw_message: str) -> Expense:
    """Добавляет новое сообщение.
    Принимает на вход текст сообщения, пришедшего в бот."""
    parsed_message = _parse_message(raw_message)
    category = Categories().get_category(
        parsed_message.category_text)
    db.insert("expense", {
        "amount": parsed_message.amount,
        "created": _get_now_datetime(),
        "category_codename": category.codename,
        "raw_text": raw_message
    })
    return Expense(id=None,
                   amount=parsed_message.amount,
                   category_name=category.name)


def get_today_statistics() -> str:
    """Возвращает строкой статистику расходов за сегодня"""

    total_income, month_planing_base_expenses = _get_month_budget()
    if total_income == 0 and month_planing_base_expenses == 0:
        return (

                "⚠️ -  вкажіть Ваш місячний бюджет для отримання доступу до\n"
                "перегляду статистики за сьогодні(/today) чи за поточний місяць(/month) \n\n"
                "/set_budget - встановити місячний бюджет\n"
                "/help- дізнатися більше про статистику та місячний бюджет"
                )

    cursor = db.get_cursor()
    cursor.execute("select sum(amount)"
                   "from expense where date(created)=date('now', 'localtime')")
    result = cursor.fetchone()
    if not result[0]:
        return "Ви сьогодні не зробили жодної витрати"
    all_today_expenses = result[0]
    cursor.execute("select sum(amount) "
                   "from expense where date(created)=date('now', 'localtime') "
                   "and category_codename in (select codename "
                   "from category where is_base_expense=true)")
    result = cursor.fetchone()
    base_today_expenses = result[0] if result[0] else 0
    return (f"Витрати сьогодні:\n"
            f"усього — {all_today_expenses} грн.\n"
            f"базові — {base_today_expenses} грн\n\n"
            f"За поточний місяц: /month")


def get_month_statistics() -> str:
    """Returns expense statistics for the current month as a string"""

    total_income, month_planing_base_expenses = _get_month_budget()
    if total_income == 0 and month_planing_base_expenses == 0:
        return (

                "⚠️ -  вкажіть Ваш місячний бюджет для отримання доступу до\n"
                "перегляду статистики за сьогодні(/today) чи за поточний місяць(/month) \n\n"
                "/set_budget - встановити місячний бюджет\n"
                "/help- дізнатися більше про статистику та місячний бюджет"
                )

    now = _get_now_datetime()
    first_day_of_month = f'{now.year:04d}-{now.month:02d}-01'
    cursor = db.get_cursor()
    cursor.execute(f"select sum(amount) "
                   f"from expense where date(created) >= '{first_day_of_month}'")
    result = cursor.fetchone()
    if not result[0]:
        return "У цьому місяці поки що нема витрат"
    all_month_expenses = result[0]
    cursor.execute(f"select sum(amount) "
                   f"from expense where date(created) >= '{first_day_of_month}' "
                   f"and category_codename in (select codename "
                   f"from category where is_base_expense=true)")
    result = cursor.fetchone()
    base_month_expenses = result[0] if result[0] else 0

    return (f"Витрати в поточному місяці:\n"
            f"всього — {all_month_expenses} грн.\n"
            f"базові — {base_month_expenses} грн з "
            f" грн місячної норми")


def _get_last_five_expenses():  #  -> List[(Expense, List(str))]
    """Returns the last few expenses"""
    cursor = db.get_cursor()
    cursor.execute(
        "select e.id, e.amount, c.name, e.raw_text "
        "from expense e left join category c "
        "on c.codename=e.category_codename "
        "order by created desc limit 10")
    rows = cursor.fetchall()
    last_5_expenses_with_raw_text = [(Expense(id=row[0], amount=row[1], category_name=row[2]), row[3]) for row in rows]
    return last_5_expenses_with_raw_text


def delete_expense(row_id: int) -> None:
    """Deletes a message by its id"""
    db.delete("expense", row_id)


def _parse_message(raw_message: str) -> Message:
    """Parsing content in incoming message about a new expense."""
    regexp_result = re.match(r"([\d ]+) (.*)", raw_message)
    if not regexp_result or not regexp_result.group(0) \
            or not regexp_result.group(1) or not regexp_result.group(2):
        raise exceptions.NotCorrectMessage(
            "Не можу зрозуміти повідомлення. Напишіть повідомлення у форматі, "
            "наприклад:\n100 таксі")

    amount = regexp_result.group(1).replace(" ", "")
    category_text = regexp_result.group(2).strip().lower()
    return Message(amount=amount, category_text=category_text)


def _get_now_datetime() -> str:
    """Возвращает сегодняшнюю дату строкой"""
    return datetime.datetime.utcnow().strftime("%Y-%m-%d %H:%M:%S")


def _get_month_budget():
    """Return current values of month budjet(total_income, month_planing_base_expenses)"""
    return tuple(db.fetchall("budget", ["total_income", "month_planing_base_expenses"])[-1].values())
