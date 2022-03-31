import datetime

from PIL import Image
from django.db import models
from django.db.models import CASCADE, Count
from django.utils.text import slugify

from movies.models import Movie
from user_requests.models import BluRayRequest


# Create your models here.
class BluRay(models.Model):
    """
    A model that represents an actor or director.
    """
    movie = models.ForeignKey(Movie, on_delete=models.CASCADE,
                              related_name='bluray_movie', blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=False, blank=True)
    ean = models.CharField(max_length=13, blank=True, null=True)
    amazon_asin = models.CharField(max_length=10, blank=True, null=True)
    amazon_aff_link = models.URLField(max_length=200, blank=True)
    release_date = models.DateField(blank=True, null=True)
    blu_ray_image = models.ImageField(null=True,
                                      blank=True,
                                      upload_to="blurays/")
    request = models.ForeignKey(BluRayRequest,
                                on_delete=CASCADE,
                                blank=True,
                                null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blu-Ray"

    def __str__(self):
        return f"Blu-Ray de {self.movie}"

    def save(self, *args, **kwargs):
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
            self.slug = slugify(self.movie)
        if self.amazon_asin:
            self.amazon_aff_link = f"https://www.amazon.fr/dp/{self.amazon_asin}?m=A1X6FK5RDHNB96&tag=laureatis-21"
        if self.blu_ray_image:
            updated_image = Image.open(self.blu_ray_image)
            if updated_image.width > 100 or updated_image.height > 150:
                output_size = (100, 150)
                updated_image.thumbnail(output_size)
                updated_image.save(self.blu_ray_image)
        return super(BluRay, self).save(*args, **kwargs)


def get_blurays(user):
    blurays = BluRay.objects.all()
    top_blurays = blurays.annotate(num_favorites=Count("favorite_bluray")).order_by("-num_favorites")[:5]
    favorite_blurays = blurays.filter(favorite_bluray__user=user)
    return {"blurays": blurays,
            "top_blurays": top_blurays,
            "favorite_blurays": favorite_blurays,
            "latest_blurays": blurays.filter(release_date__lte=datetime.date.today()).order_by("release_date"),
            "next_blurays": blurays.filter(release_date__gte=datetime.date.today()).order_by("release_date")}
