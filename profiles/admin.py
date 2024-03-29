from django.contrib import admin
from .models import FavoriteUser, FavoriteMovie, FavoritePeople, FavoriteBluRay


# Register your models here.
@admin.register(FavoriteUser)
class FavoriteUserAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage FavoriteUser instances in the
    Admin interface.
    """
    list_per_page = 5


@admin.register(FavoriteMovie)
class FavoriteMovieAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage FavoriteUser instances in the
    Admin interface.
    """
    list_per_page = 5


@admin.register(FavoritePeople)
class FavoritePeopleAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage FavoriteUser instances in the
    Admin interface.
    """
    list_per_page = 5


@admin.register(FavoriteBluRay)
class FavoriteBluRayAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage FavoriteUser instances in the
    Admin interface.
    """
    list_per_page = 5
