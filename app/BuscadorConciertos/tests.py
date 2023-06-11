from django.test import TestCase
from unittest.mock import patch
import requests
from .models import Artist, Concierto
from . import credentials

# Create your tests here.

class ModelsTestCase(TestCase):

    def setUp(self):
        Artist.objects.create(name='Drake', artist_id=300, is_spotified=False)
        Artist.objects.create(name='Duki', artist_id=393, is_spotified=True)
        drake = Artist.objects.get(id=1)
        duki = Artist.objects.get(id=2)

        Concierto.objects.create(name='Concierto Drake', date='2023-07-30',
            place='Ayuntamiento Toronto', country='Canada', price=60, 
            artist=drake)
        Concierto.objects.create(name='Concierto Duki', date='2023-06-30',
            place='Ayuntamiento Buenos Aires', country='Argentina', price=50,
            artist=duki)
        
    def testArtist(self):
        drake = Artist.objects.get(id=1)
        self.assertEquals(drake.id, 1)
        self.assertEquals(drake.name, 'Drake')
        self.assertEquals(drake.artist_id, '300')
        self.assertEquals(drake.is_spotified, False)

        duki = Artist.objects.get(id=2)
        self.assertEquals(duki.id, 2)
        self.assertEquals(duki.name, 'Duki')
        self.assertEquals(duki.artist_id, '393')
        self.assertEquals(duki.is_spotified, True)

    def tetsConcierto(self):
        conciertoDrake = Concierto.objects.get(id=1)
        self.assertEquals(conciertoDrake.name, 'Concierto Drake')
        self.assertEquals(conciertoDrake.date, '2023-07-30')
        self.assertEquals(conciertoDrake.place, 'Ayuntamiento Toronto')
        self.assertEquals(conciertoDrake.country, 'Canada')
        self.assertEquals(conciertoDrake.price, 60)
        self.assertEquals(conciertoDrake.artist, 'Drake')

        conciertoDuki = Concierto.objects.get(id=2)
        self.assertEquals(conciertoDuki.name, 'Concierto Duki')
        self.assertEquals(conciertoDuki.date, '2023-06-30')
        self.assertEquals(conciertoDuki.place, 'Ayuntamiento Buenos Aires')
        self.assertEquals(conciertoDuki.country, 'Argentina')
        self.assertEquals(conciertoDuki.price, 50)
        self.assertEquals(conciertoDuki.artist, 'Duki')


class ViewsTestCase(TestCase):

    def test_get_attraction_id(self):
        artist_name = 'Drake'
        artist_name2 = 'Duki'
        attraction_id = 'K8vZ917Gp47'
        attarction_id2 = 'K8vZ917bvf7'
        orden = 'relevance,desc'

        url = f'https://app.ticketmaster.com/discovery/v2/attractions.json?apikey={credentials.TICKETMASTER_ID}&keyword={artist_name}&sort={orden}&size=1&segmentName=Music'
        url2 = f'https://app.ticketmaster.com/discovery/v2/attractions.json?apikey={credentials.TICKETMASTER_ID}&keyword={artist_name2}&sort={orden}&size=1&segmentName=Music'
        response = requests.get(url)
        response2 = requests.get(url2)
        data = response.json()
        data2 = response2.json()

        self.assertEquals(data['_embedded']['attractions'][0]['id'], attraction_id)
        self.assertEquals(data['_embedded']['attractions'][0]['name'], artist_name)
        self.assertEquals(data2['_embedded']['attractions'][0]['id'], attarction_id2)
        self.assertEquals(data2['_embedded']['attractions'][0]['name'], artist_name2)

    def test_get_events_for_id(self):
        attraction_id = 'K8vZ917Gp47'

        url3 = f'https://app.ticketmaster.com/discovery/v2/events?apikey={credentials.TICKETMASTER_ID}&attractionId={attraction_id}'
        response = requests.get(url3)
        data = response.json()

        self.assertEquals(data['_embedded']['events'][0]['name'], "Drake: It's All A Blur Tour")
        self.assertEquals(data['_embedded']['events'][0]['dates']['start']['localDate'], '2023-06-29')
        self.assertEquals(data['_embedded']['events'][0]['_embedded']['venues'][0]['city']['name'], 'Memphis')
        self.assertEquals(data['_embedded']['events'][0]['_embedded']['venues'][0]['country']['name'], 'United States Of America')
        self.assertEquals(data['_embedded']['events'][0]['priceRanges'][0]['min'], 50.5)

    def test_get_distance(self):
        origen = 'Madrid'
        destino = 'Barcelona'

        origen2 = 'Chicago'
        destino2 = 'Boston'

        url = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origen}&destinations={destino}&key={credentials.GOOGLE_CLIENT}"
        response = requests.get(url)
        data = response.json()

        url2 = f"https://maps.googleapis.com/maps/api/distancematrix/json?origins={origen2}&destinations={destino2}&key={credentials.GOOGLE_CLIENT}"
        response2 = requests.get(url2)
        data2 = response2.json()
        print(data2)

        self.assertEquals(data['rows'][0]['elements'][0]['distance']['value'], 626061)
        self.assertEquals(data2['rows'][0]['elements'][0]['distance']['value'], 1582651)
