# Generated by Django 4.1.5 on 2023-03-04 23:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carpool', '0016_gasprice'),
    ]

    operations = [
        migrations.AddField(
            model_name='ride',
            name='rider_destination',
            field=models.CharField(default='Boston, MA', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='ride',
            name='rider_origin',
            field=models.CharField(default='Colby College, Mayflower Hill Drive, Waterville, ME, USA', max_length=100),
        ),
        migrations.AlterField(
            model_name='ride',
            name='time',
            field=models.CharField(choices=[('Morning', 'Morning'), ('Afternoon', 'Afternoon'), ('Evening', 'Evening')], max_length=10),
        ),
    ]
