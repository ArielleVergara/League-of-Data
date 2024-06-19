from django.urls import path
from .views import home, buscarInvc, nosotros, plot_image, view_single_summoner, compare_summoners, comparar


urlpatterns = [
    path('', home, name='home'),
    path('comparar/', comparar, name='comparar'),
    path('summoner/', view_single_summoner, name='view_single_summoner'),
    path('busqueda/', buscarInvc, name="buscarInvc"),
    path('nosotros/', nosotros, name="nosotros"),
    path('plot_image/<str:summoner_name>/<str:match_id>/<str:graph_type>/', plot_image, name='plot_image'),
    path('compare/', compare_summoners, name='compare_summoners'),
    
]

