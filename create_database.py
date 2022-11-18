# This Python file uses the following encoding: utf-8

from faker import Faker
from models.buttons import Button
from models.categories import Category
from fastapi import Depends
from __init__ import get_db, Session
import json


def _load_fake_data(session: Session = Depends(get_db)):
    with open('buttons.json', 'r', encoding="utf8") as f:
        data = json.load(f)

    category1 = Category(id=1, category_id=1, name=data[0]['name'], type=data[0]['type'])  # Категория - Полезное
    category2 = Category(id=2, category_id=2, name=data[1]['name'], type=data[1]['type'])  # Категория - Сервисы
    category3 = Category(id=3, category_id=3, name=data[2]['name'], type=data[2]['type'])  # Категория - Информация

    # Категория - Полезное
    button1 = Button(id=1, name=data[0]['items'][0]['text'], icon=data[0]['items'][0]['icon']["src"],  # Полезное
                     category_id=1)
    button2 = Button(id=2, name=data[0]['items'][1]['text'], icon=data[0]['items'][1]['icon']["src"],  # Этажи
                     category_id=1)

    # Категория - Сервисы
    button3 = Button(id=3, name=data[1]['items'][0]['text'], icon=data[1]['items'][0]['icon']["src"],  # Написать
                     category_id=2)
    button4 = Button(id=4, name=data[1]['items'][1]['text'], icon=data[1]['items'][1]['icon']["src"],  # Учебная часть
                     category_id=2)
    button5 = Button(id=5, name=data[1]['items'][2]['text'], icon=data[1]['items'][2]['icon']["src"],  # МФК
                     category_id=2)
    button6 = Button(id=6, name=data[1]['items'][3]['text'], icon=data[1]['items'][3]['icon']["src"],  # Жалоба
                     category_id=2)
    button7 = Button(id=7, name=data[1]['items'][4]['text'], icon=data[1]['items'][4]['icon']["src"],  # Мат. помощь
                     category_id=2)
    button8 = Button(id=8, name=data[1]['items'][5]['text'], icon=data[1]['items'][5]['icon']["src"],  # Профсоюз
                     category_id=2)

    # Категория - Информация
    button9 = Button(id=9, name=data[2]['items'][0]['text'], icon=data[2]['items'][0]['icon']["src"],  # Приложение
                     category_id=3)
    button10 = Button(id=10, name=data[2]['items'][1]['text'], icon=data[2]['items'][1]['icon']["src"],  # Обратная связь
                      category_id=3)
    button11 = Button(id=11, name=data[2]['items'][2]['text'], icon=data[2]['items'][2]['icon']["src"],  # О приложении
                      category_id=3)

    faker = Faker('ru_RU')

    session.add(category1)
    session.add(category2)
    session.add(category3)
    session.add(button1)
    session.add(button2)
    session.add(button3)
    session.add(button4)
    session.add(button5)
    session.add(button6)
    session.add(button7)
    session.add(button8)
    session.add(button9)
    session.add(button10)
    session.add(button11)

    session.commit()


_load_fake_data(Session())
