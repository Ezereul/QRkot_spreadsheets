from aiogoogle import Aiogoogle
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.db import get_async_session
from app.core.google_client import get_service
from app.core.user import current_superuser
from app.crud.charityproject import charityproject_crud
from app.services.google_api import (
    spreadsheets_create, set_user_permissions, spreadsheets_update_value
)
from app.services.project_sorting import get_projects_by_completion_rate

router = APIRouter()


@router.post(
    '/',
    dependencies=[Depends(current_superuser)]
)
async def get_report(
        session: AsyncSession = Depends(get_async_session),
        wrapper_services: Aiogoogle = Depends(get_service)
) -> str:
    """Только для суперюзеров."""
    projects = await charityproject_crud.get_closed(session)
    formatted_projects = await get_projects_by_completion_rate(projects)

    spreadsheet_id = await spreadsheets_create(wrapper_services)
    await set_user_permissions(spreadsheet_id, wrapper_services)
    try:
        await spreadsheets_update_value(
            spreadsheet_id, formatted_projects, wrapper_services)
    except ValueError:
        raise HTTPException(status_code=400, detail='Слишком много данных')
    except Exception:
        raise HTTPException(status_code=500, detail='Unexpected error.')

    return f'https://docs.google.com/spreadsheets/d/{spreadsheet_id}'
