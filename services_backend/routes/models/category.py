from .base import Base
from .button import ButtonGet


class CategoryCreate(Base):
    type: str | None
    name: str | None


class CategoryUpdate(Base):
    type: str | None
    name: str | None


class CategoryGet(Base):
    id: int
    type: str | None
    name: str | None
    button: list[ButtonGet]

