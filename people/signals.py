from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import People
from user_requests.models import PeopleRequest


@receiver(post_save, sender=PeopleRequest)
def create_deal(sender, instance, **kwargs):
    if instance.status == "2":
        imdb_id = instance.imdb_id
        requested_by = instance.user
        if not People.objects.filter(imdb_id=imdb_id):
            People.objects.create(imdb_id=imdb_id,
                                  requested_by=requested_by)
