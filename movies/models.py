from django.conf import settings
from django.db import models
from django.db.models import Count, Q
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from bloodeal.settings import CLOUDINARY_PREFIX_URL
from people.models import People


# Create your models here.
class Movie(models.Model):
    """
    A model that represents an actor or director.
    """
    title_vf = models.CharField(max_length=200,
                                blank=True,
                                null=True)
    title_vo = models.CharField(max_length=200,
                                blank=True,
                                null=True)
    slug = models.SlugField(max_length=200,
                            unique=False,
                            blank=True)
    release_year = models.IntegerField(blank=True,
                                       null=True)
    imdb_id = models.CharField(max_length=9,
                               blank=True,
                               null=True,
                               unique=True)
    movie_image = models.ImageField(null=True,
                                    blank=True,
                                    upload_to="movies/")
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE,
                                     related_name='movie_requested_by',
                                     blank=True,
                                     null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = "Film"

    def __str__(self):

        return f"{self.title_vf}"

    def directors(self):

        directors = MovieDirector.objects.filter(movie=self)
        directors = [director.director for director in directors]

        return directors

    def actors(self):

        actors = MovieActor.objects.filter(movie=self)
        actors = [actor.actor for actor in actors]

        return actors

    def save(self, **kwargs):

        if not self.slug or self.slug == "none":
            self.slug = slugify(self.title_vf)

        return super(Movie, self).save(**kwargs)

    def image_tag(self):

        if self.movie_image != '':
            cloudinary_url = CLOUDINARY_PREFIX_URL + self.movie_image.name

            return mark_safe('<img src="%s" height="100px" />' % cloudinary_url)


class MovieDirector(models.Model):
    """
    A model that represents Director(s) of a movie
    """

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='movie_director')
    director = models.ForeignKey(People, on_delete=models.CASCADE,
                                 related_name='director')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = "Réalisateur par film"
        verbose_name_plural = "Réalisateurs par film"
        unique_together = ("movie", "director")


class MovieActor(models.Model):
    """
    A model that represents Actor(s) of a movie
    """

    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='movie_actor')
    actor = models.ForeignKey(People, on_delete=models.CASCADE,
                              related_name='actor')
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:

        verbose_name = "Acteur par film"
        verbose_name_plural = "Acteurs par film"
        unique_together = ("movie", "actor")


def get_movies(user):

    movies = Movie.objects.all()
    top_movies = movies.annotate(num_favorites=Count("favorite_movie")).order_by("-num_favorites")[:5]
    favorite_movies = movies.filter(favorite_movie__user=user)

    return {"movies": movies,
            "top_movies": top_movies,
            "favorite_movies": favorite_movies,
            "latest_movies": movies.exclude(movie_image="").order_by("-date_created")}


def get_movies_results(keyword):

    movies_results = Movie.objects.filter(Q(title_vf__icontains=keyword) | Q(title_vo__icontains=keyword))

    return {"movies_results": movies_results}


def get_user_requested_movies(user):

    movies = Movie.objects.filter(requested_by=user)

    return {"user_requested_movies": movies}
