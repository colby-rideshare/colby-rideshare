# Generated by Django 4.1.5 on 2023-03-05 01:59

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carpool', '0018_remove_ride_rider_destination_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='riderequest',
            name='passenger',
            field=models.ForeignKey(default=3, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
