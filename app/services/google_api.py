from aiogoogle import Aiogoogle

from app.core.config import settings
from app.services import constants as const


async def spreadsheets_create(wrapper_services: Aiogoogle) -> str:
    service = await wrapper_services.discover('sheets', const.SHEETS_VERSION)
    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=const.SPREADSHEET_BODY)
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
    service = await wrapper_services.discover('sheets', const.SHEETS_VERSION)
    table_values = [
        *const.HEADER_TABLE_VALUES,
        *[[
            project.name,
            str(project.close_date - project.create_date),
            project.description] for project in projects],
    ]
    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    table_length = len(table_values)
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{table_length}C3',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
