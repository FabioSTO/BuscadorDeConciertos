from django.urls import path
from . import views

urlpatterns = [
    path('buscador/', views.buscador, name='buscador'),
]