from django.urls import path
from .views import home, get_summoner, buscarInvc, nosotros, plot_image, display_matches
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('get_summoner/', get_summoner, name='get_summoner'),
    path('data_visualization/<str:summoner_name>/<str:summoner_tag>/<str:summoner_region>/', views.display_matches, name='display_matches'),
    path('busqueda/', buscarInvc, name="buscarInvc"),
    path('nosotros/', nosotros, name="nosotros"),
    path('plot_image/<str:summoner_name>/<str:match_id>/<str:graph_type>/', plot_image, name='plot_image'),
    path('time_info_to_plot_image/<str:match_id>/<str:graph_type>/<str:summoner_name>/', views.time_info_to_plot_image, name='time_info_to_plot_image'),
]

