from pydantic import Field

from ...models.database import Type
from .base import Base


class ButtonCreate(Base):
    icon: str = Field(description='Иконка кнопки')
    name: str = Field(description='Название кнопки')
    link: str = Field(description='Ссылка, на которую перенаправляет кнопка')
    type: Type = Field(description='Тип открываемой ссылки (Ссылка приложения/Браузер в приложении/Браузер')


class ButtonUpdate(Base):
    category_id: int | None = Field(description='Айди категории')
    icon: str | None = Field(description='Иконка кнопки')
    name: str | None = Field(description='Название кнопки')
    order: int | None = Field(description='Порядок, в котором отображаются кнопки')
    link: str | None = Field(description='Ссылка, на которую перенаправляет кнопка')
    type: str | None = Field(description='Тип открываемой ссылки (Ссылка приложения/Браузер в приложении/Браузер')


class ButtonGet(Base):
    id: int = Field(description='Айди кнопки')
    order: int = Field(description='Порядок, в котором отображаются кнопки')
    icon: str | None = Field(description='Иконка кнопки')
    name: str | None = Field(description='Название кнопки')
    link: str | None = Field(description='Ссылка, на которую перенаправляет кнопка')
    type: str | None = Field(description='Тип открываемой ссылки (Ссылка приложения/Браузер в приложении/Браузер')
