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


class SmartHomeController:
    def __init__(self, data):
        self.data = data

    def check_leak_water(self):
        pass

    def check_cold_water(self):
        pass

    def check_hot_water(self):
        pass

    def check_curtains(self):
        pass

    def check_smoke(self):
        pass

    def check_bedroom_temperature(self):
        pass


@celery.task()
def smart_home_manager():
    # Здесь ваш код для проверки условий
    smart_home_controller = SmartHomeController(request_controller_newdata())
    smart_home_controller.check_leak_water()
    smart_home_controller.check_cold_water()
    smart_home_controller.check_hot_water()
    smart_home_controller.check_curtains()
    smart_home_controller.check_smoke()
    smart_home_controller.check_bedroom_temperature()
