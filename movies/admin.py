from django.contrib import admin
from django.utils.html import format_html

from .models import Movie, MovieActor, MovieDirector


# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage Movie instances in the Admin
    interface.
    """
    list_per_page = 5
    list_display = ("id", "image_tag", "link_to_imdb", "title_vf", "title_vo",
                    "slug", "release_year", "movie_image")
    list_editable = ("title_vf", "title_vo", "release_year", "movie_image")
    search_fields = ("title_vf", "title_vo")
    ordering = ("title_vf",)

    def link_to_imdb(self, obj):
        if obj.imdb_id:
            link = "https://www.imdb.com/title/" + str(obj.imdb_id)
            return format_html('<a href="{}" target="_blank">{}</a>', link, obj.imdb_id)
        else:
            return ""

    link_to_imdb.short_description = 'IMDB'


@admin.register(MovieActor)
class MovieActorAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage Movie instances in the Admin
    interface.
    """
    list_per_page = 5
    list_display = ("id", "movie", "actor")
    list_editable = ("movie", "actor")
    search_fields = ("movie", "actor")
    ordering = ("movie", "actor")


@admin.register(MovieDirector)
class MovieDirectorAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage Movie instances in the Admin
    interface.
    """
    list_per_page = 5
    list_display = ("id", "movie", "director")
    list_editable = ("movie", "director")
    search_fields = ("movie", "director")
    ordering = ("movie", "director")
