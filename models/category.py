from sqlalchemy import Column, String, Integer
from sqlalchemy.orm import relationship
from models.database import Base


class Category(Base):
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    type = Column(String)

    def __repr__(self):
        return f'Категория {self.name}. Тип: {self.type}'

    def give_id(self):  # Небольшой костыль :)
        return self.id
