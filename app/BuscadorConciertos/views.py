import requests
from . import credentials
from django.shortcuts import render, redirect, reverse
from .models import Artist, Concierto
import pandas as pd
from datetime import datetime
from django.http import HttpResponse
import json

def get_distance(origen, destino):
    url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origen}&destinations={destino}&key={credentials.GOOGLE_CLIENT}"

    response = requests.get(url)
    json_response = response.json()

    distancia_metros = json_response["rows"][0]["elements"][0]["distance"]["value"]
    return distancia_metros


# Create your views here.
def get_attraction_id(artist_name):

    orden = 'relevance,desc'
    # Código para obtener el attractionId de Ticketmaster correspondiente al artista
    try:
        # Hacer una solicitud GET a la API de Ticketmaster para buscar eventos basados en el nombre del artista
        url2 = f'https://app.ticketmaster.com/discovery/v2/attractions.json?apikey={credentials.TICKETMASTER_ID}&keyword={artist_name}&sort={orden}&size=1&segmentName=Music'
        response2 = requests.get(url2)

    # Convertir los datos de la respuesta en formato JSON
        datete = response2.json()

        attraction_id = datete['_embedded']['attractions'][0]['id']
        attraction_name = datete['_embedded']['attractions'][0]['name']

        artist = Artist(name=attraction_name, artist_id=attraction_id)
        artist.save()

    except KeyError:
        artist = None

    except AttributeError:
        artist = None
        return None
    
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
                city = place['city']['name']
                country = place['country']['name']
            for p in dato['priceRanges']:
                price = p['min']
            concierto = Concierto(name=name, date=dateS, place=city, country=country, price=price, artist=artist)
            concierto.save()

    except KeyError:
        key = None


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

def showLista(request):
    artists = Artist.objects.all()
    artist_list = []
    for artist in artists:
        artist_list.append({
            'id': artist.id,
            'name': artist.name,
            'is_spotified': artist.is_spotified
        })

    response_data = {
        'artists': artist_list,
    }

    return HttpResponse(json.dumps(response_data), content_type='application/json')

from django.db import IntegrityError

def busqArtista(request):
    nombre = request.POST.get('nombre')
    
    try:
        artist_id = ticketmaster(request, nombre)
        ticket_events(request, artist_id)
        return HttpResponse()  # Retorna una respuesta vacía
    except IntegrityError:
        return HttpResponse('Duplicado.')
    except AttributeError:
        return HttpResponse('Inválido.')

def buscador(request):
  artists = Artist.objects.all()
  conciertos = Concierto.objects.all().values() #Obtener valores de los conciertos
  conciertos_df = pd.DataFrame(conciertos) #Importamos a un dataframe de pandas

  #Transformas el df a formato html para luego pasarlo al render
  #conciertos_dict = conciertos_df.to_html()

  url_auth = f'https://accounts.spotify.com/authorize?response_type=code&client_id={ credentials.SPOTIFY_CLIENT_ID }&redirect_uri=http://127.0.0.1:8000/SpotiLog/spotilog/&scope=user-top-read'

  if request.method == 'POST':
    
    if 'iniciarBusqueda' in request.POST:
        ubi = request.POST.get('ubicacion')
        pais = request.POST.get('pais')
        presupuesto = request.POST.get('presupuesto')
        inicio = request.POST.get('inicio')
        fin = request.POST.get('fin')

        conciertos_df = aplicar_filtros(conciertos_df, pais, presupuesto, inicio, fin, ubi)
        dataframe_selecciones = pd.DataFrame(conciertos_df)
        conciertos_dict = dataframe_selecciones.to_html()

        waypoints = ""
        origin = ""
        destination = ""

        for concierto in conciertos_df[1:-1]:
             waypoints += concierto.place + "," + concierto.country + "|"
        origin = conciertos_df[0].place + "," + conciertos_df[0].country
        destination = conciertos_df[-1].place + "," + conciertos_df[-1].country
        
        ##### MAPS #####
        
        maps_url = f"https://www.google.com/maps/embed/v1/directions?key={credentials.GOOGLE_CLIENT}&origin={origin}&destination={destination}&waypoints={waypoints[:-1]}&units=metric&mode=driving"
        print(origin)
        print(destination)
        print(waypoints)
        #################

        return render(request, 'buscador.html', {'artists': artists, 'conciertos': conciertos_dict, 'url_auth':url_auth, 'maps_url': maps_url})
    
  else:

    return render(request, 'buscador.html', {'artists': artists, 'url_auth':url_auth})
  

def aplicar_filtros(df, pais, presupuesto, inicio, fin, ubi):
    if not df.empty:
        print(inicio)
        fecha_inicio = datetime.strptime( inicio,'%Y-%m-%d').date()
        fecha_fin = datetime.strptime( fin,'%Y-%m-%d').date()
        
        if pais:
            df = df.loc[df['country'] == pais]
        df = df.drop(df[df['price'] >= float(presupuesto)].index)
        df = df.drop('id', axis=1)
        df = df.sort_values(by = ['date'])
        rango_dias = (df['date'] >fecha_inicio) & (df['date'] <=fecha_fin)
        df = df.loc[rango_dias]

        primerdia = df.iloc[0]['date']  #Obtiene el día del primer concierto

        total_price = 0.0
        selecciones = []

        while total_price < float(presupuesto):
            
            limite = primerdia + pd.Timedelta(days=7)  

            semana_actual = df.loc[(df['date'] < limite)]   #Obtiene los conciertos de la primera semana

            distances = get_distance(ubi, semana_actual['place'])
            pricedist = semana_actual['price'].astype(float) + round(distances / 500000, 1)

            semana_actual['distance'] = distances
            semana_actual['price+dist'] = pricedist
                
            seleccion = semana_actual.loc[semana_actual['price+dist'].idxmin()] #Seleccionamos "mejor" concierto de la semana actual

            arid = seleccion['artist_id']
            df = df.query("artist_id != @arid")
            
            total_price += float(seleccion['price']) #Va obteniendo el precio total

            selecciones.append(seleccion) #Añade a la lista de seleccionados el mejor concierto

            #selecciones = pd.concat([selecciones, seleccion], ignore_index=True)

            print(total_price)
            print(arid)

            ubi = seleccion['place'] #Nueva ubi de origen

            df = df.loc[df['date'] >= limite] #Eliminar filas de esta semana

            if df.empty:
                break

            primerdia = df.iloc[0]['date']  #Nuevo primer dia de nueva semana

    return selecciones