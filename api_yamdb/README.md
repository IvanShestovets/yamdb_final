# **Проект YaMDb**
### ***Описание***

Проект YaMDb собирает **отзывы** пользователей на **произведения**.
Произведения делятся на **категории**, такие как "Книги", "Фильмы", "Музыка" и тд.
Произведению может быть присвоен **жанр** из списка предустановленных(например, "Сказка", "Рок" или "Артхаус").
Добавлять произведения, категории и жанры может только администратор.
Пользователи оставляют к произведениям текстовые **отзывы** и ставят произведению оценку в диапазоне от одного до десяти (целое число); из пользовательских оценок формируется усреднённая оценка произведения — **рейтинг** (целое число). На одно произведение пользователь может оставить только один отзыв.
Пользователи могут оставлять **комментарии** к отзывам.
Добавлять отзывы, комментарии и ставить оценки могут только аутентифицированные пользователи.

### ***Техническое описание проекта YaMDb***

В приложении **reviews** описан бэкэнд проекта, а в приложении **api** - **API**.
### _Ресурсы API YaMDb_
- Ресурс **auth**: аутентификация.
- Ресурс **users**: пользователи.
- Ресурс **titles**: произведения, к которым пишут отзывы (определённый фильм, книга или песенка).
- Ресурс **categories**: категории (типы) произведений («Фильмы», «Книги», «Музыка»). Одно произведение может быть привязано только к одной категории.
- Ресурс **genres**: жанры произведений. Одно произведение может быть привязано к нескольким жанрам.
- Ресурс **reviews**: отзывы на произведения. Отзыв привязан к определённому произведению.
- Ресурс **comments**: комментарии к отзывам. Комментарий привязан к определённому отзыву.

### _Пользовательские роли и права доступа_
- **Аноним** — может просматривать описания произведений, читать отзывы и комментарии.
- **Аутентифицированный пользователь (user)** — может читать всё, как и **Аноним**, может публиковать отзывы и ставить оценки произведениям (фильмам/книгам/песенкам), может комментировать отзывы; может редактировать и удалять свои отзывы и комментарии, редактировать свои оценки произведений. Эта роль присваивается по умолчанию каждому новому пользователю.
- **Модератор (moderator)** — те же права, что и у Аутентифицированного пользователя, плюс право удалять и редактировать любые отзывы и комментарии.
- **Суперюзер Django** должен всегда обладать правами администратора, пользователя с правами admin. Даже если изменить пользовательскую роль суперюзера — это не лишит его прав администратора. Суперюзер — всегда администратор, но администратор — не обязательно суперюзер.

### _Самостоятельная регистрация новых пользователей_
1. Пользователь отправляет POST-запрос с параметрами `email` и `username` на эндпоинт `/api/v1/auth/signup/`.
2. Сервис **YaMDB** отправляет письмо с кодом подтверждения (`confirmation_code`) на указанный адрес `email`.
3. Пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен).

В результате пользователь получает токен и может работать с API проекта, отправляя этот токен с каждым запросом. 
После регистрации и получения токена пользователь может отправить PATCH-запрос на эндпоинт `/api/v1/users/me/` и заполнить поля в своём профайле (описание полей — в документации).

### _Создание пользователя администратором_
Пользователей создаёт администратор — через админ-зону сайта или через POST-запрос на специальный эндпоинт `api/v1/users/` (описание полей запроса для этого случая есть в документации). При создании пользователя не предполагается автоматическая отправка письма пользователю с кодом подтверждения.
После этого пользователь должен самостоятельно отправить свой `email` и `username` на эндпоинт `/api/v1/auth/signup/` , в ответ ему должно прийти письмо с кодом подтверждения.
Далее пользователь отправляет POST-запрос с параметрами `username` и `confirmation_code` на эндпоинт `/api/v1/auth/token/`, в ответе на запрос ему приходит `token` (JWT-токен), как и при самостоятельной регистрации.

### _Как развернуть проект_
- _Создайте и активируйте виртуальное окружение_

_на Windows_
```sh
python -m venv venv
source venv/Scripts/activate
```
_на MacOS и Linux_
```sh
python3 -m venv venv
source venv/bin/activate
```

- _Установите зависимости из файла requirements.txt_
```sh
python -m pip install --upgrade pip
pip install -r requirements.txt
```
- _В папке с файлом manage.py выполните миграции_
```sh
python manage.py migrate
```
- _В папке с файлом manage.py импортируйте данные из csv файлов в БД_

_Для Windows_
```sh
python manage.py load_all_data
```

_Для UNIX и прочих_
```sh
python manage.py load_all_data_unix
```

- _В папке с файлом manage.py выполните команду_
```sh
python manage.py runserver
```
## ***Запросы к API***
Server - `/api/v1/`

<details>
  <summary>Примеры запросов</summary>

### _AUTH - Регистрация пользователей и выдача токенов_
## `POST` _/auth/signup/_
_Получить код подтверждения на переданный **email**. Права доступа: **Доступно без токена**. Использовать имя 'me' в качестве **username** запрещено. Поля **email** и **username** должны быть уникальными._

_Request body_
```json
{
  "email": "user@example.com",
  "username": "e4H4rj501Kuqu9I.f17-7YjGt_+K0r8Dg1rXzKQPBHHUVzTB83o6@fuBmk1Uo-tpOsr@ANdKAF112MjIGCMJuItetyz0PXzMnz"
}
```

_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "email": "string",
  "username": "string"
}
```
**Code 400** - Отсутствует обязательное поле или оно некорректно
```json
{
  "field_name": [
    "string"
  ]
}
```

## `POST` _/auth/token/_
_Получение JWT-токена в обмен на username и confirmation code. Права доступа: **Доступно без токена**._

_Request body_
```json
{
  "username": "@KfcEZR7f92x-Pz09b+ahiKKLwWtpR+36w6FehP74i0vBO9qh@W2cIxYRpar7ocYrduYA3cveAXz",
  "confirmation_code": "string"
}
```

_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "token": "string"
}
```
**Code 400** - Отсутствует обязательное поле или оно некорректно
```json
{
  "field_name": [
    "string"
  ]
}
```

### _CATEGORIES - Категории (типы) произведений_

## `GET` _/categories/_
_Получить список всех категорий Права доступа: **Доступно без токена**._

***Parametrs***
**search** - Поиск по названию категории

_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "qJEXafTmx3ZipFKgTsn6MAU-r8UuYP"
    }
  ]
}
```

### `POST` _/categories/_
_Создать категорию. Права доступа: **Администратор**. Поле `slug` каждой категории должно быть уникальным._

_Request body_
```json
{
  "name": "string",
  "slug": "xhWkopY49yINmPF18mqQ7jZirDfNYEZ1_ix0Ststyq6_JNDEvr"
}
```

_Responses_
**Code 201** - Удачное выполнение запроса
```json
{
  "name": "string",
  "slug": "string"
}
```
**Code 400** - Отсутствует обязательное поле или оно некорректно
```json
{
  "field_name": [
    "string"
  ]
}
```
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа

### `DELETE` _/categories/{slug}/_
_Удалить категорию. Права доступа: **Администратор**._

***Parametrs***
**slug** - slug категории

_Responses_
**Code 204** - Удачное выполнение запроса
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа
**Code 404** - Категория не найдена

### _GENRES - Категории жанров_

## `GET` _/genres/_
_Получить список всех жанров. Права доступа: **Доступно без токена**._

***Parametrs***
**search** - Поиск по названию жанра

_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "name": "string",
      "slug": "X0RkpUiB"
    }
  ]
}
```

### `POST` _/genres/_
_Добавить жанр. Права доступа: **Администратор**. Поле `slug` каждого жанра должно быть уникальным._

_Request body_
```json
{
  "name": "string",
  "slug": "3oro4GP3fyN3f3RU3-tGqOR2tW7joL10X3oGp_YuIFxzECqTbS"
}
```

_Responses_
**Code 201** - Удачное выполнение запроса
```json
{
  "name": "string",
  "slug": "string"
}
```
**Code 400** - Отсутствует обязательное поле или оно некорректно
```json
{
  "field_name": [
    "string"
  ]
}
```
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа

### `DELETE` _/genres/{slug}/_
_Удалить жанр. Права доступа: **Администратор**._

***Parametrs***
**slug** - slug жанра

_Responses_
**Code 204** - Удачное выполнение запроса
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа
**Code 404** - Категория не найдена

### _TITLES - Произведения, к которым пишут отзывы (определённый фильм, книга или песенка)._

## `GET` _/titles/_
_Получить список всех объектов. Права доступа: **Доступно без токена**._

***Parametrs***
**search** - Поиск по названию категории
**category** - фильтрует по полю slug категории
**genre** - фильтрует по полю slug жанра
**name** - фильтрует по названию произведения
**year** - фильтрует по году

_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "name": "string",
      "year": 0,
      "rating": 0,
      "description": "string",
      "genre": [
        {
          "name": "string",
          "slug": "-kiqz3iIxdQwckzpgVhhl-13bbwAh7_ftXElCGkHAUWUomw8e"
        }
      ],
      "category": {
        "name": "string",
        "slug": "RPK4cmvSP1qBpPyZOr84bqO8M2f-GlRltz10KcYo28qgNlRulq"
      }
    }
  ]
```

### `POST` _/titles/_
_Добавить новое произведение. Права доступа: **Администратор**. Нельзя добавлять произведения, которые еще не вышли (год выпуска не может быть больше текущего). При добавлении нового произведения требуется указать уже существующие категорию и жанр._

_Request body_
```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```

_Responses_
**Code 201** - Удачное выполнение запроса
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "l-fPe2ze0AKA7WXUkctVjKPxDb8AC4JLyb33QEFZIzwN5jNnnG"
    }
  ],
  "category": {
    "name": "string",
    "slug": "8Z_H6ZLzC1iHiPhS0ga3dQkYxO93Vj3RwLrVqDrYJD44R6Otmt"
  }
}
```
**Code 400** - Отсутствует обязательное поле или оно некорректно
```json
{
  "field_name": [
    "string"
  ]
}
```
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа

### `GET` _/titles/{titles_id}/_
_Информация о произведении. Права доступа: **Доступно без токена**._

***Parametrs***
**titles_id** - ID объекта

_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "TvZnR42uvfpjcu83rCmfOTqkGcTW4wn"
    }
  ],
  "category": {
    "name": "string",
    "slug": "cEG7qT8iF1cdFeX"
  }
}
```
**Code 404** - Объект не найден

### `PATCH` _/titles/{titles_id}/_
_Обновить информацию о произведении. Права доступа: **Администратор**._

***Parametrs***
**titles_id** - ID объекта

_Request body_
```json
{
  "name": "string",
  "year": 0,
  "description": "string",
  "genre": [
    "string"
  ],
  "category": "string"
}
```
_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "id": 0,
  "name": "string",
  "year": 0,
  "rating": 0,
  "description": "string",
  "genre": [
    {
      "name": "string",
      "slug": "FteB2S8Zad6Qv1"
    }
  ],
  "category": {
    "name": "string",
    "slug": "y4X-EqJYzAIozhLB9"
  }
}
```
**Code 400** - Отсутствует обязательное поле или оно некорректно
```json
{
  "field_name": [
    "string"
  ]
}
```
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа
**Code 404** - Категория не найдена

### `DELETE` _/titles/{titles_id}/_
_Удалить произведение. Права доступа: **Администратор**._

***Parametrs***
**titles_id** - ID объекта

_Responses_
**Code 204** - Удачное выполнение запроса
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа
**Code 404** - Произведение не найдено

### _REVIEWS - Отзывы._

## `GET` _/titles/{title_id}/reviews/_
_Получить список всех отзывов. Права доступа: **Доступно без токена**._

***Parametrs***
**title_id ** - ID произведения

_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "score": 10,
      "pub_date": "2023-01-05T18:33:46.054Z"
    }
  ]
}
```
**Code 404** - Произведение не найдено

### `POST` _/titles/{title_id}/reviews/_
_Добавить новый отзыв. Пользователь может оставить только один отзыв на произведение. Права доступа: **Аутентифицированные пользователи**._

***Parametrs***
**title_id ** - ID произведения

_Request body_
```json
{
  "text": "string",
  "score": 10
}
```

_Responses_
**Code 201** - Удачное выполнение запроса
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 10,
  "pub_date": "2023-01-05T18:36:02.662Z"
}
```
**Code 400** - Отсутствует обязательное поле или оно некорректно
```json
{
  "field_name": [
    "string"
  ]
}
```
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа

### `GET` _/titles/{titles_id}/reviews/{review_id}/_
_Получить отзыв по id для указанного произведения. Права доступа: **Доступно без токена**._

***Parametrs***
**titles_id** - ID произведения
**review_id** - ID отзыва

_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 10,
  "pub_date": "2023-01-05T18:38:02.632Z"
}
```
**Code 404** - Произведение или отзыв не найден

### `PATCH` _/titles/{titles_id}/reviews/{review_id}/_
_Частично обновить отзыв по id. Права доступа: **Автор отзыва, модератор или администратор**._

***Parametrs***
**titles_id** - ID произведения
**review_id** - ID отзыва

_Request body_
```json
{
  "text": "string",
  "score": 10
}
```
_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "score": 10,
  "pub_date": "2023-01-05T18:41:41.171Z"
}
```

**Code 400** - Отсутствует обязательное поле или оно некорректно
```json
{
  "field_name": [
    "string"
  ]
}
```
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа
**Code 404** - Не найдено произведение или отзыв

### `DELETE` _/titles/{titles_id}/reviews/{review_id}/_
_Удалить отзыв по id. Права доступа: **Автор отзыва, модератор или администратор**._

***Parametrs***
**titles_id** - ID произведения
**review_id** - ID отзыва

_Responses_
**Code 204** - Удачное выполнение запроса
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа
**Code 404** - Не найдено произведение или отзыв

### _COMMENTS - Комментарии к отзывам._

## `GET` _/titles/{title_id}/reviews/{review_id}/_
_Получить список всех комментариев к отзыву по id. Права доступа: **Доступно без токена**._

***Parametrs***
**title_id** - ID произведения
**review_id** - ID отзыва

_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "id": 0,
      "text": "string",
      "author": "string",
      "pub_date": "2023-01-05T18:50:42.124Z"
    }
  ]
}
```
**Code 404** - Не найдено произведение или отзыв

### `POST` _/titles/{title_id}/reviews/{review_id}/comments/_
_Добавить новый комментарий для отзыва. Права доступа: **Аутентифицированные пользователи**._

***Parametrs***
**title_id** - ID произведения
**review_id** - ID отзыва

_Request body_
```json
{
  "text": "string"
}
```

_Responses_
**Code 201** - Удачное выполнение запроса
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2023-01-05T18:51:51.801Z"
}
```
**Code 400** - Отсутствует обязательное поле или оно некорректно
```json
{
  "field_name": [
    "string"
  ]
}
```
**Code 401** - Необходим JWT-токен
**Code 404** - Не найдено произведение, отзыв или комментарий

### `GET` _/titles/{titles_id}/reviews/{review_id}/comments/{comments_id}/_
_Получить комментарий для отзыва по id. Права доступа: **Доступно без токена**._

***Parametrs***
**titles_id** - ID произведения
**review_id** - ID отзыва
**comments_id** - ID комментария

_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2023-01-05T18:53:34.785Z"
}
```
**Code 404** - Не найдено произведение, отзыв или комментарий

### `PATCH` _/titles/{titles_id}/reviews/{review_id}/comments/{comments_id}/_
_Частично обновить комментарий к отзыву по id. Права доступа: **Автор отзыва, модератор или администратор**._

***Parametrs***
**titles_id** - ID произведения
**review_id** - ID отзыва
**comments_id** - ID комментария

_Request body_
```json
{
  "text": "string"
}
```
_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "id": 0,
  "text": "string",
  "author": "string",
  "pub_date": "2023-01-05T18:54:45.327Z"
}
```

**Code 400** - Отсутствует обязательное поле или оно некорректно
```json
{
  "field_name": [
    "string"
  ]
}
```
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа
**Code 404** - Не найдено произведение, отзыв или комментарий

### `DELETE` _/titles/{titles_id}/reviews/{review_id}/comments/{comments_id}/_
_Удалить комментарий к отзыву по id. Права доступа: **Автор отзыва, модератор или администратор**._

***Parametrs***
**titles_id** - ID произведения
**review_id** - ID отзыва
**comments_id** - ID комментария

_Responses_
**Code 204** - Удачное выполнение запроса
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа
**Code 404** - Не найдено произведение, отзыв или комментарий

### _USERS - Пользователи._

## `GET` _/users/_
_Получить список всех пользователей. Права доступа: **Администратор**._

***Parametrs***
**search ** - Поиск по имени пользователя (username)

_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "count": 0,
  "next": "string",
  "previous": "string",
  "results": [
    {
      "username": "LmDzoedIUy1yHi.@BwjBE+EDfJ.VsGyQQ7QedNC6oBs0W3QY9x62uMls+37G2NJwCOL4WiSE+_sw7oOjQ5kzyv2z71EID0Woz",
      "email": "user@example.com",
      "first_name": "string",
      "last_name": "string",
      "bio": "string",
      "role": "user"
    }
  ]
}
```
**Code 401** - Необходим JWT-токен

## `POST` _/users/_
_Добавить нового пользователя. Права доступа: **Администратор**. Поля `email` и `username` должны быть уникальными._

_Request body_
```json
{
  "username": "Wbvbz6yGeRS70ktl+CTwXG+79rKmk.D06vAM.ANlHhOAhd8IQkrcz",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
_Responses_
**Code 201** - Удачное выполнение запроса
```json
{
  "username": "n8JnWSSo1T4.hucMsrp6sLjLX8sJPcAM8RIqTQ8zT@9.gM+9RFfhfMnjmNp+ob8+mi_ycUjRoz@N+z",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
**Code 400** - Отсутствует обязательное поле или оно некорректно
```json
{
  "field_name": [
    "string"
  ]
}
```
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа

## `GET` _/users/{username}/_
_Получить пользователя по username. Права доступа: **Администратор**._

***Parametrs***
**username** - Username пользователя

_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "username": "1ZRk.eycY63m_4VRcfJGX_NhcMiIz",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа
**Code 404** - Пользователь не найден

## `POST` _/users/{username}/_
_Изменить данные пользователя по username. Права доступа: **Администратор**. Поля `email` и `username` должны быть уникальными._

***Parametrs***
**username** - Username пользователя

_Request body_
```json
{
  "username": "_6@vCvFi_sJOJB-PN@wW.gVdaGWW7p4ueOZ7B@nMgURcNgyHmTz",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "username": "n8JnWSSo1T4.hucMsrp6sLjLX8sJPcAM8RIqTQ8zT@9.gM+9RFfhfMnjmNp+ob8+mi_ycUjRoz@N+z",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
**Code 400** - Отсутствует обязательное поле или оно некорректно
```json
{
  "field_name": [
    "string"
  ]
}
```
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа
**Code 404** - Пользователь не найден

## `DELETE` _/users/{username}/_
_Удалить пользователя по username. Права доступа: **Администратор**._

***Parametrs***
**username** - Username пользователя

_Responses_
**Code 204** - Удачное выполнение запроса
**Code 401** - Необходим JWT-токен
**Code 403** - Нет прав доступа
**Code 404** - Произведение не найдено

## `GET` _/users/me/_
_Получить данные своей учетной записи Права доступа: **Любой авторизованный пользователь**_

_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "username": "n8JnWSSo1T4.hucMsrp6sLjLX8sJPcAM8RIqTQ8zT@9.gM+9RFfhfMnjmNp+ob8+mi_ycUjRoz@N+z",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```

## `PATCH` _/users/me/_
_Изменить данные своей учетной записи Права доступа: **Любой авторизованный пользователь**. Поля `email` и `username` должны быть уникальными._

_Request body_
```json
{
  "username": "Vbz",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string"
}
```

_Responses_
**Code 200** - Удачное выполнение запроса
```json
{
  "username": "n8JnWSSo1T4.hucMsrp6sLjLX8sJPcAM8RIqTQ8zT@9.gM+9RFfhfMnjmNp+ob8+mi_ycUjRoz@N+z",
  "email": "user@example.com",
  "first_name": "string",
  "last_name": "string",
  "bio": "string",
  "role": "user"
}
```
**Code 400** - Отсутствует обязательное поле или оно некорректно
```json
{
  "field_name": [
    "string"
  ]
}
```

</details>

## Авторы
- Василий Игнатьев - _https://github.com/vaskos63i_
- Иван Шестовец - _https://github.com/IvanShestovets_
- Сергей Ефанов - _https://github.com/sergey-efanov_