from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, Extra, validator


class CharityProjectBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    description: str = Field(..., min_length=1)
    full_amount: int = Field(..., gt=0)

    class Config:
        extra = Extra.forbid


class CharityProjectCreate(CharityProjectBase):
    pass


class CharityProjectUpdate(CharityProjectBase):
    name: Optional[str] = Field(None, max_length=100)
    description: Optional[str] = None
    full_amount: Optional[int] = Field(None, gt=0)

    class Config:
        min_anystr_length = 1

    @validator('name')
    def name_cannot_be_null(cls, value):
        if value is None:
            raise ValueError('Имя проекта не может быть пустым')
        return value


class CharityProjectDB(CharityProjectBase):
    id: int
    invested_amount: int
    fully_invested: bool
    create_date: datetime = Field(..., example=datetime.now().strftime('%Y-%m-%dT%H:%M'))
    close_date: Optional[datetime] = None

    class Config:
        orm_mode = True
