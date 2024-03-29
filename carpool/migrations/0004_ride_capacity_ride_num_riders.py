# Generated by Django 4.1.4 on 2023-01-04 07:16

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0003_ride_notes'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='capacity',
            field=models.IntegerField(default=1),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ride',
            name='num_riders',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
    ]
