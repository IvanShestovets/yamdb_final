# CI/CD для проекта API YAMDB
REST API для сервиса YaMDb — базы отзывов о фильмах, книгах и музыке.

## Технологический стек
![Django-app workflow](https://github.com/IvanShestovets/yamdb_final/actions/workflows/yamdb_workflow.yml/badge.svg)

Публичный IPv4: 51.250.90.94

## Workflow
* tests - Проверка кода на соответствие стандарту PEP8 (с помощью пакета flake8) и запуск pytest. Дальнейшие шаги выполнятся только если push был в ветку master или main.
* build_and_push_to_docker_hub - Сборка и доставка докер-образов на Docker Hub
* deploy - Автоматический деплой проекта на боевой сервер. Выполняется копирование файлов из репозитория на сервер:
* send_message - Отправка уведомления в Telegram

### Подготовка для запуска workflow
Создайте и активируйте виртуальное окружение, обновите pip:
```
python -m venv venv
. venv/bin/activate
python -m pip install --upgrade pip
```
Запустите автотесты:
```
pytest
```
Зайдите на виртуальную машинy.
```
ssh <username>@<ipv4>
```
Остановите службу nginx
```
sudo systemctl stop nginx 
````
Установите docker:
```
sudo apt install docker.io
```
Установите docker-compose

Создайте файл docker-compose.yaml на виртуальной машине. 
```
touch docker-compose.yaml
```
Скопируйте с локального компьютера информацию из файла docker-compose.yaml и вставьте на виртуальной машине.
```
nano docker-compose.yaml
```

Cоздайте на виртуальной машине директорию nginx.
```
mkdir nginx/
```
Создайте в директории nginx файл default.conf
```
cd nginx
touch default.conf
```
Скопируйте содержимое файла default.conf с локального компьютера и вставьте в файл default.conf на виртуальной машине.
```
nano default.conf
```

В репозитории на Гитхабе добавьте данные в `Settings - Secrets - Actions secrets`:
```
DOCKER_USERNAME - имя пользователя в DockerHub
DOCKER_PASSWORD - пароль пользователя в DockerHub
HOST - ip-адрес сервера
USER - пользователь
SSH_KEY - приватный ssh-ключ (публичный должен быть на сервере)
PASSPHRASE - кодовая фраза для ssh-ключа
DB_ENGINE - django.db.backends.postgresql
DB_NAME - postgres (по умолчанию)
POSTGRES_USER - postgres (по умолчанию)
POSTGRES_PASSWORD - postgres (по умолчанию)
DB_HOST - db
DB_PORT - 5432
TELEGRAM_TO - id своего телеграм-аккаунта (можно узнать у @userinfobot, команда /start)
TELEGRAM_TOKEN - токен бота (получить токен можно у @BotFather, /token, имя бота)
```
При внесении любых изменений в проект, после коммита и пуша
```
git add .
git commit -m "..."
git push
```