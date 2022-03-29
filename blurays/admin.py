from django.contrib import admin
from .models import BluRay


# Register your models here.
@admin.register(BluRay)
class BluRayAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage BluRay instances in the Admin
    interface.
    """
    list_display = ("id", "movie", "slug", "ean", "amazon_aff_link", "amazon_asin", "blu_ray_image",
                    "release_date")
    list_editable = ("movie", "ean", "amazon_asin", "blu_ray_image",
                     "release_date")
    search_fields = ("movie", "ean", "amazon_asin")
    ordering = ("movie",)
