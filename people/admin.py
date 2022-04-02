from django.contrib import admin
from .models import People


# Register your models here.
@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_display = ("id", "image_tag", "first_name", "last_name", "slug", "birth_date",
                    "death_date", "imdb_id", "people_image")
    list_editable = ("first_name", "last_name", "birth_date", "death_date",
                     "imdb_id", "people_image")
    search_fields = ("first_name", "last_name")
    ordering = ("last_name", "first_name", )
