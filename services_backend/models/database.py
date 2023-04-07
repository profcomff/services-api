from __future__ import annotations

from enum import Enum
from sqlalchemy import Enum as DbEnum
from sqlalchemy import ForeignKey, Integer, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from .base import Base


class Category(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order: Mapped[int] = mapped_column(Integer, default=1)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    buttons: Mapped[list[Button]] = relationship(
        "Button", back_populates="category", foreign_keys="Button.category_id", order_by='Button.order'
    )
    scopes: Mapped[list[Scope]] = relationship("Scope", back_populates="category")


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


class Scope(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String, nullable=True)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey("category.id"))
    category: Mapped[Category] = relationship("Category", back_populates="scopes", foreign_keys=[category_id])
