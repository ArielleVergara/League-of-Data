from django.urls import path
from .views import home, data_visualization,get_summoner_info, buscarInvc, nosotros

urlpatterns = [
    path('', home, name='home'),
    path('get_summoner_info/', get_summoner_info, name='get_summoner_info'),
    path('data_visualization/', data_visualization, name='data_visualization'),
    path('busqueda/', buscarInvc, name="buscarInvc"),
    path('nosotros/', nosotros, name="nosotros"),
]