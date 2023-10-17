from datetime import datetime


def string_to_date(string, date_format="%B %d, %Y at %I:%M%p"):
    """Преобразовывает строку заданного формата в дату.
    Возвращает дату"""
    date = datetime.strptime(string, date_format)
    return date


def get_last_news(values):
    """Возвращает последнюю запись из google-таблицы
    в виде списка содержимого заполненных ячеек"""
    return values[-1]
