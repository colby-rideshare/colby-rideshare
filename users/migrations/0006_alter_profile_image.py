# Generated by Django 4.1.5 on 2023-03-09 03:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_remove_profile_first_name_remove_profile_last_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='image',
            field=models.ImageField(default='default.jpg', upload_to='profile_pics', verbose_name='Profile picture'),
        ),
    ]