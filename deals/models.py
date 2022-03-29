import re

from django.conf import settings
from django.db import models
from django.utils.timezone import now

from blurays.models import BluRay


CHOICES = [("1", "Actif"),
           ("2", "Expiré"),
           ("3", "Indéterminé")]


# Create your models here.
class Deal(models.Model):
    """
    A model that represents an actor or director.
    """
    blu_ray = models.ForeignKey(BluRay,
                                on_delete=models.CASCADE,
                                related_name='deal_blu_ray',
                                blank=True,
                                null=True)
    amazon_link = models.URLField(max_length=200,
                                  blank=False,
                                  null=False,
                                  verbose_name="Lien Amazon")
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                   on_delete=models.CASCADE,
                                   related_name='deal_user',
                                   blank=False, null=False)
    status = models.CharField(max_length=56,
                              choices=CHOICES,
                              default="3",
                              blank=True,
                              null=True)
    price = models.FloatField(blank=False,
                              null=False)
    start_date = models.DateField(default=now, blank=True, null=True)
    end_date = models.DateField(blank=True, null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Bon Plan"
        verbose_name_plural = "Bons Plans"

    def save(self, *args, **kwargs):
        if self.end_date:
            self.status = "2"
        if not self.blu_ray:
            print(self.amazon_link)
            amazon_asin = re.search(r"B0[.]*[^/]+", f"{self.amazon_link}")
            if amazon_asin:
                bluray = BluRay.objects.filter(amazon_asin=amazon_asin[0])
                if bluray:
                    self.blu_ray = bluray[0]
        return super(Deal, self).save(*args, **kwargs)
