from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.crud.base import CRUDBase
from app.models import CharityProject


class CharityProjectCRUD(CRUDBase):

    async def get_project_by_name(
            self,
            name: str,
            session: AsyncSession
    ):
        project = await session.scalars(
            select(self.model).where(self.model.name == name)
        )
        return project.first()

    async def get_projects_by_completion_rate(
            self,
            session: AsyncSession
    ):
        projects = await session.scalars(
            select(CharityProject).where(CharityProject.fully_invested == True) # noqa
        )
        projects = projects.all()
        sorted_projects = sorted(
            projects,
            key=lambda project: project.close_date - project.create_date
        )
        return sorted_projects


charityproject_crud = CharityProjectCRUD(CharityProject)
