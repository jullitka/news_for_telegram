# News for telegram

Телеграм - бот обращается с определенной периодичностью к google-таблице, которая содержит новости для публикации, проверяет, появились ли еще не опубликованные новости, и отправляет их в telegram-канал.

## Стек технологий

[![Python](https://img.shields.io/badge/-Python-blue)](https://www.python.org/)
[![Telegram](https://img.shields.io/badge/-Telegram-blue)](https://docs.python-telegram-bot.org/en/latest/)
[![GoogleAPI](https://img.shields.io/badge/-GoogleAPI-blue)](https://support.google.com/googleapi/?hl=en#topic=7014522)
[![Docker](https://img.shields.io/badge/-Docker-blue)](https://www.docker.com/)

## Запуск проекта

#### Клонировать репозиторий:
```
git clone https://github.com/Jullitk/news_for_telegram.git
```
#### Cоздать и активировать в репозитории виртуальное окружение:
```
python -m venv venv
```
Для Linux
    ```
    source venv/bin/activate
    ```
    
Для Windows
    ```
    source venv/Scripts/activate
    ```
#### Установить зависимости из файла requirements.txt:
```
python -m pip install --upgrade pip
pip install -r requirements.txt
```
#### Создать в корне файл .env и заполнить его по образцу:

(cм. файл env.example)
```
TYPE = ""
PROJECT_ID = ""
PRIVATE_KEY_ID = ""
PRIVATE_KEY = ""
CLIENT_EMAIL = ""
CLIENT_ID = ""
AUTH_URI = ""
TOKEN_URI = ""
AUTH_PROVIDER_X509_CERT_URL = ""
CLIENT_X509_CERT_URL = ""
UNIVERSE_DOMAIN = ""
EMAIL = ""
TOKEN = ""
CHANNEL_ID = ""
SPREADSHEET_ID = ""
```
#### Запустить проект:
```
python bot.py
```
#### Запустить проекта в контейнере

```
docker-compose up --build
```
### Требования к google-таблице

Google-таблица должна быть доступна всем, у кого есть доступ, открыта для редактирования для данного сервисного аккаунта и иметь следующие колонки:
| Дата | Заголовок | Текст | Тип | Ссылка | Тэги |
| :---: | :---: | :---: | :---: | :---: | :---: |
|January 01, 2001 at 01:01PM | | | | | | 
- Все колонки должны быть заполнены
- Дата должна соответствовать следующему формату:
```
%B %d, %Y at %I:%M%p"
```
- Тэги перечисляются через запятую
## Авторы
[Юлия Пашкова](https://github.com/Jullitka)
