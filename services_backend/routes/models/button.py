from .base import Base
from typing import Optional


class ButtonCreate(Base):
    category_id: int
    icon: Optional[str]
    name: Optional[str]


class ButtonUpdate(Base):
    id: int
    category_id: Optional[int]
    icon: Optional[str]
    name: Optional[str]


class ButtonGet(Base):  
    id: int
    category_id: int
    icon: Optional[str]
    name: Optional[str]
