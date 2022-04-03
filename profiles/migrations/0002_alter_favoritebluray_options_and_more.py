# Generated by Django 4.0.3 on 2022-03-23 14:15

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('movies', '0002_alter_movie_options_alter_movieactor_options_and_more'),
        ('blurays', '0002_alter_bluray_options'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('people', '0002_alter_people_options'),
        ('profiles', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='favoritebluray',
            options={'verbose_name': 'Blu-Ray Préféré', 'verbose_name_plural': 'Blu-Rays Préférés'},
        ),
        migrations.AlterModelOptions(
            name='favoritemovie',
            options={'verbose_name': 'Film Préféré', 'verbose_name_plural': 'Films Préférés'},
        ),
        migrations.AlterModelOptions(
            name='favoritepeople',
            options={'verbose_name': 'Personnalité Préférée', 'verbose_name_plural': 'Personnalités Préférées'},
        ),
        migrations.AlterUniqueTogether(
            name='favoritebluray',
            unique_together={('user', 'blu_ray')},
        ),
        migrations.AlterUniqueTogether(
            name='favoritemovie',
            unique_together={('user', 'movie')},
        ),
        migrations.AlterUniqueTogether(
            name='favoritepeople',
            unique_together={('user', 'people')},
        ),
    ]
