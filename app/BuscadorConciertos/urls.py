from django.urls import path
from . import views
from .views import delete_artist, clean_database


urlpatterns = [
    path('', views.buscador, name='buscador'),
    path('delete/<int:artist_id>/', delete_artist, name='delete_artist'),
    path('clean/', clean_database, name='clean_database'),
    path('busqArtista/', views.busqArtista, name='busqArtista'),
    path('showLista/', views.showLista, name='showLista'),
    path('iniciarBusqueda/', views.iniciarBusqueda, name='iniciarBusqueda'),
]