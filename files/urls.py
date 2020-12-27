from django.urls import path
from . import views

app_name = 'files'
urlpatterns = [
    path('', views.upload_file, name='upload'),

]
