from datetime import datetime

from sqlalchemy import Column, Integer, Boolean, DateTime, CheckConstraint

from app.core.db import Base


class InvestmentBase(Base):
    __abstract__ = True
    full_amount = Column(Integer, nullable=False)
    invested_amount = Column(Integer, nullable=False, default=0)
    fully_invested = Column(Boolean, nullable=False, default=False)
    create_date = Column(DateTime, nullable=False,
                         default=datetime.utcnow)
    close_date = Column(DateTime)
    __table_args__ = (
        CheckConstraint('full_amount > 0', name='full_amount_positive'),
        CheckConstraint('invested_amount >= 0',
                        name='invested_amount_positive'),
        CheckConstraint('invested_amount <= full_amount',
                        name='invested_amount_lte_full_amount'),
    )

    def __repr__(self):
        return (f'full_amount={self.full_amount}, '
                f'invested_amount={self.invested_amount}, '
                f'fully_invested={self.fully_invested}), '
                f'create_date={self.create_date}, '
                f'close_date={self.close_date}>')
