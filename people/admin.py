from django.contrib import admin
from django.utils.html import format_html

from .models import People


# Register your models here.
@admin.register(People)
class PeopleAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_per_page = 5
    list_display = ("id", "image_tag", "link_to_imdb", "first_name",
                    "last_name", "slug", "birth_date", "death_date",
                    "people_image")
    list_editable = ("first_name", "last_name", "birth_date",
                     "death_date", "people_image")
    search_fields = ("first_name", "last_name")
    ordering = ("last_name", "first_name", )

    def link_to_imdb(self, obj):
        if obj.imdb_id:
            link = "https://www.imdb.com/name/" + str(obj.imdb_id)
            return format_html('<a href="{}" target="_blank">{}</a>', link, obj.imdb_id)
        else:
            return ""

    link_to_imdb.short_description = 'IMDB'
