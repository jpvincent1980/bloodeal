from PIL import Image
from django.db import models
from django.db.models import CASCADE
from django.utils.text import slugify

from user_requests.models import PeopleRequest


# Create your models here.
class People(models.Model):
    """
    A model that represents an actor or director.
    """
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=False, null=False)
    slug = models.SlugField(max_length=200, unique=False, blank=True)
    birth_date = models.DateField("Date de naissance", blank=True, null=True)
    imdb_id = models.CharField(max_length=9, blank=True, null=True)
    people_image = models.ImageField(null=True,
                                     blank=True,
                                     upload_to="people/")
    request = models.ForeignKey(PeopleRequest,
                                on_delete=CASCADE,
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
        Overrides the save method to update image size at upload to limit width
        and height

        Args:
            force_insert: False
            force_update: False
            using: None
            update_fields: None

        Returns: Nothing

        """
        if not self.slug:
            self.slug = slugify(f"{self.first_name} {self.last_name}")
        if self.people_image:
            updated_image = Image.open(self.people_image)
            if updated_image.width > 100 or updated_image.height > 150:
                output_size = (100, 150)
                updated_image.thumbnail(output_size)
                updated_image.save(self.people_image)
        return super(People, self).save()
