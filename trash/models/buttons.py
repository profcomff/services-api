from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from trash.models.categories import Category


class Button(declarative_base()):
    __tablename__ = 'buttons'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey(Category.id))
    icon = Column(String)

    def __repr__(self):
        return f'Кнопка {self.name} (id: {self.id}):\n'\
               f'Находится в категории {self.category_id}\n' \
               f'Иконка: {self.icon}'
