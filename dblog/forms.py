from django.forms import ModelForm
from .models import LogFileModel


class LogForm(ModelForm):
    class Meta:
        model = LogFileModel
        fields = ['name', 'file']
