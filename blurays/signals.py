from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import BluRay
from user_requests.models import BluRayRequestOpen


@receiver(post_save, sender=BluRayRequestOpen)
def create_bluray(sender, instance, **kwargs):
    if instance.status == "2":
        if not instance.asin:
            amazon_link = instance.amazon_link
        else:
            amazon_link = f"https://www.amazon.fr/dp/{instance.asin}?m=A1X6FK5RDHNB96&tag=laureatis-21"
            amazon_asin = instance.asin
        requested_by = instance.user
        if not BluRay.objects.filter(amazon_asin=amazon_asin):
            bluray = BluRay.objects.create(amazon_asin=amazon_asin,
                                           amazon_aff_link=amazon_link,
                                           requested_by=requested_by)
            instance.bluray = bluray
            instance.save()
