from datetime import datetime

# services.google_api
FORMAT = "%Y/%m/%d %H:%M:%S"
DRIVE_VERSION = 'v3'
SHEETS_VERSION = 'v4'
ROW_COUNT = 100
COLUMN_COUNT = 10
SHEET_ID = 0

# core.users
JWT_LIFE_TIME = 60 * 60

GOOGLE_API_EXAMPLE = 'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'

# summary for endpoints in api.charity_projects
GET_ALL_CHARITY_PROJECTS = 'Список всех проектов'
CREATE_CHARITY_PROJECTS = 'Создать проект'
UPDATE_CHARITY_PROJECT = 'Редактировать проект'
DELETE_CHARITY_PROJECTS = 'Удалить проект'

# summary for endpoints in api.donations
GET_ALL_DONATIONS = 'Список пожертвований'
CREATE_DONATION = 'Создать пожертвование'
GET_MY_DONATIONS = 'Список пожертвований текущего пользователя'

# summary for endpoints in api.google
GET_GOOGLE_REPORT = 'Создать отчет по проектам'

# error messages
ERR_LEN_PASSWORD = 'Password should be at least 3 characters'
ERR_EMAIL_IN_PASSWORD = 'Пароль содержит ваш e-mail'
ERR_NOT_FOUND = 'Проекта с id %s не существует'
ERR_NAME_EXIST = 'Проект с таким именем уже существует!'
ERR_HAS_INVEST = 'В проект были внесены средства, не подлежит удалению!'
ERR_PROJECT_CLOSED = 'Закрытый проект нельзя редактировать!'
ERR_FULL_AMOUNT = 'Нельзя установить требуемую cумму меньше уже вложенной'
ERR_DONT_DELETE_USER = 'Удаление пользователей запрещено!'

NOW_DATE_TIME = datetime.now().strftime(FORMAT)
SPREADSHEET_BODY = {
    'properties': {
        'title': f'Отчет на {NOW_DATE_TIME}',
        'locale': 'ru_RU'},
    'sheets': [
        {
            'properties': {
                'sheetType': 'GRID',
                'sheetId': SHEET_ID,
                'title': 'Рейтинг проектов по скорости сбора средств',
                'gridProperties': {
                    'rowCount': ROW_COUNT,
                    'columnCount': COLUMN_COUNT
                }
            }
        }
    ]
}
HEADER_TABLE_VALUES = [
    ['Отчет от', NOW_DATE_TIME],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]
