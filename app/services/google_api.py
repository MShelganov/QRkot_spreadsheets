from datetime import datetime

from aiogoogle import Aiogoogle

from app.core.config import settings
from app.services import constants as const


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    now_date_time = datetime.now().strftime(const.FORMAT)
    service = await wrapper_services.discover('sheets', const.SHEETS_VERSION)
    spreadsheet_body = {
        'properties': {
            'title': f'Отчет на {now_date_time}',
            'locale': 'ru_RU'},
        'sheets': [
            {
                'properties': {
                    'sheetType': 'GRID',
                    'sheetId': const.SHEET_ID,
                    'title': 'Рейтинг проектов по скорости сбора средств',
                    'gridProperties': {
                        'rowCount': const.ROW_COUNT,
                        'columnCount': const.COLUMN_COUNT
                    }
                }
            }
        ]
    }
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    return response['spreadsheetId']


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email,

    }
    service = await wrapper_services.discover('drive', const.DRIVE_VERSION)
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id',
            sendNotificationEmail=False,
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
):
    now_date_time = datetime.now().strftime(const.FORMAT)
    service = await wrapper_services.discover('sheets', const.SHEETS_VERSION)
    table_values = [
        ['Отчет от', now_date_time],
        ['Топ проектов по скорости закрытия'],
        ['Название проекта', 'Время сбора', 'Описание']
    ]
    for project in projects:
        table_values.append([
            project.name,
            str(project.close_date - project.create_date),
            project.description
        ])

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    table_length = len(table_values)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'A1:C{table_length}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
