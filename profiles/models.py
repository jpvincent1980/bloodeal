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
        user_name = self.user.pseudo if self.user.pseudo else self.user
        return f"{self.user} est abonné à {self.followed_user}"

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
                              related_name='favorite_movie')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'movie')
        verbose_name = "Film Préféré"
        verbose_name_plural = "Films Préférés"

    def __str__(self):
        user_name = self.user.pseudo if self.user.pseudo else self.user.email
        return user_name + " aime " + self.movie.title_vf


class FavoritePeople(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user_people')
    people = models.ForeignKey(People,
                               on_delete=models.CASCADE,
                               related_name='favorite_people')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'people')
        verbose_name = "Personnalité Préférée"
        verbose_name_plural = "Personnalités Préférées"

    def __str__(self):
        user_name = self.user.pseudo if self.user.pseudo else self.user.email
        people_name = f"{self.people.first_name} {self.people.last_name}"
        return user_name + " aime " + people_name


class FavoriteBluRay(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='user_bluray')
    bluray = models.ForeignKey(BluRay,
                               on_delete=models.CASCADE,
                               related_name='favorite_bluray')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        unique_together = ('user', 'bluray')
        verbose_name = "Blu-Ray Préféré"
        verbose_name_plural = "Blu-Rays Préférés"

    def __str__(self):
        user_name = self.user.pseudo if self.user.pseudo else self.user.email
        movie_name = self.bluray.movie.title_vf
        return user_name + " aime le Blu-Ray de " + movie_name


def get_user_all_favorites(user):
    # Get BluRay queryset from favorite blurays
    favorite_blurays = BluRay.objects.filter(favorite_bluray__user=user)
    # Get BluRay queryset from favorite movies
    favorite_movies = Movie.objects.filter(favorite_movie__user=user)
    bluray_movies_favorites = BluRay.objects.filter(movie__in=favorite_movies)
    # Get BluRay queryset from favorite people
    favorite_people = People.objects.filter(favorite_people__user=user)
    movies_director_favorites = Movie.objects.filter(movie_director__director__in=favorite_people)
    movies_actor_favorites = Movie.objects.filter(movie_actor__actor__in=favorite_people)
    movies_favorites = movies_director_favorites | movies_actor_favorites
    user_movies_recommended_favorites = movies_favorites.difference(favorite_movies)
    bluray_people_favorites = BluRay.objects.filter(movie__in=movies_favorites)
    # Join all BluRay querysets from previous queries
    all_blurays = bluray_movies_favorites | bluray_people_favorites
    user_recommended_favorites = all_blurays.difference(favorite_blurays)
    return {"user_favorite_movies": favorite_movies,
            "user_recommended_movies": user_movies_recommended_favorites,
            "user_favorite_blurays": favorite_blurays,
            "user_recommended_blurays": user_recommended_favorites,
            "user_favorite_people": favorite_people,
            "user_all_blurays": all_blurays}


def get_user_suggested_blurays(user):
    # User all favorites minus already favorites
    user_all_favorites = get_user_all_favorites(user).get("user_favorites",
                                                          BluRay.objects.none())
    # Get user already favorite blurays
    favorite_blurays = BluRay.objects.filter(favorite_bluray__user=user)
    # Get the difference between both querysets
    user_suggested_blurays = user_all_favorites.difference(favorite_blurays)
    return {"user_suggested_blurays": user_suggested_blurays}
