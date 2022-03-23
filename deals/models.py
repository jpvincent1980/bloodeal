from django.conf import settings
from django.db import models

from blurays.models import BluRay


CHOICES = [("1", "Actif"),
           ("2", "Expiré"),
           ("3", "Indéterminé")]


# Create your models here.
class Deal(models.Model):
    """
    A model that represents an actor or director.
    """
    blu_ray = models.ForeignKey(BluRay, on_delete=models.CASCADE,
                                related_name='deal_movie', blank=False, null=False)
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name='deal_user',
                                   blank=False, null=False)
    status = models.CharField(max_length=56, choices=CHOICES, blank=False,
                              null=False)
    price = models.FloatField(blank=False, null=False)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bon Plan"
        verbose_name_plural = "Bons Plans"
