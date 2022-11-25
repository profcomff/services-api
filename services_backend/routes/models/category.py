from .base import Base
from typing import Optional


class CategoryCreate(Base):
    category_id: int
    type: Optional[str]
    name: Optional[str]


class CategoryUpdate(Base):
    id: int
    category_id: Optional[int]
    type: Optional[str]
    name: Optional[str]


class CategoryGet(Base):
    id: int

