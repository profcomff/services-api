from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from sqlalchemy.ext.declarative import declarative_base


class Category(declarative_base()):
    __tablename__ = 'category'

    id = Column('id', Integer, primary_key=True)
    category_id = Column('category_id', Integer, unique=True)
    name = Column('name', String)
    type = Column('type', String)
    # category = relationship("Button", back_populates="category")

    def __repr__(self):
        return f'Категория {self.name}. Тип: {self.type}\n' \
               f'ID: {self.category_id}'

