from django.urls import path
from . import views
from .views import delete_artist


urlpatterns = [
    path('', views.buscador, name='buscador'),
    path('delete/<int:artist_id>/', delete_artist, name='delete_artist'),
    path('busqArtista/', views.busqArtista, name='busqArtista'),
    path('showLista/', views.showLista, name='showLista'),
    path('iniciarBusqueda/', views.iniciarBusqueda, name='iniciarBusqueda'),
    path('getTitulares/', views.getTitulares, name='getTitulares')
]