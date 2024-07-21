# Backers

## Установка и использование (для Windows)

1. **Клонируйте репозиторий**
    ``` bash
    git clone https://github.com/Anton31312/backers.git
    ```

2. **Создайте и активируйте виртуальное окружение**
    ``` bash
    Проект использует Poetry, за информацией по установке https://pythonchik.ru/okruzhenie-i-pakety/menedzher-zavisimostey-poetry-polnyy-obzor-ot-ustanovki-do-nastroyki
    ```
3. **Для работы программы необходимо установить зависимости**
    ``` bash
    Пропишите "poetry init" в командную строку.
    ```
4. **Создайте файл .env. Введите туда свои настройки как указано в файле .env.sample.**
    *Дополнительно* \
    *Если вы используете redis в качестве брокера celery, то в файле .env* \
    *В поле CACHES_LOCATION замените localhost(127.0.0.1) на redis*
5. **Создайте базу данных** 
    ``` bash
    Например, через консоль: 1 - psql -U postgres; 
    2 - create database online_studing; 
    3 - выход: \q
    ```
6. **Сделайте и примените миграции.** 
    ``` bash
    python manage.py makemigrations 
    python manage.py migrate
    ```
7. **Можете загрузить тестовые данные**
    ``` bash
    python manage.py loaddata data_posts.json 
    python manage.py loaddata data_users.json либо создать свои.
    ```
8. **Создайте суперпользователя**
    ``` bash
    python manage.py csu
    ```
9. **Запустите сервер** 
    ``` bash
    python manage.py runserver
    ```

## Запуск проекта с использованием Docker

### Шаги по запуску

1. **Клонируйте репозиторий**
    ```
    git clone https://github.com/Anton31312/backers.git
    ```

2. **Переименуйте пример файла окружения с .env.sample в .env и отредактируйте его**

    *Дополнительно* \
    *Если вы используете redis в качестве брокера celery, то в файле .env* \
    *В поле CACHES_LOCATION замените localhost(127.0.0.1) на redis*


4. **Постройте и запустите контейнеры Docker**
    ```
    docker-compose up -d --build
    ```

5. **Выполните миграции**

   ```
   docker-compose exec app python manage.py migrate
   ```

6. **Создание суперпользователя**
    ```
    docker-compose exec app python manage.py csu
    ```
    *Дополнительно* \
    Данные для входа под аккаунтом администратора: \
    *Логин: 89992223311* \
    *Пароль: 123qwe456rty* 

### Доступ к приложению
- Приложение будет доступно по адресу: [http://localhost:8000](http://localhost:8000)
- Админ панель Django: [http://localhost:8000/admin](http://localhost:8000/admin)

### Остановка контейнеров
Для остановки контейнеров используйте следующую команду:

```
docker-compose down
```
