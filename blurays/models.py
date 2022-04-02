import datetime

from PIL import Image
from django.conf import settings
from django.db import models
from django.db.models import Count, Q
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from movies.models import Movie


BLURAY_CHOICES = [("1", "Oui"),
                  ("2", "Non"),
                  ("3", "Indéterminé")]


# Create your models here.
class BluRay(models.Model):
    """
    A model that represents an actor or director.
    """
    movie = models.ForeignKey(Movie,
                              on_delete=models.CASCADE,
                              related_name='bluray_movie',
                              blank=True,
                              null=True)
    slug = models.SlugField(max_length=200,
                            unique=False,
                            blank=True)
    title = models.CharField(max_length=200,
                             blank=True,
                             null=True)
    uhd = models.BooleanField(blank=True,
                              null=True)
    vf = models.SmallIntegerField(choices=BLURAY_CHOICES,
                                  blank=True,
                                  null=True)
    forced_sub = models.SmallIntegerField(choices=BLURAY_CHOICES,
                                          blank=True,
                                          null=True)
    ean = models.CharField(max_length=13,
                           blank=True,
                           null=True)
    amazon_asin = models.CharField(max_length=10,
                                   blank=True,
                                   null=True,
                                   unique=True)
    amazon_aff_link = models.URLField(max_length=200,
                                      blank=True)
    release_date = models.DateField(blank=True,
                                    null=True)
    bluray_image = models.ImageField(null=True,
                                     blank=True,
                                     upload_to="blurays/")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Blu-Ray"

    def __str__(self):
        name = self.title if self.title else self.movie
        return f"{name}"

    def save(self, *args, **kwargs):
        if not self.slug or self.slug == "none":
            self.slug = slugify(self.movie) if not self.title else slugify(self.title)
        if self.amazon_asin:
            self.amazon_aff_link = f"https://www.amazon.fr/dp/{self.amazon_asin}?m=A1X6FK5RDHNB96&tag=laureatis-21"
        if self.bluray_image:
            try:
                with Image.open(self.bluray_image) as updated_image:
                    if updated_image.width > 100 or updated_image.height > 150:
                        print(f"Width -> {updated_image.width}")
                        print(f"Height -> {updated_image.height}")
                        output_size = (100, 150)
                        updated_image.thumbnail(output_size)
                        updated_image.save(self.bluray_image)
            except (OSError, ):
                print("L'image n'a pas pu être réduite.")
        return super(BluRay, self).save(*args, **kwargs)

    def image_tag(self):
        if self.bluray_image != '':
            return mark_safe('<img src="%s%s" height="100px" />' % (f'{settings.MEDIA_URL}',
                                                     self.bluray_image))


def get_blurays(user):
    blurays = BluRay.objects.all()
    top_blurays = blurays.annotate(num_favorites=Count("favorite_bluray")).order_by("-num_favorites")[:5]
    favorite_blurays = blurays.filter(favorite_bluray__user=user)
    return {"blurays": blurays,
            "top_blurays": top_blurays,
            "favorite_blurays": favorite_blurays,
            "latest_blurays": blurays.filter(release_date__lte=datetime.date.today()).order_by("release_date"),
            "next_blurays": blurays.filter(release_date__gte=datetime.date.today()).order_by("release_date")}


def get_blurays_results(keyword):
    blurays_results = BluRay.objects.filter(Q(movie__title_vf__icontains=keyword) |
                                            Q(movie__title_vo__icontains=keyword))
    return {"blurays_results": blurays_results}
