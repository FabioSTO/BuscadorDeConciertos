from django.test import TestCase
from BuscadorConciertos.models import Artist, Concierto

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
