import time

from telegram import Bot

from google_client import get_sheet_data
from db import get_last_news_from_db, update_table
from settings import CHANNEL_ID, SECRET_TOKEN, RETRY_PERIOD, SPREADSHEET_ID
from utils import string_to_date


def get_new_news(last_news_from_db, values):
    """Находит новости, которые недавно добавили в google-таблицу.
    Возвращает из в виде списка"""
    last_news_list = []
    for row in values[::-1]:
        if string_to_date(row[0]) < string_to_date(last_news_from_db[0]):
            break
        if row[0] != last_news_from_db[0]:
            if len(row) == 6:
                last_news_list.append(row)
        else:
            break
    return last_news_list[::-1]


def update_news_in_bd(old_date_time, last_news_list):
    """Обновляет последнюю новость в бд"""
    if last_news_list:
        last_news = last_news_list[-1]
        update_table(old_date_time, last_news[0], last_news[1],
                     last_news[2], last_news[3], last_news[4])


def list_messages(last_news_list):
    """Получает список неопубликованных новостей
    и возвращает сообщения, которые должен отправть бот"""
    messages = []
    for news in last_news_list:
        message = f"{news[1]}\n {news[2]}\n {news[4]}"
        messages.append(message)
    return messages


def send_news(bot, message):
    """Оnправляет сообщение в бот"""
    bot.send_message(chat_id=CHANNEL_ID, text=message)


def main():
    """Основная логика работы бота."""
    while True:
        values = get_sheet_data(SPREADSHEET_ID)
        last_news_from_db = get_last_news_from_db()
        last_news_list = get_new_news(last_news_from_db, values)
        bot = Bot(token=SECRET_TOKEN)
        messages = list_messages(last_news_list)
        for message in messages:
            send_news(bot, message)
            time.sleep(RETRY_PERIOD)
        update_news_in_bd(last_news_from_db[0], last_news_list)
        time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
