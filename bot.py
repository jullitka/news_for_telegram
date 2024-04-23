import logging
import sys
import time

from telegram import Bot

from google_client import get_sheet_data
from db import add_news, create_db, get_last_news_from_db, update_table
from settings import CHANNEL_ID, SECRET_TOKEN, RETRY_PERIOD, SPREADSHEET_ID
from utils import string_to_date


handler = logging.FileHandler(filename='main.log', encoding='utf-8')
logging.basicConfig(
    handlers=(handler,),
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(stream=sys.stdout)
logger.addHandler(handler)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)


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
                logger.info(f'Неопубликованная новость: {row}')
        else:
            break
    return last_news_list[::-1]


def update_news_in_bd(old_date_time, last_news_list):
    """Обновляет последнюю новость в бд"""
    if last_news_list:
        last_news = last_news_list[-1]
        update_table(old_date_time, last_news[0], last_news[1],
                     last_news[2], last_news[3], last_news[4], last_news[5])
        logger.info('Обновлена последняя новость в бд')


def list_messages(last_news_list):
    """Получает список неопубликованных новостей
    и возвращает сообщения, которые должен отправть бот"""
    messages = []
    for news in last_news_list:
        message = f'<b>{news[1]}</b>\n{news[2]}\n{news[4]}'
        logger.info(f'Сообщение к отправке: {message}')
        messages.append(message)
    return messages


def send_news(bot, message):
    """Оnправляет сообщение в бот"""
    bot.send_message(chat_id=CHANNEL_ID, text=message, parse_mode='HTML')
    logger.info('Сообщение отправлено')


def main():
    """Основная логика работы бота."""
    while True:
        try:
            values = get_sheet_data(SPREADSHEET_ID)
            create_db()

            last_news_from_db = get_last_news_from_db()
            # если в базе не записана последняя новость, то записываем
            if not last_news_from_db:
                last_news_list = []
                last_news = values[-1]
                add_news(last_news[0], last_news[1], last_news[2],
                         last_news[3], last_news[4], last_news[5])
                logger.info('Последняя новость добавлена в базу')
            # если записана, то получаем список новых новостей
            else:
                last_news_list = get_new_news(last_news_from_db, values)

            # если они есть, то бот отправит их в канал и обновит в бд
            if last_news_list:
                bot = Bot(token=SECRET_TOKEN)
                messages = list_messages(last_news_list)
                for message in messages:
                    send_news(bot, message)
                    time.sleep(RETRY_PERIOD)
                update_news_in_bd(last_news_from_db[0], last_news_list)
        except Exception as error:
            message = f'Сбой в работе программы: {error}'
            logger.error(message)
        finally:
            time.sleep(RETRY_PERIOD)


if __name__ == '__main__':
    main()
