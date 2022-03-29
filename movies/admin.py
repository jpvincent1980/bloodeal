from django.contrib import admin
from .models import Movie, MovieActor, MovieDirector


# Register your models here.
@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage Movie instances in the Admin
    interface.
    """
    list_display = ("id", "title_vf", "title_vo", "slug", "release_year", "imdb_id",
                    "movie_image")
    list_editable = ("title_vf", "title_vo", "release_year", "imdb_id",
                     "movie_image")
    search_fields = ("title_vf", "title_vo")
    ordering = ("title_vf",)


@admin.register(MovieActor)
class MovieActorAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage Movie instances in the Admin
    interface.
    """
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
    list_display = ("id", "movie", "director")
    list_editable = ("movie", "director")
    search_fields = ("movie", "director")
    ordering = ("movie", "director")
