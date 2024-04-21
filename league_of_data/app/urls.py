from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_home, name='get_home'),
    path('get_summoner_info', views.get_summoner_info, name='get_summoner_info'),
    path('data_visualization', views.data_visualization, name='data_visualization'),
]