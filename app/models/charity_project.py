from sqlalchemy import Column, String, Text

from app.models.investment_base import InvestmentBase


class CharityProject(InvestmentBase):
    name = Column(String(100), unique=True, nullable=False)
    description = Column(Text, nullable=False)

    def __repr__(self):
        return (f'<CharityProject(name="{self.name}", '
                f'description="{self.description}", ' +
                super().__repr__())
