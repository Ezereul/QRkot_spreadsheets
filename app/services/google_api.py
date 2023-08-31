from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings


FORMAT = "%Y/%m/%d %H:%M:%S"
ROW_COUNT = 100
COLUMN_COUNT = 11
SPREADSHEET_TEMPLATE = dict(
    properties=dict(
        title='',
        locale='ru_RU',
    ),
    sheets=[dict(properties=dict(
        sheetType='GRID',
        sheetId=0,
        title='Лист1',
        gridProperties=dict(
            rowCount=ROW_COUNT,
            columnCount=COLUMN_COUNT,
        )
    ))]
)
TABLE_HEAD = [
    ['Отчет от', ''],
    ['Топ проектов по скорости закрытия'],
    ['Название проекта', 'Время сбора', 'Описание']
]


async def spreadsheets_create(wrapper_services: Aiogoogle, template=None) -> str:
    if template is None:
        template = SPREADSHEET_TEMPLATE
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = deepcopy(template)
    spreadsheet_body['properties']['title'] = f'Отчет от {now_date_time}'

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response['spreadsheetId']
    return spreadsheet_id


async def set_user_permissions(
        spreadsheet_id: str,
        wrapper_services: Aiogoogle
) -> None:
    permissions_body = {
        'type': 'user',
        'role': 'writer',
        'emailAddress': settings.email
    }
    service = await wrapper_services.discover('drive', 'v3')
    await wrapper_services.as_service_account(
        service.permissions.create(
            fileId=spreadsheet_id,
            json=permissions_body,
            fields='id'
        )
    )


async def spreadsheets_update_value(
        spreadsheet_id: str,
        projects: list,
        wrapper_services: Aiogoogle
) -> None:
    now_date_time = datetime.now().strftime(FORMAT)
    service = await wrapper_services.discover('sheets', 'v4')
    head = deepcopy(TABLE_HEAD)
    head[0][1] = now_date_time
    table_values = [
        *head,
        *[list(map(str, project.values())) for project in projects]
    ]
    num_rows = len(table_values)
    num_columns = max(map(len, table_values))

    if num_rows > ROW_COUNT or num_columns > COLUMN_COUNT:
        raise ValueError

    update_body = {
        'majorDimension': 'ROWS',
        'values': table_values
    }
    await wrapper_services.as_service_account(
        service.spreadsheets.values.update(
            spreadsheetId=spreadsheet_id,
            range=f'R1C1:R{num_rows}C{num_columns}',
            valueInputOption='USER_ENTERED',
            json=update_body
        )
    )
