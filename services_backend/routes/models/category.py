from .base import Base
from typing import Optional


class CategoryCreate(Base):
    type: Optional[str]
    name: Optional[str]


class CategoryUpdate(Base):
    id: int
    type: Optional[str]
    name: Optional[str]


class CategoryGet(Base):
    id: int
    type: Optional[str]
    name: Optional[str]

