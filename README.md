Smart House pet-project using Python, Django and Celery
==============
<img src="https://user-images.githubusercontent.com/55922843/166962659-0088ce56-6c79-4c5e-b768-aa387e58f685.jpg" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="550" height="350" />
<img src="https://user-images.githubusercontent.com/55922843/166962717-1851c8dd-e6da-414f-a107-ddef5f39ed66.jpg" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="550" height="350" />
<img src="https://user-images.githubusercontent.com/55922843/166962761-9b8b0132-5c23-41ac-8d82-19d6d8ded829.jpg" data-canonical-src="https://gyazo.com/eb5c5741b6a9a16c692170a41a49c858.png" width="800" height="500" />

Установка
---------

Установите pipenv https://docs.pipenv.org/

    $ pip install pipenv


Установите зависимости проекта, включая зависимости для разработки

    $ pipenv install --dev

Активируйте virtualenv проекта

    $ pipenv shell

Запустите миграции

    $ python manage.py migrate
    
Запуск
------

На главной странице сервиса будет расположена панель управления вашим умным домом.

Для запуска периодического опроса состояния дома, используется celery.

Она запускается как celery -A smart_house.celery worker -l info -B

Celery использует Redis как брокер, инструкция по установке Redis: https://redis.io/topics/quickstart


Тестирование
------------


Для запуска тестов выполните команду

.. code-block:: bash

    $ py.test tests
