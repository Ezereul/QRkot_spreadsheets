from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.api.validators import (
    check_charity_project_exists, check_charity_project_deletable,
    check_charity_project_before_edit, check_charity_project_duplicate
)
from app.core.db import get_async_session
from app.core.user import current_superuser
from app.crud.charityproject import charityproject_crud
from app.crud.donation import donation_crud
from app.schemas.charity_project import (
    CharityProjectDB, CharityProjectUpdate, CharityProjectCreate
)
from app.services.investing import distribute_investment


router = APIRouter()


@router.get('/',
            response_model=List[CharityProjectDB],
            response_model_exclude_none=True)
async def get_all_charity_projects(
        session: AsyncSession = Depends(get_async_session)):
    return await charityproject_crud.get_multi(session)


@router.delete('/{project_id}',
               response_model=CharityProjectDB,
               dependencies=[Depends(current_superuser)])
async def delete_charity_project(
        project_id: int,
        session: AsyncSession = Depends(get_async_session),
):
    charity_project = await check_charity_project_exists(project_id, session)
    check_charity_project_deletable(charity_project)

    return await charityproject_crud.remove(charity_project, session)


@router.post('/',
             response_model=CharityProjectDB,
             dependencies=[Depends(current_superuser)],
             response_model_exclude_none=True)
async def create_charity_project(
        obj_in: CharityProjectCreate,
        session: AsyncSession = Depends(get_async_session)
):
    await check_charity_project_duplicate(obj_in.name, session)

    charity_project = await charityproject_crud.create(
        obj_in, session, to_commit=False)

    session.add_all(
        distribute_investment(
            charity_project,
            await donation_crud.get_open(session)
        )
    )
    await session.commit()
    await session.refresh(charity_project)
    return charity_project


@router.patch('/{project_id}',
              response_model=CharityProjectDB,
              dependencies=[Depends(current_superuser)])
async def update_charity_project(
        project_id: int,
        obj_in: CharityProjectUpdate,
        session: AsyncSession = Depends(get_async_session)
):
    charity_project = await check_charity_project_exists(project_id, session)
    await check_charity_project_duplicate(obj_in.name, session)
    check_charity_project_before_edit(charity_project, obj_in)
    charity_project = await charityproject_crud.update(
        charity_project, obj_in, session)

    return charity_project
