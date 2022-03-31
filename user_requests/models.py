from itertools import chain

from django.conf import settings
from django.db import models
import re

from django.db.models import Value

STATUS_CHOICES = [("1", "Non traitée"),
                  ("2", "Acceptée"),
                  ("3", "Refusée"),
                  ("4", "Indéterminée")]


# Create your models here.
class PeopleRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='people_user_request',
                             blank=False,
                             null=False)
    imdb_link = models.URLField(blank=False,
                                null=False,
                                verbose_name="Lien IMDB")
    imdb_id = models.CharField(max_length=9, blank=True, null=True)
    status = models.CharField(max_length=56,
                              choices=STATUS_CHOICES,
                              blank=False,
                              null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Suggestion de personnalité N° {self.pk}"

    def get_imdb_id(self):
        imdb_id = re.search(r"nm[0-9].[^/]+", str(self.imdb_link))
        if imdb_id:
            imdb_id = imdb_id[0]
        return imdb_id

    def save(self, **kwargs):
        if self.imdb_link and not self.imdb_id:
            imdb_id = self.get_imdb_id()
            if imdb_id:
                self.imdb_id = imdb_id
        return super().save(**kwargs)

    class Meta:
        verbose_name = "Ajout - Personnalité"
        verbose_name_plural = "Ajouts - Personnalités"


class MovieRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='movie_user_request',
                             blank=False,
                             null=False)
    imdb_link = models.URLField(blank=False,
                                null=False,
                                verbose_name="Lien IMDB")
    imdb_id = models.CharField(max_length=9, blank=True, null=True)
    status = models.CharField(max_length=56,
                              choices=STATUS_CHOICES,
                              blank=False,
                              null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Suggestion de films N° {self.pk}"

    def get_imdb_id(self):
        imdb_id = re.search(r"tt[0-9].[^/]+", str(self.imdb_link))
        if imdb_id:
            imdb_id = imdb_id[0]
        return imdb_id

    def save(self, **kwargs):
        if self.imdb_link and not self.imdb_id:
            imdb_id = self.get_imdb_id()
            if imdb_id:
                self.imdb_id = imdb_id
        return super().save(**kwargs)

    class Meta:
        verbose_name = "Ajout - Film"
        verbose_name_plural = "Ajouts - Films"


class BluRayRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='bluray_user_request',
                             blank=False,
                             null=False)
    amazon_link = models.URLField(blank=False,
                                  null=False,
                                  verbose_name="Lien Amazon")
    asin = models.CharField(max_length=10, blank=True, null=True)
    status = models.CharField(max_length=56,
                              choices=STATUS_CHOICES,
                              blank=False,
                              null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Suggestion de Blu-Ray N° {self.pk}"

    def get_asin(self):
        asin = re.search(r"B0[.]*[^/]+", str(self.amazon_link))
        if asin:
            asin = asin[0]
        return asin

    def save(self, **kwargs):
        if self.amazon_link and not self.asin:
            asin = self.get_asin()
            if asin:
                self.asin = asin
        return super().save(**kwargs)

    class Meta:
        verbose_name = "Ajout - Blu-Ray"
        verbose_name_plural = "Ajouts - Blu-Rays"


def get_user_requests_blurays(user, only_open=False):
    requests = BluRayRequest.objects.filter(user=user).annotate(type=Value("blu-ray"))
    requests = requests.filter(status=1) if only_open else requests
    return {"user_requests_blurays": requests}


def get_user_requests_movies(user, only_open=False):
    requests = MovieRequest.objects.filter(user=user).annotate(type=Value("film"))
    requests = requests.filter(status=1) if only_open else requests
    return {"user_requests_movies": requests}


def get_user_requests_people(user, only_open=False):
    requests = PeopleRequest.objects.filter(user=user).annotate(type=Value("personnalité"))
    requests = requests.filter(status=1) if only_open else requests
    return {"user_requests_people": requests}


def get_user_requests(user, only_open=False):
    blurays_requests = get_user_requests_blurays(user, only_open=only_open).get("user_requests_blurays", BluRayRequest.objects.none())
    movies_requests = get_user_requests_movies(user, only_open=only_open).get("user_requests_movies", MovieRequest.objects.none())
    people_requests = get_user_requests_people(user, only_open=only_open).get("user_requests_people", PeopleRequest.objects.none())
    requests = list(chain(blurays_requests, movies_requests, people_requests))
    return {"user_requests": requests}


def get_user_requests_total(user, only_open=False):
    total = 0
    total += len(get_user_requests_blurays(user, only_open=only_open).get("user_requests_blurays", BluRayRequest.objects.none()))
    total += len(get_user_requests_movies(user, only_open=only_open).get("user_requests_movies", MovieRequest.objects.none()))
    total += len(get_user_requests_people(user, only_open=only_open).get("user_requests_people", PeopleRequest.objects.none()))
    return {"user_requests_total": total}
