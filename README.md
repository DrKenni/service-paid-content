# SVINK

## Описание

Платформа для публикации контента пользователя

## Задача

Реализовать платформу для публикации записей пользователями. Публикация может быть бесплатной, то есть доступной любому
пользователю без регистрации, либо платной, которая доступна только авторизованным пользователям, который оплатили
разовую подписку. Для реализации оплаты подписки используйте Stripe. Регистрация пользователя должна быть по номеру
телефона.

## Технологии

* Python 
* HTML 
* CSS, JS
* PostgreSQL
* Django 
* Redis, Celery

## Зависимости
```
python = "^3.11"
django = "^4.2.7"
psycopg2-binary = "^2.9.9"
pillow = "^10.1.0"
python-dotenv = "^1.0.0"
redis = "^5.0.1"
django-crispy-forms = "^2.1"
crispy-bootstrap5 = "^2023.10"
stripe = "^7.6.0"
celery = "^5.3.6"
coverage = "^7.3.2"
```

## Прежде чем начать использовать проект нужно:
* Установить PostgreSQL и предварительно настроить БД.
* Установить Redis.
* Создать в проекте файл `.evn` и указать нужные данные из файла `.evn.sample`.
## `.evn`
```
# Database
POSTGRES_PASSWORD=
POSTGRES_USER=
POSTGRES_DB=

# Django settings
SECRET_KEY=
DEBUG=

# SMS
SMS_API_ID=

# Stripe
STRIPE_API_KEY=
```
## Инструкция по запуску приложения:
Для запуска проекта необходимо клонировать репозиторий и создать и активировать виртуальное окружение: 
```
poetry shell
```
Установить зависимости:
```
poetry init
```
Выполнить миграции:
```
python manage.py migrate
```

Для создания администратора запустить команду:

```
python manage.py csu
```

Для запуска redis:

```
redis-cli
```

Для запуска celery:

```
celery -A config worker -l info
```
На Windows:
```
celery -A config worker -l info -P eventlet 
```

Для запуска django-celery-beat:

```
celery -A config beat -l info
```

Для запуска приложения:

```
python manage.py runserver
```

_Для тестирования проекта запустить команду:_

```
python manage.py test
```
### Запуск проекта в Docker:

Для создания образа из Dockerfile и запуска контейнера запустить команду:
```
docker-compose up --build -d
```
