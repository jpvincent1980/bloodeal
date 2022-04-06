from PIL import Image
from django.conf import settings
from django.db import models
from django.db.models import Count, Q
from django.utils.safestring import mark_safe
from django.utils.text import slugify


# Create your models here.
class People(models.Model):
    """
    A model that represents an actor or director.
    """
    first_name = models.CharField(max_length=256,
                                  blank=True,
                                  null=True)
    last_name = models.CharField(max_length=256,
                                 blank=False,
                                 null=False)
    slug = models.SlugField(max_length=200,
                            unique=False,
                            blank=True)
    birth_date = models.DateField("Date de naissance",
                                  blank=True,
                                  null=True)
    death_date = models.DateField("Date de décès",
                                  blank=True,
                                  null=True)
    imdb_id = models.CharField(max_length=9,
                               blank=True,
                               null=True,
                               unique=True)
    people_image = models.ImageField(null=True,
                                     blank=True,
                                     upload_to="people/")
    requested_by = models.ForeignKey(settings.AUTH_USER_MODEL,
                                     on_delete=models.CASCADE,
                                     related_name='people_requested_by',
                                     blank=True,
                                     null=True)
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Personnalité"
        verbose_name_plural = "Personnalités"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        """
        if not self.slug and self.first_name and self.last_name:
            self.slug = slugify(f"{self.first_name} {self.last_name}")
        return super(People, self).save()

    def image_tag(self):
        if self.people_image != '':
            return mark_safe('<img src="%s%s" height="100px" />' % (f'{settings.MEDIA_URL}',
                                                                    self.people_image))


def get_people(user):
    people = People.objects.all()
    top_people = people.annotate(num_favorites=Count("favorite_people")).order_by("-num_favorites")[:5]
    favorite_people = people.filter(favorite_people__user=user)
    return {"movies": people,
            "top_people": top_people,
            "favorite_people": favorite_people,
            "latest_people": people.order_by("-date_created")}


def get_people_results(keyword):
    people_results = People.objects.filter(Q(first_name__icontains=keyword) | Q(last_name__icontains=keyword))
    return {"people_results": people_results}


def get_user_requested_people(user):
    people = People.objects.filter(requested_by=user)
    return {"user_requested_people": people}
