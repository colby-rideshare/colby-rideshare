# Generated by Django 4.1.5 on 2023-02-18 01:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0010_remove_ride_test'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ride',
            name='num_riders',
            field=models.IntegerField(),
        ),
    ]