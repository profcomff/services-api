from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from .base import Base


class Category(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)
    button = relationship("Button", back_populates="category", foreign_keys="Button.category_id")


class Button(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey(Category.id))
    category = relationship("Category", back_populates="button", foreign_keys=[category_id])
    icon = Column(String)
