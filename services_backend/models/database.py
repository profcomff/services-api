from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Category(Base):
    id = Column(Integer, primary_key=True)
    order = Column(Integer)
    name = Column(String)
    type = Column(String)
    buttons = relationship("Button", back_populates="category", foreign_keys="Button.category_id")


class Button(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    order = Column(Integer)
    category_id = Column(Integer, ForeignKey(Category.id))
    category = relationship("Category", back_populates="buttons", foreign_keys=[category_id])
    icon = Column(String)
