from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base


class Category(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order: Mapped[int] = mapped_column(Integer, default=1)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    buttons: Mapped[list[Button]] = relationship("Button", back_populates="category", foreign_keys="Button.category_id")


class Button(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    order: Mapped[int] = mapped_column(Integer, default=1)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey(Category.id))
    category: Mapped[Category] = relationship("Category", back_populates="buttons", foreign_keys=[category_id])
    icon: Mapped[str] = mapped_column(String)
    link: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)

