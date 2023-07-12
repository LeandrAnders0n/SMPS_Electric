from django.contrib import admin
from django.urls import path,include
from . import views



urlpatterns = [
    path('index/', views.index, name='index'),
    path('auth/', views.auth, name='auth'),
    path('add_user/', views.add_user, name='add_user'),
    path('add_tower/', views.add_tower, name='add_tower'),
    path('assign_tower/', views.assign_tower, name='assign_tower'),
    path('mqtt_subscribe/', views.mqtt_subscribe, name='mqtt_subscribe'),
]
