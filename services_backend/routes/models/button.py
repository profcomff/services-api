from pydantic import Field

from ...models.database import Type
from .base import Base


class ButtonCreate(Base):
    icon: str = Field(description='Иконка кнопки')
    name: str = Field(description='Название кнопки')
    link: str = Field(description='Ссылка, на которую перенаправляет кнопка')
    type: Type = Field(description='Тип открываемой ссылки')


class ButtonUpdate(Base):
    category_id: int | None
    icon: str | None
    name: str | None
    order: int | None
    link: str | None
    type: str | None


class ButtonGet(Base):
    id: int
    order: int
    icon: str | None
    name: str | None
    link: str | None
    type: str | None
