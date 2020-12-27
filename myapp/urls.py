from django.urls import path
from . import views

app_name = 'myapp'
urlpatterns = [
    path(r'add_book/', views.add_book),
    path(r'show_books/', views.show_books),
]
