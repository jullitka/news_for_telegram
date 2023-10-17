import sqlite3


def create_db():
    """Создает таблицу, если ее еще нет"""
    conn = sqlite3.connect('from_google.db')
    cur = conn.cursor()
    cur.execute("""CREATE TABLE IF NOT EXISTS from_google(
        date_time VARCHAR PRIMARY KEY UNIQUE NOT NULL,
        heading VARCHAR,
        text TEXT,
        type_news VARCHAR(100),
        link VARCHAR,
        tag VARCHAR
        );""")


def add_news(date_time, heading, text, type, link):
    """Добавляет последнюю строку google-таблицы в таблицу"""
    conn = sqlite3.connect('from_google.db')
    cur = conn.cursor()
    cur.execute("""INSERT INTO from_google
                (date_time, heading,
                 text, type_news, link)
                VALUES(?, ?, ?, ?, ?);""",
                (date_time, heading, text, type, link))
    conn.commit()


def update_table(old_date_time, date_time, heading, text, type, link):
    """Заменяет информацию о последней записи"""
    conn = sqlite3.connect('from_google.db')
    cur = conn.cursor()
    cur.execute("""UPDATE from_google SET
                date_time = ?, heading = ?,
                text = ?, type_news = ?, link = ?
                WHERE date_time = ?;""",
                (date_time, heading, text, type, link, old_date_time))
    conn.commit()


def get_last_news_from_db():
    """Возвращает последнюю новость из таблицы в базе """
    conn = sqlite3.connect('from_google.db')
    cur = conn.cursor()
    cur.execute("""SELECT * FROM from_google
                ORDER BY date_time DESC
                LIMIT 1""")
    last_news = cur.fetchone()
    return last_news
