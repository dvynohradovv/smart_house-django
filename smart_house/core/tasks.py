from __future__ import absolute_import, unicode_literals
import tempfile
import celery
import os
import json

import requests.exceptions
from django.conf import settings
from requests import get

from .models import Setting

AUTH_HEADERS = {'Authorization': f"Bearer {settings.SMART_HOME_ACCESS_TOKEN}"}


def request_controller_newdata():
    try:
        raw_data = get(settings.SMART_HOME_API_URL, headers=AUTH_HEADERS).json()["data"]
    except requests.exceptions.RequestException:
        raw_data = []

    data = {controller["name"]: controller["value"] for controller in raw_data}
    with open(os.path.join(tempfile.gettempdir(), "controller.json"), 'w') as fs:
        json.dump(data, fs)

    return data


@celery.task()
def smart_home_manager():
    # Здесь ваш код для проверки условий
    pass
