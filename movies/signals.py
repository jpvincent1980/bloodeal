from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Movie
from user_requests.models import MovieRequest


@receiver(post_save, sender=MovieRequest)
def create_deal(sender, instance, **kwargs):
    if instance.status == "2":
        imdb_id = instance.imdb_id
        if not Movie.objects.filter(imdb_id=imdb_id):
            Movie.objects.create(imdb_id=imdb_id)
