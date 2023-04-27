import requests
from . import credentials
from django.shortcuts import render, redirect, reverse
from .models import Artist, Concierto

# Create your views here.

def get_attraction_id(artist_name):

    orden = 'relevance,desc'
    # Código para obtener el attractionId de Ticketmaster correspondiente al artista
    try:
        # Hacer una solicitud GET a la API de Ticketmaster para buscar eventos basados en el nombre del artista
        url2 = f'https://app.ticketmaster.com/discovery/v2/attractions.json?apikey={credentials.TICKETMASTER_ID}&keyword={artist_name}&sort={orden}&size=1'
        response2 = requests.get(url2)

    # Convertir los datos de la respuesta en formato JSON
        datete = response2.json()

        attraction_id = datete['_embedded']['attractions'][0]['id']
        attraction_name = datete['_embedded']['attractions'][0]['name']

        artist = Artist(name=attraction_name, artist_id=attraction_id)
        artist.save()

    except KeyError:
        artist = None
    
    return artist.id  #El id dentro de la base de usuario


def get_events_for_id(artist_id):
    
    try:

        artist = Artist.objects.get(id=artist_id)

        artid = artist.artist_id
        attraction_id = artist.artist_id

        url3 = f'https://app.ticketmaster.com/discovery/v2/events?apikey={credentials.TICKETMASTER_ID}&attractionId={attraction_id}'

        response3 = requests.get(url3)

        datazo = response3.json()


        for dato in datazo['_embedded']['events']:
            name = dato['name']
            dateS = dato['dates']['start']['localDate']
            for place in dato['_embedded']['venues']:
                place = place['city']['name']
            for p in dato['priceRanges']:
                price = p['min']
            concierto = Concierto(name=name, date=dateS, place=place, price=price, artist=artist)
            concierto.save()

    except KeyError:
        puedoponercualquiercosayfunciona = None


def ticketmaster(request, artist_name):

    artist_id = get_attraction_id(artist_name)

    return artist_id


def ticket_events(request, artist_id):
    
    get_events_for_id(artist_id)

def clean_database(request):
    artists = Artist.objects.all()
    conciertos = Concierto.objects.all()

    # Borra todos los artistas, con el cascade del modelo ya se eliminan los conciertos
    artists.delete()

    return redirect(reverse('buscador'), {'artists': artists, 'conciertos': conciertos})

def delete_artist(request, artist_id):
    artists = Artist.objects.all()
    conciertos = Concierto.objects.all()

    artist = Artist.objects.get(id=artist_id)
    artist.delete()

    return redirect(reverse('buscador'), {'artists': artists, 'conciertos': conciertos})

def buscador(request):
  artists = Artist.objects.all()
  conciertos = Concierto.objects.all()

  if request.method == 'POST':
    if 'buscarArtista' in request.POST:
        nombre = request.POST.get('nombre')


        artist_id = (ticketmaster(request, nombre))

        ticket_events(request, artist_id)

        return render(request, 'buscador.html', {'artists': artists, 'conciertos': conciertos})
    
    elif 'iniciarBusqueda' in request.POST:
        return render(request, 'buscador.html', {'artists': artists, 'conciertos': conciertos})
    
  else:

    return render(request, 'buscador.html', {'artists': artists, 'conciertos': conciertos})