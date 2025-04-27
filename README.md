# Memoirs

## About project 
Memoirs is a web platform for personal blogging. Something similar to [Habr](https://habr.com/ru/articles/) or [Yandex dzen](https://dzen.ru/). Here users can register, write their posts, find posts by selected tags and categories.

## About author
This is a pet-project by a first-year student (ITMO University, Faculty of Applied Informatics) in the framework of the "Programming" discipline, Mkrtchyan Karina.

## Project setup  

1. **Install dependencies**
    ```bash
    pip install -r requirements.txt
    ```
2. *Set up your database in settings.py (if you are using something other than SQLite).*

3. **Go to the project folder**
    ```bash
      cd memoirs
    ```
4. **Apply migrations**
    ```bash
    python manage.py makemigrations
    python manage.py migrate
    ```
5. **Run server**
    ```bash
    python manage.py runserver
    ```