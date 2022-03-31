import re

from django.conf import settings
from django.db import models
from django.utils.timezone import now

from blurays.models import BluRay
from profiles.models import get_user_all_favorites

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
            amazon_asin = re.search(r"B0[.]*[^/]+", f"{self.amazon_link}")
            if amazon_asin:
                bluray = BluRay.objects.filter(amazon_asin=amazon_asin[0])
                if bluray:
                    self.blu_ray = bluray[0]
        return super(Deal, self).save(*args, **kwargs)


def get_deals(bluray=None, movie=None, people=None):
    deals = Deal.objects.all()
    context = {"deals": deals,
               "best_deals": deals.order_by("price"),
               "latest_deals": deals.order_by("-date_created")}
    if bluray:
        bluray_deals = Deal.objects.filter(blu_ray=bluray)
        context.update({"bluray_deals": bluray_deals})
    if movie:
        movie_deals = Deal.objects.filter(blu_ray__movie=movie)
        context.update({"movie_deals":movie_deals})
    if people:
        people_actor_deals = Deal.objects.filter(blu_ray__movie__actor=people)
        people_director_deals = Deal.objects.filter(blu_ray__movie__director=people)
        people_deals = people_actor_deals | people_director_deals
        context.update({"people_deals": people_deals})
    return context


def get_user_favorites_deals(user):
    user_favorite_blurays = get_user_all_favorites(user)
    user_favorite_blurays = user_favorite_blurays.get("user_favorites")
    user_favorite_deals = Deal.objects.filter(blu_ray__in=user_favorite_blurays)
    return {"user_favorite_deals": user_favorite_deals}
