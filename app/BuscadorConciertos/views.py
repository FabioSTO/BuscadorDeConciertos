from django.shortcuts import render
from django.http import HttpResponse
from . import credentials

# Create your views here.

def index(request):
    return HttpResponse("Se vienen cositas")