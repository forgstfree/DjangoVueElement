from django.urls import path
from . import views

app_name = 'dblog'
urlpatterns = [
    path('upload/', views.model_form_upload, name='upload'),
    path('show_data/', views.show_data, name='showdata'),
    path('analysislog/', views.analysis_log, name='analysislog'),
]
