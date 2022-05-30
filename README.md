# Google_sheet_checker
##### Позволит отслеживать актуальность заказов и цен в таблицах гугл.
### Quick Start:
#### 1) Создаем проект в [GOOGLE CONSOLE](https://console.cloud.google.com/ "Я ссылка"):
#### 2) В поиске Google Console пишем "Google Sheets API", включаем API для этого приложения
#### 3) На панели слева жмем Credentials -> в открывшемся окне жмем Creacte Credentials -> OAuth Client ID.
#### 4) Выбираем "Web applications", обязательно записываем ip на котором будете запускать проект в разделе "Authorized redirect URIs", в моем случае это 'http://localhost' и 'http://127.0.0.1'.
#### 5) На странице созданного клиента 'OAuth Client' скачиваем client-secret JSON файл, переименовываем его в 'credentials.json' и закидываем с заменой в корень проекта.
#### 6) Запускаем скрипт из корня проекта , создаст вам ключ-файл 'token.json'.
```sh
python3 quickstart.py
```
### 7) ОБЯЗАТЕЛЬНО Переименуйте файл '.env.example' в '.env'
### 8) Запускаем сборку образов
```sh
docker-compose up -d --build --force-recreate
```
### 9) Сделаем миграции что бы создалась таблица в БД PostgreSQL
```
docker-compose exec backend python manage.py migrate
```
### 10) Узнаем id контейнера(столбец CONTAINER ID) 'goo_sheet-main_backend' выполнив команду:
P.s id контейнера имеет вид: 95f7b20c3cb4
```
docker container ls
```
### 11) Запустим фоновое выполнение задач:
```
docker exec -it -d "сюда id контейнера goo_sheet-main_backend без кавычек" celery -A google_service worker -l info
```
# Панель запуска доступна по адресу http://localhost:8000/

### В google sheets должна быть хотя бы 1 валидная строка для обновления информации в базе.
### Обновления безы продолжатся как только появится валидная строка
### Строка или строки считаются не валидными если хотя бы одно поле не заполнено или имеют не верное значение
### Не валидная строка удаляется из базы, пока не станет валидной

## Доп.информация:


Технологии:
Django 3
Nginx
Gunicorn
Celery
Redis
Flower
Docker
Telegram Bot
Python 3.8
PostgreSQL

[![Build Status](https://travis-ci.org/joemccann/dillinger.svg?branch=master)](https://travis-ci.org/joemccann/dillinger)
