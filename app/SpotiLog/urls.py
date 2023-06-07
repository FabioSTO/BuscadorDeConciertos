from django.urls import path
from . import views

urlpatterns = [
    path('spotilog/', views.spotilog, name='spotilog'),
    path('get_top_artists/', views.get_top_artists, name='get_top_artists'),
]