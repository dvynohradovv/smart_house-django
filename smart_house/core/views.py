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
        except FileNotFoundError:
            data = {"bedroom_light": False, "bathroom_light": False}
        return {
            'bedroom_target_temperature': Setting.objects.get(controller_name="bedroom_target_temperature").value,
            'hot_water_target_temperature': Setting.objects.get(controller_name="hot_water_target_temperature").value,
            'bedroom_light': data.get('bedroom_light'),
            'bathroom_light': data.get('bathroom_light'),
        }

    def form_valid(self, form: ControllerForm):
        with open(os.path.join(tempfile.gettempdir(), "form.json"), 'w') as fs:
            json.dump(form.cleaned_data, fs)
        return super(ControllerView, self).form_valid(form)
