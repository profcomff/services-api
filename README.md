# services-api

Бэкэнд сервисов приложения Твой ФФ для профкома ФФ МГУ. Реализует логику работы с кнопками и категориями в приложении.
Репозиторий был создан для упрощения работы фронтэнд-разработчиков с бэкэндом сервисов, для переноса данных кнопок и категорий из захардкодженного json файла в Postgresql базу данных (cringe) и для разграничения доступа.

[<img src="https://cdn.profcomff.com/easycode/easycode.svg" width="200"></img>](https://easycode.profcomff.com/templates/docker-fastapi/workspace?mode=manual&param.Repository+URL=https://github.com/profcomff/services-api.git&param.Working+directory=services-api)

## Функционал

- Создание кнопок и категорий для отображения на фронте (в приложении)
- Управление доступами к категориям кнопок
- Редактирование любых атрибутов/полей кнопое и категорий


## Разработка
Backend разработка – https://github.com/profcomff/.github/wiki/%5Bdev%5D-Backend-разработка

CONTRIBUTING.md - [CONTRIBUTING.md](CONTRIBUTING.md)

## Quick Start

1) Перейдите в папку проекта

2) Создайте виртуальное окружение командой:
```console
foo@bar:~$ python3 -m venv ./venv/
```
3) Установите библиотеки
```console
foo@bar:~$ pip install -m requirements.txt
```
4) Установите все переменные окружения (см. CONTRIBUTING.md)

5) Запускайте приложение!
```console
foo@bar:~$ python -m services-backend
```


## Использование
1) Создание категории кнопок
*Необходимо иметь права services.category.create*
    1. Создать новую категорию по запросу `POST /category` с телом `{"name": "имя_категории", "type": "тип отображения категории в приложении"}`

    2. *Необходимо иметь права services.button.create* Создать в категории новую кнопку по запросу `POST /category/id_категории/button` с телом `{"name": "имя кнопки", "icon": "ссылка на иконку", "link": "ссылка сервиса, на которую ведет кнопка", "type": "тип ссылки"}`

    3. *Опционально* Навесить права запросом `POST /category/{category_id}/scope` с телом `{"name": "название права доступа"}`


2) Получение категорий кнопок
*Нет необходимых прав*
    1. Получить категории по запросу `GET /category`
    2. *Опционально* Выбрать отображение кнопок принадлежащих категории по запросу `GET /category?info=buttons`


3) Удаление категории кнопок. *Необходимо иметь права services.category.delete*

    ВАЖНОЕ УТОЧНЕНИЕ: При удалении категории все кнопки, принадлежащей ей также удаляются.
    1. Удалить категорию кнопок по запросу 'DELETE /category/{category_id}

## Параметризация и плагины:
Никаких настроек кроме стандартных нет

## Ссылки:
Документация проекта - https://api.test.profcomff.com/?urls.primaryName=services#

Backend разработка – https://github.com/profcomff/.github/wiki/%5Bdev%5D-Backend-разработка

CONTRIBUTING.md - [CONTRIBUTING.md](CONTRIBUTING.md)
