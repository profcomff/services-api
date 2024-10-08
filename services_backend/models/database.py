from __future__ import annotations

import logging
from enum import Enum

from fastapi_sqlalchemy import db
from sqlalchemy import Boolean
from sqlalchemy import Enum as DbEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.ext.hybrid import hybrid_property
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


logger = logging.getLogger(__name__)


class Category(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order: Mapped[int] = mapped_column(Integer, default=1)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    buttons: Mapped[list[Button]] = relationship(
        "Button", back_populates="category", foreign_keys="Button.category_id", order_by='Button.order'
    )

    _scopes: Mapped[list[Scope]] = relationship("Scope", back_populates="category", lazy='joined', cascade='delete')

    @hybrid_property
    def scopes(self) -> set[str]:
        return set(s.name for s in self._scopes)

    @scopes.inplace.setter
    def _scopes_setter(self, value: set[str]):
        old_scopes = self.scopes
        new_scopes = set(value)

        # Удаляем более ненужные скоупы
        for s in self._scopes:
            if s.name in (old_scopes - new_scopes):
                db.session.delete(s)

        # Добавляем недостающие скоупы
        for s in new_scopes - old_scopes:
            new_scope = Scope(category=self, name=s)
            db.session.add(new_scope)
            self._scopes.append(new_scope)


class Type(str, Enum):
    INAPP: str = "inapp"
    INTERNAL: str = "internal"
    EXTERNAL: str = "external"


class Button(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    order: Mapped[int] = mapped_column(Integer, default=1)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey(Category.id))
    category: Mapped[Category] = relationship("Category", back_populates="buttons", foreign_keys=[category_id])
    icon: Mapped[str] = mapped_column(String)
    link: Mapped[str] = mapped_column(String)
    type: Mapped[Type] = mapped_column(DbEnum(Type, native_enum=False), nullable=False)
    is_hidden: Mapped[bool] = mapped_column(Boolean, default=False)

    _scopes: Mapped[list[Scope]] = relationship("Scope", back_populates="button", lazy='joined', cascade='delete')

    @hybrid_property
    def required_scopes(self) -> set[str]:
        return set(s.name for s in self._scopes if s.is_required is True)

    @required_scopes.inplace.setter
    def _required_scopes_setter(self, value: set[str]):
        old_scopes = self.required_scopes
        new_scopes = set(value)

        # Удаляем более ненужные скоупы
        for s in self._scopes:
            if s.name in (old_scopes - new_scopes):
                db.session.delete(s)

        # Добавляем недостающие скоупы
        for s in new_scopes - old_scopes:
            new_scope = Scope(button=self, name=s, is_required=True)
            db.session.add(new_scope)
            self._scopes.append(new_scope)

    @hybrid_property
    def optional_scopes(self) -> set[str]:
        return set(s.name for s in self._scopes if s.is_required is False)

    @optional_scopes.inplace.setter
    def _optional_scopes_setter(self, value: set[str]):
        old_scopes = self.optional_scopes
        new_scopes = set(value)

        # Удаляем более ненужные скоупы
        for s in self._scopes:
            if s.name in (old_scopes - new_scopes):
                db.session.delete(s)

        # Добавляем недостающие скоупы
        for s in new_scopes - old_scopes:
            new_scope = Scope(button=self, name=s, is_required=False)
            db.session.add(new_scope)
            self._scopes.append(new_scope)


class Scope(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"), nullable=True)
    button_id: Mapped[int] = mapped_column(Integer, ForeignKey("button.id"), nullable=True)
    is_required: Mapped[bool] = mapped_column(Boolean, default=True, nullable=True)
    category: Mapped[Category] = relationship("Category", back_populates="_scopes", foreign_keys=[category_id])
    button: Mapped[Category] = relationship("Button", back_populates="_scopes", foreign_keys=[button_id])
