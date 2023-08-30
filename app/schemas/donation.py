from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra


class DonationBase(BaseModel):
    full_amount: int = Field(..., gt=0)
    comment: Optional[str] = None

    class Config:
        extra = Extra.forbid


class DonationCreate(DonationBase):
    pass


class DonationUser(DonationBase):
    id: int
    create_date: datetime

    class Config:
        orm_mode = True


class DonationDB(DonationUser):
    user_id: int
    invested_amount: int
    fully_invested: bool
    close_date: Optional[datetime]
