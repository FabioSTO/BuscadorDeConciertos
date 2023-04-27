# Generated by Django 4.2 on 2023-04-27 10:33

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BuscadorConciertos', '0002_alter_artist_artist_id'),
    ]

    operations = [
        migrations.CreateModel(
            name='Concierto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('date', models.DateField()),
                ('place', models.CharField(max_length=255)),
                ('price', models.DecimalField(decimal_places=2, max_digits=8)),
                ('artist', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='BuscadorConciertos.artist')),
            ],
        ),
    ]
