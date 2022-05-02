Coursera House
==============

Это шаблон курсового проекта от преподавателей курса.


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

И приступайте к разработке.


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