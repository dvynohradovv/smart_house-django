from __future__ import absolute_import, unicode_literals
import celery

from .models import Setting


@celery.task()
def smart_home_manager():
    # Здесь ваш код для проверки условий
    pass
