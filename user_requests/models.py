from django.conf import settings
from django.db import models
import re

STATUS_CHOICES = [("1", "Créé"),
                  ("2", "Accepté"),
                  ("3", "Refusé"),
                  ("4", "Indéterminé")]


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
    imdb_id = models.CharField(max_length=7, blank=True, null=True)
    status = models.CharField(max_length=56,
                              choices=STATUS_CHOICES,
                              blank=False,
                              null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_imdb_id(self):
        imdb_id = re.search(r"/nm[0-9].[^/]+", str(self.imdb_link))[0][3:]
        return imdb_id

    class Meta:
        verbose_name = "Demande d'ajout - Personnalité"
        verbose_name_plural = "Demandes d'ajout - Personnalité"


class MovieRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='movie_user_request',
                             blank=False,
                             null=False)
    imdb_link = models.URLField(blank=False,
                                null=False,
                                verbose_name="Lien IMDB")
    imdb_id = models.CharField(max_length=7, blank=True, null=True)
    status = models.CharField(max_length=56,
                              choices=STATUS_CHOICES,
                              blank=False,
                              null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_imdb_id(self):
        imdb_id = re.search(r"/tt[0-9].[^/]+", str(self.imdb_link))[0][3:]
        return imdb_id

    class Meta:
        verbose_name = "Demande d'ajout - Film"
        verbose_name_plural = "Demandes d'ajout - Film"


class BluRayRequest(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE,
                             related_name='bluray_user_request',
                             blank=False,
                             null=False)
    amazon_link = models.URLField(blank=False,
                                  null=False,
                                  verbose_name="Lien Amazon")
    asin = models.CharField(max_length=7, blank=True, null=True)
    status = models.CharField(max_length=56,
                              choices=STATUS_CHOICES,
                              blank=False,
                              null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    def get_asin(self):
        imdb_id = re.search(r"B0[*].[^/]+", str(self.amazon_link))[0]
        return imdb_id

    class Meta:
        verbose_name = "Demande d'ajout - Blu-Ray"
        verbose_name_plural = "Demandes d'ajout - Blu-Ray"
