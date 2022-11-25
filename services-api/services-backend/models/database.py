from sqlalchemy import Column, Integer, String, ForeignKey
from .base import Base


class Category(Base):
    id = Column(Integer, primary_key=True)
    category_id = Column(Integer, unique=True)
    name = Column(String)
    type = Column(String)
    # category = relationship("Button", back_populates="category")

class Button(Base):
    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey(Category.id))
    icon = Column(String)
