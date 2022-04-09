import datetime

from django.conf import settings
from django.db import models
from django.db.models import Count, Q
from django.utils.safestring import mark_safe
from django.utils.text import slugify

from bloodeal.settings import CLOUDINARY_PREFIX_URL
from movies.models import Movie


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
    vf = models.BooleanField(blank=True,
                             null=True)
    forced_sub = models.BooleanField(blank=True,
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
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE,
                                     related_name='bluray_requested_by',
                                     blank=True,
                                     null=True)
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

        return super(BluRay, self).save(*args, **kwargs)

    def image_tag(self):

        if self.bluray_image != '':

            cloudinary_url = CLOUDINARY_PREFIX_URL + self.bluray_image.name

            return mark_safe('<img src="%s" height="100px" />' % cloudinary_url)


def get_blurays(user):

    blurays = BluRay.objects.all()
    top_blurays = blurays.annotate(num_favorites=Count("favorite_bluray")).order_by("-num_favorites")[:5]
    favorite_blurays = blurays.filter(favorite_bluray__user=user)

    return {"blurays": blurays,
            "top_blurays": top_blurays,
            "favorite_blurays": favorite_blurays,
            "latest_blurays": blurays.filter(release_date__lte=datetime.date.today()).exclude(bluray_image="").order_by("-release_date"),
            "next_blurays": blurays.filter(release_date__gte=datetime.date.today()).exclude(bluray_image="").order_by("release_date")}


def get_blurays_results(keyword):

    blurays_results = BluRay.objects.filter(Q(movie__title_vf__icontains=keyword) | Q(movie__title_vo__icontains=keyword))

    return {"blurays_results": blurays_results}


def get_user_requested_blurays(user):

    blurays = BluRay.objects.filter(requested_by=user)

    return {"user_requested_blurays": blurays}
