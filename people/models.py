from django.db import models


# Create your models here.
class People(models.Model):
    """
    A model that represents an actor or director.
    """
    first_name = models.CharField(max_length=256, blank=True, null=True)
    last_name = models.CharField(max_length=256, blank=False, null=False)
    birth_date = models.DateField("Date de naissance", blank=True, null=True)
    imdb_id = models.CharField(max_length=7, blank=True, null=True)
    people_image = models.ImageField(null=True, blank=True, upload_to="people/")
    date_created = models.DateTimeField(auto_now_add=True)
    date_updated = models.DateTimeField(auto_now=True)

    class Meta:
        verbose_name = "Personnalité"
        verbose_name_plural = "Personnalités"

    def __str__(self):
        return f"{self.first_name} {self.last_name}"
