# Memoirs

## About project 
Memoirs is a web platform for personal blogging. Something similar to [Habr](https://habr.com/ru/articles/) or [Yandex dzen](https://dzen.ru/). Here users can register, write their posts, find posts by selected tags and categories.

## About author
This is a pet-project by the first-year student (ITMO University, Faculty of Applied Informatics) Mkrtchyan Karina.

## Project setup  

1. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
2. *Set up your database in settings.py (if you are using something other than SQLite).*

3. **Create .env file in project folder (memoirs)**
   ```
    in .env file write your SECRET_KEY, EMAIL_HOST_USER and EMAIL_HOST_PASSWORD
   ```

4. **Go to the project folder**
    ```bash
      cd memoirs
    ```
5. **Apply migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
6. **Run server**
    ```bash
    python manage.py runserver
    ```