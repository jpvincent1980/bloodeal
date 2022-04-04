from itertools import chain

from django.conf import settings
from django.db import models
import re

from django.db.models import Value, CASCADE

from blurays.models import BluRay
from deals.models import Deal
from movies.models import Movie
from people.models import People
from .functions import IMDBMovieData, IMDBPeopleData

STATUS_CHOICES = [("1", "En-cours"),
                  ("2", "Acceptée"),
                  ("3", "Refusée"),
                  ("4", "Indéterminée")]


# Create your models here.
class PeopleRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=CASCADE,
                             related_name='people_user_request',
                             blank=False,
                             null=False)
    imdb_link = models.URLField(blank=False,
                                null=False,
                                verbose_name="Lien IMDB")
    imdb_id = models.CharField(max_length=9, blank=True, null=True)
    first_name = models.CharField(max_length=256,
                                  blank=True,
                                  null=True)
    last_name = models.CharField(max_length=256,
                                 blank=True,
                                 null=True)
    birth_date = models.DateField("Date de naissance",
                                  blank=True,
                                  null=True)
    death_date = models.DateField("Date de décès",
                                  blank=True,
                                  null=True)
    people = models.ForeignKey(People,
                               on_delete=CASCADE,
                               blank=True,
                               null=True)
    status = models.CharField(max_length=56,
                              choices=STATUS_CHOICES,
                              blank=False,
                              null=False,
                              default="1")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demande de personnalité N° {self.pk}"

    def get_imdb_id(self):
        imdb_id = re.search(r"nm[0-9].[^(?:/|?)]+", str(self.imdb_link))
        if imdb_id:
            imdb_id = imdb_id[0]
        return imdb_id

    def save(self, **kwargs):
        if self.imdb_link and not self.imdb_id:
            imdb_id = self.get_imdb_id()
            if imdb_id:
                self.imdb_id = imdb_id
                try:
                    people = IMDBPeopleData(imdb_id)
                    first_name = people.imdb_get_first_name
                    self.first_name = first_name if first_name else None
                    last_name = people.imdb_get_last_name
                    self.last_name = last_name if last_name else None
                    birth_date = people.imdb_get_birth_date
                    self.birth_date = birth_date if birth_date else None
                    death_date = people.imdb_get_death_date
                    self.death_date = death_date if death_date else None
                except (ConnectionError, ):
                    print(f"Impossible de scraper le site IMDB pour {imdb_id}")
        return super().save(**kwargs)

    class Meta:
        verbose_name = "Demande - Personnalité"
        verbose_name_plural = "Demandes - Personnalités"


class MovieRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=CASCADE,
                             related_name='movie_user_request',
                             blank=False,
                             null=False)
    imdb_link = models.URLField(blank=False,
                                null=False,
                                verbose_name="Lien IMDB")
    imdb_id = models.CharField(max_length=9, blank=True, null=True)
    title_vf = models.CharField(max_length=200,
                                blank=True,
                                null=True)
    title_vo = models.CharField(max_length=200,
                                blank=True,
                                null=True)
    release_year = models.IntegerField(blank=True,
                                       null=True)
    movie = models.ForeignKey(Movie,
                              on_delete=CASCADE,
                              blank=True,
                              null=True)
    status = models.CharField(max_length=56,
                              choices=STATUS_CHOICES,
                              blank=False,
                              null=False,
                              default="1")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demande de films N° {self.pk}"

    def get_imdb_id(self):
        imdb_id = re.search(r"tt[0-9].[^(?:/|?)]+", str(self.imdb_link))
        if imdb_id:
            imdb_id = imdb_id[0]
        return imdb_id

    def save(self, **kwargs):
        if self.imdb_link and not self.imdb_id:
            imdb_id = self.get_imdb_id()
            if imdb_id:
                self.imdb_id = imdb_id
                try:
                    movie = IMDBMovieData(imdb_id)
                    title_vf = movie.imdb_get_title
                    self.title_vf = title_vf if title_vf else None
                    self.title_vo = title_vf
                    release_year = movie.imdb_get_release_year
                    self.release_year = int(release_year) if release_year else None
                except (ConnectionError, ):
                    print(f"Impossible de scraper le site IMDB pour {imdb_id}")

        return super().save(**kwargs)

    class Meta:
        verbose_name = "Demande - Film"
        verbose_name_plural = "Demandes - Films"


class BluRayRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=CASCADE,
                             related_name='bluray_user_request',
                             blank=False,
                             null=False)
    amazon_link = models.URLField(blank=False,
                                  null=False,
                                  verbose_name="Lien Amazon")
    asin = models.CharField(max_length=10,
                            blank=True,
                            null=True)
    bluray = models.ForeignKey(BluRay,
                               on_delete=CASCADE,
                               related_name='created_bluray',
                               blank=True,
                               null=True)
    status = models.CharField(max_length=56,
                              choices=STATUS_CHOICES,
                              blank=False,
                              null=False,
                              default="1")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demande de Blu-Ray N° {self.pk}"

    def get_asin(self):
        asin = re.search(r"B0[.]*[^(?:/|?)]+", str(self.amazon_link))
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
        verbose_name = "Demande - Blu-Ray"
        verbose_name_plural = "Demandes - Blu-Rays"


class DealRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=CASCADE,
                             related_name='deal_user_request',
                             blank=False,
                             null=False)
    bluray = models.ForeignKey(BluRay,
                               on_delete=CASCADE,
                               blank=True,
                               null=True)
    amazon_link = models.URLField(blank=False,
                                  null=False,
                                  verbose_name="Lien Amazon")
    asin = models.CharField(max_length=10, blank=True, null=True)
    price = models.FloatField()
    deal = models.ForeignKey(Deal,
                             on_delete=CASCADE,
                             blank=True,
                             null=True)
    status = models.CharField(max_length=56,
                              choices=STATUS_CHOICES,
                              blank=False,
                              null=False,
                              default="1")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Demande de bon plan N° {self.pk}"

    def get_asin(self):
        asin = re.search(r"B0[.]*[^(?:/|?)]+", str(self.amazon_link))
        if asin:
            asin = asin[0]
        return asin

    def save(self, **kwargs):
        if self.amazon_link and not self.asin:
            asin = self.get_asin()
            if asin:
                self.asin = asin
        if self.asin:
            bluray = BluRay.objects.filter(amazon_asin=self.asin)
            if bluray:
                self.bluray = bluray[0]
        return super().save(**kwargs)

    class Meta:
        verbose_name = "Demande - Bon Plan"
        verbose_name_plural = "Demande - Bons Plans"


def get_user_requests_blurays(user, requests_filter=[choice[0] for choice in STATUS_CHOICES]):
    requests = BluRayRequest.objects.filter(user=user).annotate(type=Value("blu-ray"))
    requests = requests.filter(status__in=requests_filter) if requests_filter else requests
    requests = requests.order_by("-date_created")
    return {"user_requests_blurays": requests,
            "filter": requests_filter}


def get_user_requests_movies(user, requests_filter=[choice[0] for choice in STATUS_CHOICES]):
    requests = MovieRequest.objects.filter(user=user).annotate(type=Value("film"))
    requests = requests.filter(status__in=requests_filter) if requests_filter else requests
    requests = requests.order_by("-date_created")
    return {"user_requests_movies": requests,
            "filter": requests_filter}


def get_user_requests_people(user, requests_filter=[choice[0] for choice in STATUS_CHOICES]):
    requests = PeopleRequest.objects.filter(user=user).annotate(type=Value("personnalité"))
    requests = requests.filter(status__in=requests_filter) if requests_filter else requests
    requests = requests.order_by("-date_created")
    return {"user_requests_people": requests,
            "filter": requests_filter}


def get_user_requests_deals(user, requests_filter=[choice[0] for choice in STATUS_CHOICES]):
    requests = DealRequest.objects.filter(user=user).annotate(type=Value("deal"))
    requests = requests.filter(status__in=requests_filter) if requests_filter else requests
    requests = requests.order_by("-date_created")
    return {"user_requests_deals": requests,
            "filter": requests_filter}


def get_user_requests(user, requests_filter=[choice[0] for choice in STATUS_CHOICES]):
    blurays_requests = get_user_requests_blurays(user,
                                                 requests_filter=requests_filter).get("user_requests_blurays",
                                                                                      BluRayRequest.objects.none())
    movies_requests = get_user_requests_movies(user,
                                               requests_filter=requests_filter).get("user_requests_movies",
                                                                                    MovieRequest.objects.none())
    people_requests = get_user_requests_people(user,
                                               requests_filter=requests_filter).get("user_requests_people",
                                                                                    PeopleRequest.objects.none())
    deals_requests = get_user_requests_deals(user,
                                             requests_filter=requests_filter).get("user_requests_deal",
                                                                                  DealRequest.objects.none())
    requests = list(chain(blurays_requests,
                          movies_requests,
                          people_requests,
                          deals_requests))
    return {"user_requests": requests,
            "filter": requests_filter}


def get_user_requests_total(user, requests_filter=["1"]):
    total = 0
    total += len(get_user_requests_blurays(user,
                                           requests_filter=requests_filter).get("user_requests_blurays",
                                                                                BluRayRequest.objects.none()))
    total += len(get_user_requests_movies(user,
                                          requests_filter=requests_filter).get("user_requests_movies",
                                                                               MovieRequest.objects.none()))
    total += len(get_user_requests_people(user,
                                          requests_filter=requests_filter).get("user_requests_people",
                                                                               PeopleRequest.objects.none()))
    total += len(get_user_requests_deals(user,
                                         requests_filter=requests_filter).get("user_requests_deals",
                                                                              DealRequest.objects.none()))
    return {"user_requests_total": total}
