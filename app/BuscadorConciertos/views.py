import requests
from . import credentials
from django.shortcuts import render, redirect, reverse
from .models import Artist, Concierto
import pandas as pd
from geopy.geocoders import Nominatim

# Create your views here.

#Código para obtener el país de celebración
geolocator = Nominatim(user_agent="aplicacion_django-cancelo_fernandez_senande")

def get_country(ciudad):
    location = geolocator.geocode(ciudad)
    if location:
        return location.address.split(', ')[-1]
    else:
        return None


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

        attraction_id = artist.artist_id

        url3 = f'https://app.ticketmaster.com/discovery/v2/events?apikey={credentials.TICKETMASTER_ID}&attractionId={attraction_id}'

        response3 = requests.get(url3)

        datazo = response3.json()

        for dato in datazo['_embedded']['events']:
            name = dato['name']
            dateS = dato['dates']['start']['localDate']
            for place in dato['_embedded']['venues']:
                place = place['city']['name']
                country = get_country(place)
            for p in dato['priceRanges']:
                price = p['min']
            concierto = Concierto(name=name, date=dateS, place=place, country=country, price=price, artist=artist)
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
  conciertos = Concierto.objects.all().values() #Obtener valores de los conciertos
  conciertos_df = pd.DataFrame(conciertos) #Importamos a un dataframe de pandas

  #Comprobar si no está vacío, si está vacío y se hace alguna operación da error
  if not conciertos_df.empty:
    #Aquí podemos hacer operaciones sobre el df
    conciertos_df = conciertos_df.drop('id', axis = 1)

  #Transformas el df a formato html para luego pasarlo al render
  conciertos_dict = conciertos_df.to_html()

  print(conciertos_df)

  if request.method == 'POST':
    if 'buscarArtista' in request.POST:
        nombre = request.POST.get('nombre')

        artist_id = (ticketmaster(request, nombre))

        ticket_events(request, artist_id)

        return render(request, 'buscador.html', {'artists': artists, 'conciertos': conciertos_dict})
    
    elif 'iniciarBusqueda' in request.POST:
        ubi = request.POST.get('ubicacion')
        pais = request.POST.get('pais')
        presupuesto = request.POST.get('presupuesto')
        inicio = request.POST.get('inicio')
        fin = request.POST.get('fin')

        return render(request, 'buscador.html', {'artists': artists, 'conciertos': conciertos_dict})
    
  else:

    return render(request, 'buscador.html', {'artists': artists, 'conciertos': conciertos_dict})