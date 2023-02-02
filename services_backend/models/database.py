from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey, PickleType
from sqlalchemy.orm import relationship, Mapped, mapped_column
from .base import Base


class Category(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    order: Mapped[int] = mapped_column(Integer)
    name: Mapped[str] = mapped_column(String)
    type: Mapped[str] = mapped_column(String)
    buttons: Mapped[Button] = relationship("Button", back_populates="category", foreign_keys="Button.category_id")


class Button(Base):
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    order: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey(Category.id))
    category: Mapped[Category] = relationship("Category", back_populates="buttons", foreign_keys=[category_id])
    icon: Mapped[str] = mapped_column(String)
    link: Mapped[dict] = mapped_column(PickleType)
