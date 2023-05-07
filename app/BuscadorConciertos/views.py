import requests
from . import credentials
from django.shortcuts import render, redirect, reverse
from .models import Artist, Concierto
import pandas as pd
from datetime import datetime

def get_distance(origin, destination):
    url = f'https://maps.googleapis.com/maps/api/directions/json?destination={destination}&origin={origin}&key={credentials.GOOGLE_CLIENT}'
    response = requests.get(url)
    distance = 0
    if 'routes' in response.json():
        routes = response.json()['routes']
        if routes and 'legs' in routes[0]:
            legs = routes[0]['legs']
            if legs and 'steps' in legs[0]:
                for step in legs[0]['steps']:
                    distance += step['distance']['value']
    return distance

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


def buscador(request):
  artists = Artist.objects.all()
  conciertos = Concierto.objects.all().values() #Obtener valores de los conciertos
  conciertos_df = pd.DataFrame(conciertos) #Importamos a un dataframe de pandas

  #Transformas el df a formato html para luego pasarlo al render
  #conciertos_dict = conciertos_df.to_html()

  if request.method == 'POST':
    if 'buscarArtista' in request.POST:
        nombre = request.POST.get('nombre')

        artist_id = (ticketmaster(request, nombre))

        ticket_events(request, artist_id)

        return render(request, 'buscador.html', {'artists': artists})
    
    elif 'iniciarBusqueda' in request.POST:
        ubi = request.POST.get('ubicacion')
        pais = request.POST.get('pais')
        presupuesto = request.POST.get('presupuesto')
        inicio = request.POST.get('inicio')
        fin = request.POST.get('fin')

        conciertos_df = aplicar_filtros(conciertos_df, pais, presupuesto, inicio, fin, ubi)
        conciertos_dict = conciertos_df.to_html()

        print(conciertos_df)

        return render(request, 'buscador.html', {'artists': artists, 'conciertos': conciertos_dict})
    
  else:

    return render(request, 'buscador.html', {'artists': artists})
  

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
        limite = primerdia + pd.Timedelta(days=7)  
        primerasemana = df.loc[(df['date'] < limite)]   #Obtiene los conciertos de la primera semana


        for index, row in primerasemana.iterrows():     #Calcula distancia entre la ubi del usuario y las citys de la primera semana
            dist = get_distance(ubi, row['place'])
            pricedist = (float(row['price']) + round(dist/500000, 1)) #Calula según 1$/500KM (por ahora da juego)
            primerasemana.loc[index, 'distance'] = dist
            primerasemana.loc[index, 'price+dist'] = pricedist
            new_origin=primerasemana.loc[primerasemana['price+dist'].idxmax()]
            ubi=new_origin['place']

    return primerasemana