from copy import deepcopy
from datetime import datetime

from aiogoogle import Aiogoogle
from app.core.config import settings
from app.services.exceptions import SpreadsheetSizeExceededError

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


async def spreadsheets_create(
        wrapper_services: Aiogoogle,
        template=None) -> tuple[str, str]:
    if template is None:
        template = SPREADSHEET_TEMPLATE
    service = await wrapper_services.discover('sheets', 'v4')
    spreadsheet_body = deepcopy(template)
    spreadsheet_body['properties']['title'] = (
        f'Отчет от {datetime.now().strftime(FORMAT)}')

    response = await wrapper_services.as_service_account(
        service.spreadsheets.create(json=spreadsheet_body)
    )
    spreadsheet_id = response.get('spreadsheetId')
    url = response.get('spreadsheetUrl')
    return spreadsheet_id, url


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
    formatted_projects = [
        {
            "name": project.name,
            "duration": str(project.close_date - project.create_date),
            "description": project.description
        }
        for project in sorted(
            projects,
            key=lambda project: project.close_date - project.create_date
        )
    ]

    service = await wrapper_services.discover('sheets', 'v4')
    head = deepcopy(TABLE_HEAD)
    head[0][1] = datetime.now().strftime(FORMAT)
    table_values = [
        *head,
        *[list(map(str, project.values())) for project in formatted_projects]
    ]
    num_rows = len(table_values)
    num_columns = max(map(len, table_values))

    if num_rows > ROW_COUNT or num_columns > COLUMN_COUNT:
        raise SpreadsheetSizeExceededError(
            f"Rows: {num_rows}/{ROW_COUNT},"
            f" Cols: {num_columns}/{COLUMN_COUNT}")

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
