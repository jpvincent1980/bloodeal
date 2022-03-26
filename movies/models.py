from django.db import models
from people.models import People


# Create your models here.
class Movie(models.Model):
    """
    A model that represents an actor or director.
    """
    title_vf = models.CharField(max_length=256, blank=False, null=False)
    title_vo = models.CharField(max_length=256, blank=True, null=True)
    release_year = models.IntegerField(blank=True, null=True)
    imdb_id = models.CharField(max_length=7, blank=True, null=True)
    movie_image = models.ImageField(null=True, blank=True, upload_to="movies/")
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
