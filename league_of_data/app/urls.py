from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_home, name='get_home'),
    path('get_data_visualization', views.get_data_visualization, name='get_data_visualization')
]