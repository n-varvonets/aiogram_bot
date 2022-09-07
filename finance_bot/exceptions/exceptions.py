"""Кастомные исключения, генерируемые приложением"""


class NotCorrectMessage(Exception):
    """Некорректное сообщение в бот, которое не удалось распарсить"""
    pass


class NotCorrectMessageSetBudjet(Exception):
    """Некорректное сообщение в бот, которое cсодержит слово бюджет"""
    pass
