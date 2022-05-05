from __future__ import absolute_import, unicode_literals
import tempfile
import celery
import os
import json

import requests.exceptions
from django.conf import settings
from requests import get, post

from django.core.mail import send_mail


from .models import Setting

AUTH_HEADERS = {'Authorization': f"Bearer {settings.SMART_HOME_ACCESS_TOKEN}"}


def request_controller_data():
    try:
        raw_data = get(settings.SMART_HOME_API_URL,
                       headers=AUTH_HEADERS).json()["data"]
    except requests.exceptions.RequestException:
        raw_data = []

    data = {controller["name"]: controller["value"] for controller in raw_data}
    print(data)
    with open(os.path.join(tempfile.gettempdir(), "controller.json"), 'w') as fs:
        json.dump(data, fs)

    return data


def post_response_controller_data(data: dict):
    try:
        post(settings.SMART_HOME_API_URL, json.dumps(data), headers=AUTH_HEADERS)
    except requests.exceptions.RequestException:
        pass


class SmartHomeController:
    def __init__(self, controller_data):
        self.data = controller_data
        self.newdata = {}
        self.bedroom_target_temperature = Setting.objects.get(
            controller_name='bedroom_target_temperature').value
        self.hot_water_target_temperature = Setting.objects.get(
            controller_name='hot_water_target_temperature').value
        self.is_leak = self.data['leak_detector']
        self.is_smoke = self.data['smoke_detector']
        self.is_manual = self.data['curtains'] == 'slightly_open'

    def process_user_form(self):
        try:
            with open(os.path.join(tempfile.gettempdir(), 'form.json')) as f:
                form_data = json.load(f)
            if form_data['bedroom_light'] != self.data['bedroom_light']:
                self.new_data['bedroom_light'] = form_data['bedroom_light']
            if form_data['bathroom_light'] != self.data['bathroom_light']:
                self.new_data['bathroom_light'] = form_data['bathroom_light']
        except FileNotFoundError:
            pass

    def check_leak_water(self):
        if self.is_leak:
            self.new_data['hot_water'] = False
            self.new_data['cold_water'] = False
        send_mail(subject='Emergency situation', message='There is a water leak in your house!',
                  from_email='from@example.com', recipient_list=[settings.EMAIL_RECEPIENT, ])

    def check_cold_water(self):
        if self.is_leak or 'cold_water' in self.new_data:
            self.new_data['boiler'] = False
            self.new_data['washing_machine'] = 'off'

    def check_hot_water(self):
        if self.data['cold_water']:
            if not self.is_leak and not self.is_smoke and \
                    self.data['boiler_temperature'] < self.hot_water_target_temperature * 0.9:
                self.new_data['boiler'] = True
            elif self.data['boiler_temperature'] > self.hot_water_target_temperature * 1.1:
                self.new_data['boiler'] = False

    def check_curtains(self):
        if not self.is_manual:
            if self.data['outdoor_light'] < 50 and not self.data['bedroom_light']:
                self.new_data['curtains'] = 'open'
            elif self.data['outdoor_light'] > 50 or (not self.is_smoke and self.data['bedroom_light']):
                self.new_data['curtains'] = 'close'

    def check_smoke(self):
        if self.is_smoke:
            self.new_data['air_conditioner'] = False
            self.new_data['bedroom_light'] = False
            self.new_data['bathroom_light'] = False
            self.new_data['boiler'] = False
            self.new_data['washing_machine'] = 'off'

    def check_bedroom_temperature(self):
        if not self.is_smoke and \
                self.data['bedroom_temperature'] > self.bedroom_target_temperature * 1.1:
            self.new_data['air_conditioner'] = True
        elif self.data['bedroom_temperature'] < self.bedroom_target_temperature * 0.9:
            self.new_data['air_conditioner'] = False


@celery.task()
def smart_home_manager():
    # Здесь ваш код для проверки условий
    smart_home_controller = SmartHomeController(request_controller_data())
    smart_home_controller.process_user_form()
    smart_home_controller.check_leak_water()
    smart_home_controller.check_cold_water()
    smart_home_controller.check_hot_water()
    smart_home_controller.check_curtains()
    smart_home_controller.check_smoke()
    smart_home_controller.check_bedroom_temperature()
    post_response_controller_data(smart_home_controller.newdata)
