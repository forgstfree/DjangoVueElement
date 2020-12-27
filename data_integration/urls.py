from django.urls import path
from . import views

app_name = 'data_integration'
urlpatterns = [
    path('getList/', views.getList, name='getlist'),
    path('getBrief/', views.getBrief, name='getbrief'),
    path('getProjectCluster/', views.getProjectCluster, name='getprojectcluster'),
    path('createData/', views.createData, name='createproject'),
    path('updateData/', views.updateData, name='updatedata'),
    path('deleteData/', views.deleteData, name='deletedata'),
    path('startScheduler/', views.startScheduler, name='startScheduler'),
]
