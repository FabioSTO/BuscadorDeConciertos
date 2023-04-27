from django.urls import path
from . import views
from .views import delete_artist, clean_database


urlpatterns = [
    path('buscador/', views.buscador, name='buscador'),
    path('delete/<int:artist_id>/', delete_artist, name='delete_artist'),
    path('clean/', clean_database, name='clean_database')
]