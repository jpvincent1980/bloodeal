from django.conf import settings
from django.db import models

from movies.models import Movie
from people.models import People
from blurays.models import BluRay


# Create your models here.
class FavoriteUser(models.Model):
    """
    A model that represents a user and user(s) followed
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user_following')
    followed_user = models.ForeignKey(settings.AUTH_USER_MODEL,
                                      on_delete=models.CASCADE,
                                      related_name='user_followed')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.email + " abonné à " + self.followed_user.email

    class Meta:
        unique_together = ('user', 'followed_user')
        verbose_name = "Abonnement"
        verbose_name_plural = "Abonnements"


class FavoriteMovie(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user_movie')
    movie = models.ForeignKey(Movie,
                              on_delete=models.CASCADE,
                              related_name='movie')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')
        verbose_name = "Film Préféré"
        verbose_name_plural = "Films Préférés"


class FavoritePeople(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user_people')
    people = models.ForeignKey(People,
                               on_delete=models.CASCADE,
                               related_name='people')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'people')
        verbose_name = "Personnalité Préférée"
        verbose_name_plural = "Personnalités Préférées"


class FavoriteBluRay(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user_bluray')
    blu_ray = models.ForeignKey(BluRay,
                                on_delete=models.CASCADE,
                                related_name='blu_ray')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'blu_ray')
        verbose_name = "Blu-Ray Préféré"
        verbose_name_plural = "Blu-Rays Préférés"
