from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from movies.models import Movie
from .models import BluRay


# Register your models here.
@admin.register(BluRay)
class BluRayAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage BluRay instances in the Admin
    interface.
    """
    list_per_page = 11
    list_display = ("id", "image_tag", "link_to_movie", "movie", "slug",
                    "title", "uhd", "vf", "forced_sub", "ean",
                    "link_to_amazon", "amazon_asin", "bluray_image",
                    "release_date")
    list_editable = ("movie", "title", "uhd", "vf", "forced_sub", "ean",
                     "amazon_asin", "bluray_image", "release_date")
    search_fields = ("movie", "ean", "amazon_asin")
    ordering = ("movie",)

    def link_to_movie(self, obj):
        if obj.movie:
            link = reverse("admin:movies_movie_change", args=[obj.movie.pk])
            return format_html('<a href="{}" target="_blank">{}</a>', link, obj.movie)
        else:
            return ""
    link_to_movie.short_description = 'Movie'

    def link_to_amazon(self, obj):
        if obj.amazon_aff_link:
            link = obj.amazon_aff_link
            return format_html('<a href="{}" target="_blank">{}</a>', link, obj.amazon_aff_link)
        return ""
    link_to_amazon.short_description = 'Amazon'
