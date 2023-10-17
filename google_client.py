from google.oauth2.service_account import Credentials
from googleapiclient import discovery

from settings import INFO, SCOPES


def auth():
    # Создаём экземпляр класса Credentials
    credentials = Credentials.from_service_account_info(
                  info=INFO, scopes=SCOPES)
    # Создаём экземпляр класса Resource
    service = discovery.build('sheets', 'v4', credentials=credentials)
    return service, credentials


def get_sheet_data(spreadsheet_id, range='Лист1'):
    """Получает данные из google-таблицы.
    Возвращает все записи в указанном диапазоне"""
    result = service.spreadsheets().values().get(
        spreadsheetId=spreadsheet_id,
        range=range
    ).execute()
    values = result.get('values', [])
    if not values:
        print('No data found.')
    return values


service, credentials = auth()
