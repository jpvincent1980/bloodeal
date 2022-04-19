from django.db.models.signals import post_save
from django.dispatch import receiver

from blurays.models import BluRay
from .models import Deal
from user_requests.models import DealRequestOpen


@receiver(post_save, sender=DealRequestOpen)
def create_deal(sender, instance, **kwargs):
    if instance.status == "2" and not instance.deal:
        if not instance.asin:
            amazon_aff_link = instance.amazon_link
        else:
            amazon_aff_link = f"https://www.amazon.fr/dp/{instance.asin}?m=A1X6FK5RDHNB96&tag=laureatis-21"
        bluray = BluRay.objects.filter(amazon_asin=instance.asin)
        bluray = bluray[0] if bluray else None
        requested_by = instance.user
        status = "1"
        price = instance.price
        deal = Deal.objects.create(bluray=bluray,
                                   amazon_aff_link=amazon_aff_link,
                                   requested_by=requested_by,
                                   status=status,
                                   price=price)
        instance.deal = deal
        instance.save()
