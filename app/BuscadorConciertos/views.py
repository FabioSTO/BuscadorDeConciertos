import requests
from . import credentials
from django.shortcuts import render

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
    except KeyError:
        attraction_id = None
    
    return attraction_id


def get_events_for_id(attraction_id):
    
    try:

        url3 = f'https://app.ticketmaster.com/discovery/v2/events?apikey={credentials.TICKETMASTER_ID}&attractionId={attraction_id}'

        response3 = requests.get(url3)

        datazo = response3.json()

        events = []
        for dato in datazo['_embedded']['events']:
            name = dato['name']
            dateS = dato['dates']['start']['localDate']
            for place in dato['_embedded']['venues']:
                place = place['city']['name']
            for p in dato['priceRanges']:
                price = p['min']
            events.append({'dateS': dateS, 'name': name, 'place': place, 'price': price})

    except KeyError:
        puedoponercualquiercosayfunciona = None

    return events


def ticketmaster(request, artist_name):

    attraction_id = get_attraction_id(artist_name)

    return attraction_id


def ticket_events(request, attraction_id):
    
    event = get_events_for_id(attraction_id)
    return event


def buscador(request):
  if request.method == 'POST':
    nombre = request.POST.get('nombre')


    attraction_id = (ticketmaster(request, nombre))

    events_for_id = ticket_events(request, attraction_id)

    #nuevo_artista = Artista(nombre=nombre)
    #nuevo_artista.save()
    #return redirect('agregar_artista')

    return render(request, 'buscador.html', {'nombre': nombre, 'attraction_id': attraction_id, 'events': events_for_id})
  else:
    return render(request, 'buscador.html')