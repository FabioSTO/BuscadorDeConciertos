from django.http import HttpResponse
import requests
from django.shortcuts import render, redirect
from BuscadorConciertos import views
from .models import Artist, Concierto, Playlist
from . import credentials
import json
from django.db import IntegrityError

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
        try:
            id = views.get_attraction_id(artist['name'],True)
            if id:
                    views.get_events_for_id(id)


        except IntegrityError: # Si viola la unicidad del campo artista (se repite)
                continue


    return HttpResponse(status=204)

def get_playlists(request):

    playlists = Playlist.objects.all()
    # Borra todas las playlists anteriores
    playlists.delete()

    url = 'https://api.spotify.com/v1/me/playlists'
    headers = {'Authorization': 'Bearer ' + credentials.SPOTIFY_TOKEN}
    response = requests.get(url, headers=headers)

    arr_playlists = []

    # Convierte a JSON
    data = response.json()

    for playlist in data['items']:
        playlist_name = playlist['name']
        playlist = Playlist(name=playlist_name, playlist_id=playlist['id'])
        playlist.save()
        arr_playlists.append(playlist_name)

    return HttpResponse(json.dumps(arr_playlists), content_type='application/json')

def get_artists_from_playlist(request):

    playlist_name = request.POST.get('playlistName')
    if not playlist_name:
        return HttpResponse(status=204)
    playlist = Playlist.objects.get(name=playlist_name)
    playlist_id = playlist.playlist_id  # Obtenemos la id asignada al nombre

    #Solicitud para obtener artistas
    
    url = f'https://api.spotify.com/v1/playlists/{playlist_id}/tracks?limit=10'
    headers = {'Authorization': 'Bearer ' + credentials.SPOTIFY_TOKEN}
    response = requests.get(url, headers=headers)

    # Convierte a JSON
    data = response.json()
    i=1
 
    for track in data['items']:
        for artist in track['track']['artists']:
            try:
                print(artist['name'])
                id = views.get_attraction_id(artist['name'],True)
                if id:
                    views.get_events_for_id(id)
                
            except IntegrityError: # Si viola la unicidad del campo artista (se repite)
                continue
    
    return HttpResponse(status=204)

def spotilog(request):
    artists = Artist.objects.all()

    try:
        if credentials.SPOTIFY_CODE == '' or credentials.SPOTIFY_TOKEN == '': # Para evitar el KeyError al recargar la página estando logueado
            credentials.SPOTIFY_CODE = request.GET.get('code')
            credentials.SPOTIFY_TOKEN = get_Spotoken(credentials.SPOTIFY_CODE)
    except KeyError:                                                              # En caso de que caduque el token, para que te redirija a la autorización otra vez
        url_auth = f'https://accounts.spotify.com/authorize?response_type=code&client_id={ credentials.SPOTIFY_CLIENT_ID }&redirect_uri=http://127.0.0.1:8000/SpotiLog/spotilog/&scope=user-top-read playlist-read-private'
        return redirect(url_auth)


    username, userpic = get_user_id(request)
    playlists = get_playlists(request)

    return render(request, 'spotilog.html', {'artists': artists, 'username':username, 'userpic':userpic, 'playlists':playlists})