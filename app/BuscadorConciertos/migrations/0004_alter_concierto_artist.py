# Generated by Django 4.1.7 on 2023-05-01 09:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('BuscadorConciertos', '0003_concierto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='concierto',
            name='artist',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='concerts', to='BuscadorConciertos.artist'),
        ),
    ]
