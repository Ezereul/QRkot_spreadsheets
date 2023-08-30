from sqlalchemy import ForeignKey, Column, Integer, Text

from app.models.investment_base import InvestmentBase


class Donation(InvestmentBase):
    user_id = Column(Integer, ForeignKey('user.id'))
    comment = Column(Text)

    def __repr__(self):
        return (f'<Donation(user_id={self.user_id}, '
                f'comment="{self.comment}", ' +
                super().__repr__())
