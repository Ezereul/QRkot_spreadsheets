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


charityproject_crud = CharityProjectCRUD(CharityProject)
