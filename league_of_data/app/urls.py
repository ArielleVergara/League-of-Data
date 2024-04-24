from django.urls import path
from .views import home, data_visualization,get_summoner, buscarInvc, nosotros

urlpatterns = [
    path('', home, name='home'),
    path('get_summoner/', get_summoner, name='get_summoner'),
    path('data_visualization/', data_visualization, name='data_visualization'),
    path('busqueda/', buscarInvc, name="buscarInvc"),
    path('nosotros/', nosotros, name="nosotros"),
]