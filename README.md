# Проект API YaMDb CI/CD

### Описание проекта
Проект YaMDb собирает отзывы пользователей и рейтинги произведений искусства. Произведение может иметь несколько жанров и одну категорию. Вы можете оставлять комментарии к отзывам. В проекте действует система модерации контента.

[![](https://github.com/fairsk/api_yamdb/actions/workflows/yamdb_workflow.yml/badge.svg)](https://github.com/fairsk/api_yamdb/actions/workflows/yamdb_workflow.yml)

### Как запустить проект:
Склонируйте репозиторию:

```
git@github.com:FairSk/yamdb_final.git
```

Перейдите в папку с файлом Dockerfile:

```
cd yamdb_final/api_yamdb
```

Создайте образ проекта:

```
docker build -t yamdb .
```

Запустите docker-compose:

```
docker-compose up -d --build 
```

Сделайте миграции:
```
docker-compose exec web python manage.py migrate
```

Создайте суперпользователя и проследуйте инструкциям в терминале:
```
docker-compose exec web python manage.py createsuperuser
```

Соберите статику:
```
docker-compose exec web python manage.py collectstatic --no-input 
```

### Шаблон наполнения .env:

```
DB_ENGINE=django.db.backends.postgresql
DB_NAME=postgres
POSTGRES_USER=postgres
POSTGRES_PASSWORD=postgres
DB_HOST=db
DB_PORT=5432
DJANGO_SECRET_KEY=<YOUR_KEY>
```

### Ключи для запуска Git Actions:

```
DOCKER_USERNAME - юзернейм DockerHub
DOCKER_PASSWORD - пароль DockerHub
HOST -  публичный ip сервера
USER - имя пользователя сервера
SSH_KEY - SHH ключ пользователя сервера
PASSPHRASE - фразовый код пользователя сервера
TELEGRAM_TO - id получается в телеграм
TELEGRAM_TOKEN - токен бота в телеграм
```

### Документация:

```
localhost/redoc/
```

### Стек:

Django, docker, Django-REST, gunicorn, nginx

### Автор:
***FairSk***
