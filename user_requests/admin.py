from django.contrib import admin

from user_requests.models import PeopleRequest, MovieRequest, BluRayRequest


# Register your models here.
@admin.register(PeopleRequest)
class PeopleRequestAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_display = ("id", "user", "imdb_link", "imdb_id", "status")
    list_editable = ("user", "imdb_link", "status")
    search_fields = ("user", "imdb_id", "status")
    ordering = ("user", )


@admin.register(MovieRequest)
class MovieRequestAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_display = ("id", "user", "imdb_link", "imdb_id", "status")
    list_editable = ("user", "imdb_link", "status")
    search_fields = ("user", "imdb_id", "status")
    ordering = ("user", )


@admin.register(BluRayRequest)
class BluRayRequestAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_display = ("id", "user", "amazon_link", "asin", "status")
    list_editable = ("user", "amazon_link", "status")
    search_fields = ("user", "asin", "status")
    ordering = ("user", )
