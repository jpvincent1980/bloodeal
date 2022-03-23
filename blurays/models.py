from django.db import models

from movies.models import Movie


# Create your models here.
class BluRay(models.Model):
    """
    A model that represents an actor or director.
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='bluray_movie', blank=False, null=False)
    ean = models.CharField(max_length=13, blank=True, null=True)
    amazon_asin = models.CharField(max_length=10, blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    blu_ray_image = models.ImageField(null=True, blank=True, upload_to="blurays/")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blu-Ray"
