<<<<<<< Updated upstream
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
=======
from __future__ import annotations
from sqlalchemy import Integer, String, ForeignKey, PickleType
from sqlalchemy.orm import relationship, Mapped, mapped_column
>>>>>>> Stashed changes
from .base import Base


class Category(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    buttons = relationship("Button", back_populates="category", foreign_keys="Button.category_id")


class Button(Base):
<<<<<<< Updated upstream
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey(Category.id))
    category = relationship("Category", back_populates="buttons", foreign_keys=[category_id])
    icon = Column(String)
=======
    id: Mapped[int] = mapped_column(Integer, primary_key=True)
    name: Mapped[str] = mapped_column(String)
    order: Mapped[int] = mapped_column(Integer)
    category_id: Mapped[int] = mapped_column(Integer, ForeignKey(Category.id))
    category: Mapped[Category] = relationship("Category", back_populates="buttons", foreign_keys=[category_id])
    icon: Mapped[str] = mapped_column(String)
    link: Mapped[dict] = mapped_column(PickleType)
>>>>>>> Stashed changes
