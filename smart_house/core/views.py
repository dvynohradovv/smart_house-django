import json
import os
import tempfile

from django.urls import reverse_lazy
from django.views.generic import FormView

from .models import Setting
from .form import ControllerForm


class ControllerView(FormView):
    form_class = ControllerForm
    template_name = 'core/control.html'
    success_url = reverse_lazy('form')

    def get_context_data(self, **kwargs):
        context = super(ControllerView, self).get_context_data()
        try:
            with open(os.path.join(tempfile.gettempdir(), "controller.json")) as fs:
                context['data'] = json.load(fs)
        except FileNotFoundError:
            context['data'] = {}
        return context

    def get_initial(self):
        try:
            with open(os.path.join(tempfile.gettempdir(), "controller.json")) as fs:
                data = json.load(fs)
            return {
                'bedroom_target_temperature': data.get('bedroom_target_temperature', None),
                'hot_water_target_temperature': data.get('hot_water_target_temperature', None),
                'bedroom_light': data.get('bedroom_light', False),
                'bathroom_light': data.get('bathroom_light', False),
            }
        except FileNotFoundError:
            return {}

    def form_valid(self, form):
        return super(ControllerView, self).form_valid(form)
