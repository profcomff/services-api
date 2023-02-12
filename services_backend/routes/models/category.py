from .base import Base
from .button import ButtonGet


class CategoryCreate(Base):
    type: str | None
    name: str | None


class CategoryUpdate(Base):
    type: str | None
    name: str | None
    order: int | None


class CategoryGet(Base):
    id: int
    order: int
    type: str | None
    name: str | None
    buttons: list[ButtonGet] | None
