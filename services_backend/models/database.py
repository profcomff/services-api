from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base


class Scope(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    read_scope: Mapped[str] = mapped_column(String, nullable=False)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey(Category.id))
    category: Mapped[list[Category]] = relationship("Category", back_populates="Category.read_scope", foreign_keys=category_id)


class Category(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order: Mapped[int] = mapped_column(Integer, default=1)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    read_scope: Mapped[str] = mapped_column(String, ForeignKey(Scope.read_scope))
    buttons: Mapped[list[Button]] = relationship("Button", back_populates="category", foreign_keys="Button.category_id")
    scopes: Mapped[list[Scope]] = relationship("scopes", back_populates="category", foreign_keys=read_scope)


class Button(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    order: Mapped[int] = mapped_column(Integer, default=1)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey(Category.id))
    category: Mapped[Category] = relationship("Category", back_populates="buttons", foreign_keys=[category_id])
    icon: Mapped[str] = mapped_column(String)
    link: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
