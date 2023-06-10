from django.http import HttpResponse
import requests
from django.shortcuts import render
from BuscadorConciertos import views
from .models import Artist, Concierto
from . import credentials
import json

# Create your views here.

def get_Spotoken(code):

    url = 'https://accounts.spotify.com/api/token'
    headers = {'Authorization': 'Basic ' + credentials.SPOTIFY_AUTH_HEADER}
    data = {'grant_type': 'authorization_code', 'code': code, 'redirect_uri': 'http://127.0.0.1:8000/SpotiLog/spotilog/'}
    response = requests.post(url, headers=headers, data=data)
 
    # Extraer el token de acceso de la respuesta en formato JSON
    access_token = response.json()['access_token']

    return access_token

def get_user_id(request):

    code = credentials.SPOTIFY_CODE

    url = 'https://api.spotify.com/v1/me'
    headers = {'Authorization': 'Bearer ' + credentials.SPOTIFY_TOKEN}
    response = requests.get(url, headers=headers)

    # Convierte a JSON
    data = response.json()

    username = data['display_name']
    userpic = data['images'][0]['url']

    return username, userpic

def get_top_artists(request):

    code = credentials.SPOTIFY_CODE

    #Solicitud para obtener artistas
    url = 'https://api.spotify.com/v1/me/top/artists?limit=10'
    headers = {'Authorization': 'Bearer ' + credentials.SPOTIFY_TOKEN}
    response = requests.get(url, headers=headers)

    # Convierte a JSON
    data = response.json()
    i=1

    for artist in data['items']:
        i += 1
        artist = Artist(name=artist['name'], artist_id=i, is_spotified=True)
        artist.save()


    return HttpResponse(status=204)

def get_playlists(request):

    code = credentials.SPOTIFY_CODE

    url = 'https://api.spotify.com/v1/me/playlists'
    headers = {'Authorization': 'Bearer ' + credentials.SPOTIFY_TOKEN}
    response = requests.get(url, headers=headers)

    arr_playlists = []

    # Convierte a JSON
    data = response.json()

    for playlist in data['items']:
        arr_playlists.append(playlist['name'])

    return HttpResponse(json.dumps(arr_playlists), content_type='application/json')

def spotilog(request):
    artists = Artist.objects.all()
    credentials.SPOTIFY_CODE = request.GET.get('code')
    credentials.SPOTIFY_TOKEN = get_Spotoken(credentials.SPOTIFY_CODE)

    username, userpic = get_user_id(request)
    playlists = get_playlists(request)

    return render(request, 'spotilog.html', {'artists': artists, 'username':username, 'userpic':userpic, 'playlists':playlists})