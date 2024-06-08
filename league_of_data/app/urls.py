from django.urls import path
from .views import home, data_visualization,get_summoner, buscarInvc, nosotros, plot_image
from . import views

urlpatterns = [
    path('', home, name='home'),
    path('get_summoner/', get_summoner, name='get_summoner'),
    path('data_visualization/', data_visualization, name='data_visualization'),
    path('busqueda/', buscarInvc, name="buscarInvc"),
    path('nosotros/', nosotros, name="nosotros"),
    path('plot_image/<int:match_id>/<str:graph_type>/', views.plot_image, name="plot_image"),
]

