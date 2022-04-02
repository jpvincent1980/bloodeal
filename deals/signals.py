from django.db.models.signals import post_save
from django.dispatch import receiver

from blurays.models import BluRay
from .models import Deal
from user_requests.models import DealRequest


@receiver(post_save, sender=DealRequest)
def create_deal(sender, instance, **kwargs):
    if instance.status == "2":
        if not instance.asin:
            amazon_aff_link = instance.amazon_link
        else:
            amazon_aff_link = f"https://www.amazon.fr/dp/{instance.asin}?m=A1X6FK5RDHNB96&tag=laureatis-21"
        bluray = BluRay.objects.filter(amazon_asin=instance.asin)
        bluray = bluray[0] if bluray else None
        created_by = instance.user
        status = "1"
        price = instance.price
        Deal.objects.create(bluray=bluray,
                            amazon_aff_link=amazon_aff_link,
                            created_by=created_by,
                            status=status,
                            price=price)
