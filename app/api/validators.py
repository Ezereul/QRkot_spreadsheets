from fastapi import HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.charityproject import charityproject_crud
from app.models import CharityProject
from app.schemas.charity_project import CharityProjectUpdate


async def check_charity_project_duplicate(
        project_name: str,
        session: AsyncSession
):
    charity_project = await charityproject_crud.get_project_by_name(
        project_name, session)
    if charity_project is not None:
        raise HTTPException(
            status_code=400,
            detail='Проект с таким именем уже существует!'
        )


async def check_charity_project_exists(
        project_id: int,
        session: AsyncSession
) -> CharityProject:
    charity_project = await charityproject_crud.get(project_id, session)

    if not charity_project:
        raise HTTPException(
            status_code=404, detail='Проект не найден.')

    return charity_project


def check_charity_project_deletable(
        charity_project: CharityProject,
):
    if charity_project.invested_amount > 0:
        raise HTTPException(
            status_code=400,
            detail='В проект были внесены средства, не подлежит удалению!'
        )


def check_charity_project_before_edit(
        charity_project: CharityProject,
        obj_in: CharityProjectUpdate,
):
    if (obj_in.full_amount and
            obj_in.full_amount < charity_project.invested_amount):
        raise HTTPException(
            status_code=422,
            detail='Требуемая сумма не может быть меньше уже внесенной'
        )
    if charity_project.fully_invested:
        raise HTTPException(
            status_code=400,
            detail='Закрытый проект нельзя редактировать!'
        )
