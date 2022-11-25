from pydantic import BaseModel
from typing import Optional


class Category(BaseModel):
    id: int
    category_id: int
    type: Optional[str]
    name: Optional[str]

    class Config:
        orm_mode = True


class Button(BaseModel):
    id: int
    category_id: int
    name: Optional[str]
    icon: Optional[str]

    class Config:
        orm_mode = True
