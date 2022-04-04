from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import Movie
from user_requests.models import MovieRequest


@receiver(post_save, sender=MovieRequest)
def create_deal(sender, instance, **kwargs):
    if instance.status == "2":
        imdb_id = instance.imdb_id
        requested_by = instance.user
        title_vf = instance.title_vf
        title_vo = instance.title_vo
        release_year = instance.release_year
        if not Movie.objects.filter(imdb_id=imdb_id):
            movie = Movie.objects.create(imdb_id=imdb_id,
                                         requested_by=requested_by,
                                         title_vf=title_vf,
                                         title_vo=title_vo,
                                         release_year=release_year)
            instance.movie = movie
            instance.save()
