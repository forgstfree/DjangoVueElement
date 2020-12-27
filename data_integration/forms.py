from django.forms import ModelForm
from django.forms import fields
from .models import *


class ProjectForm(ModelForm):
    class Meta:
        model = ProjectModel
        fields = ['name', 'businessUnit', 'description']


class ClusterForm(ModelForm):
    class Meta:
        model = ClusterModel
        fields = ['name', 'description', 'autoSuspend',
                  'date', 'statusOfCluster', 'projectOfCluster']


class FlowForm(ModelForm):
    class Meta:
        model = FlowModel
        fields = ['name', 'dataOfFlow', 'clusterOfFlow']
