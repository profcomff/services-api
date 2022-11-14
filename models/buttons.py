from sqlalchemy import Column, Integer, String, ForeignKey
from models.database import Base


class Button(Base):
    __tablename__ = 'buttons'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    category_id = Column(Integer, ForeignKey("category.category_id"))
    icon = Column(String)

    # category = relationship("Category", back_populates="category")

    def __init__(self, id: int, name: str, category_id: int, icon: dict):
        self.id = id
        self.name = name
        self.category_id = category_id
        self.icon = icon["src"]

    def __repr__(self):
        info: str = f'Кнопка {self.name} (id: {self.id}):\n'\
                    f'Находится в категории {self.category_id}\n' \
                    f'Иконка: {self.icon}'

        return info
