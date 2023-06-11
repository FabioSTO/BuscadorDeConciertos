from django.urls import path
from . import views

urlpatterns = [
    path('spotilog/', views.spotilog, name='spotilog'),
    path('get_top_artists/', views.get_top_artists, name='get_top_artists'),
    path('get_playlists/', views.get_playlists, name='get_playlists'),
    path('get_artists_from_playlist/', views.get_artists_from_playlist, name='get_artists_from_playlist'),
]