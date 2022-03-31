from PIL import Image
from django.db import models
from django.db.models import CASCADE, Count
from django.utils.text import slugify

from people.models import People
from user_requests.models import MovieRequest


# Create your models here.
class Movie(models.Model):
    """
    A model that represents an actor or director.
    """
    title_vf = models.CharField(max_length=256, blank=False, null=False)
    title_vo = models.CharField(max_length=256, blank=True, null=True)
    slug = models.SlugField(max_length=200, unique=False, blank=True)
    release_year = models.IntegerField(blank=True, null=True)
    imdb_id = models.CharField(max_length=9, blank=True, null=True)
    movie_image = models.ImageField(null=True, blank=True, upload_to="movies/")
    request = models.ForeignKey(MovieRequest,
                                on_delete=CASCADE,
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
        """
        Overrides the save method to update image size at upload to limit width
        and height

        Args:
            force_insert: False
            force_update: False
            using: None
            update_fields: None

        Returns: Nothing

        """
        if not self.slug:
            self.slug = slugify(self.title_vf)
        try:
            if self.movie_image:
                updated_image = Image.open(self.movie_image)
                if updated_image.width > 100 or updated_image.height > 150:
                    output_size = (100, 150)
                    updated_image.thumbnail(output_size)
                    updated_image.save(self.movie_image)
        except (OSError,) as error:
            print(error)
        return super(Movie, self).save(**kwargs)


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


def get_movies(user):
    movies = Movie.objects.all()
    top_movies = movies.annotate(num_favorites=Count("favorite_movie")).order_by("-num_favorites")[:5]
    favorite_movies = movies.filter(favorite_movie__user=user)
    return {"movies": movies,
            "top_movies": top_movies,
            "favorite_movies": favorite_movies,
            "latest_movies": movies.order_by("-date_created")}
