# QRkot_spreadseets

## Описание:
Фонд собирает пожертвования на различные целевые проекты: на медицинское обслуживание нуждающихся хвостатых, на обустройство кошачьей колонии в подвале, на корм оставшимся без попечения кошкам — на любые цели, связанные с поддержкой кошачьей популяции.
Пожертвования в проекты поступают по принципу First In, First Out: все пожертвования идут в проект, открытый раньше других; когда этот проект набирает необходимую сумму и закрывается — пожертвования начинают поступать в следующий проект.

## Развертывание:
### Запуск веб-сервера::
- Склонируйте проект на Ваш компьютер 
```sh 
git clone https://github.com/MShelganov/QRkot_spreadsheets.git
``` 
- Перейдите в папку с проектом 
```sh 
cd QRkot_spreadsheets
``` 
- Создайте и активируйте виртуальное окружение 
```sh 
python -m venv venv 
source venv/Scripts/activate 
``` 
- Обновите менеджер пакетов (pip) 
```sh 
pip install --upgrade pip 
``` 
- Установите необходимые зависимости 
```sh 
pip install -r requirements.txt
``` 
-   Создайте файл с переменными окружения `.env`.Пример его содержимого ниже:
```sh
# название проекта
APP_TITLE=Фонд QRKot
# описание проекта
APP_DESCRIPTION=Благотворительный фонд поддержки котиков
# используемая база данных
DATABASE_URL=sqlite+aiosqlite:///./basename.db
# секретный ключ
SECRET=SEKRET
# email первого суперпользователя
FIRST_SUPERUSER_EMAIL=admin@admin.ru
# пароль первого суперпользователя
FIRST_SUPERUSER_PASSWORD=admin
# email для шаринга
EMAIL=private_E-mail
# данные из JSON-файла сервисного аккаунта
TYPE=service_account
PROJECT_ID=project_id
PRIVATE_KEY_ID=private_key_id
PRIVATE_KEY=private_key
CLIENT_EMAIL=email
CLIENT_ID=client_id
AUTH_URI=https://accounts.google.com/o/oauth2/auth
TOKEN_URI=https://oauth2.googleapis.com/token
AUTH_PROVIDER_X509_CERT_URL=https://www.googleapis.com/oauth2/v1/certs
CLIENT_X509_CERT_URL=https://www.googleapis.com/robot/v1/metadata/x509/service-user%40watchful-gear-351810.iam.gserviceaccount.com
```
- Запуск проекта:
```sh
uvicorn app.main:app --reload
```

## Документация API

Документация по проекту доступна на следующих эндпойнтах:

-   `/docs` — документация в формате Swagger;
-   `/redoc` — документация в формате ReDoc.

## Системные требования:
- [Python](https://www.python.org/) 3.10.6

## Используемые технологии:
- [FastAPI](https://fastapi.tiangolo.com/) 0.78.0
- [Uvicorn](https://www.uvicorn.org/) 0.17.6
- [python-multipart](https://pypi.org/project/python-multipart/) 0.0.5
- [aiosqlite](https://github.com/omnilib/aiosqlite) 0.17.0
- [SQLalchemy](https://www.sqlalchemy.org/) 1.4.36
- [Alembic](https://alembic.sqlalchemy.org/en/latest/) 1.7.7
- [FastAPI Users](https://fastapi-users.github.io/fastapi-users/10.1/)
- [Google Sheets API](https://developers.google.com/sheets/api/)
- [Google Drive API](https://developers.google.com/drive/api/)
- [Google Api Python Client](https://github.com/googleapis/google-api-python-client/)
- [Aiogoogle](https://aiogoogle.readthedocs.io/en/latest/)

## Авторы:
- [Maksim Shelganov](https://github.com/MShelganov/)

## Лицензия:
- MIT