from django.urls import path
from .views import home, buscarInvc, nosotros, plot_image, view_single_summoner, compare_summoners, comparar, plot_compare

urlpatterns = [
    path('', home, name='home'),
    path('comparar/', comparar, name='comparar'),
    path('summoner/', view_single_summoner, name='view_single_summoner'),
    path('busqueda/', buscarInvc, name="buscarInvc"),
    path('nosotros/', nosotros, name="nosotros"),
    path('plot_image/<str:summoner_name>/<str:match_id>/<str:graph_type>/', plot_image, name='plot_image'),
    path('compare/', compare_summoners, name='compare_summoners'),
    path('plot_compare/<str:summoner_a>/<str:summoner_b>/<int:graph_type>/', plot_compare, name='plot_compare'),

]

