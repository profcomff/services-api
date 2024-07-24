# services-api

Ссылки: 

1) Backend разработка – https://docs.profcomff.com/tvoy-ff/backend/index.html


Для запуска проекта нужно иметь доступ к БД профкома/иметь локальную БД. 

Локальную БД можно поднять так:
- Установить Docker
- В терминале запустить: ```docker run -d -p 5432:5432 -e POSTGRES_HOST_AUTH_METHOD=trust --name db-services-backend postgres:15```


Переменные:
1) DB_DSN = 'postgres://логин:пароль@адрес:порт/бд'
