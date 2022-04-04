from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from user_requests.models import PeopleRequest, MovieRequest, BluRayRequest, \
    DealRequest


# Register your models here.
@admin.register(PeopleRequest)
class PeopleRequestAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_display = ("id",
                    "user",
                    "first_name",
                    "last_name",
                    "imdb_link",
                    "imdb_id",
                    "status")
    list_editable = ("user",
                     "first_name",
                     "last_name",
                     "imdb_link",
                     "status")
    search_fields = ("user__pseudo",
                     "first_name",
                     "last_name",
                     "imdb_id",
                     "status")
    ordering = ("user", )


@admin.register(MovieRequest)
class MovieRequestAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_display = ("id",
                    "user",
                    "title_vf",
                    "title_vo",
                    "release_year",
                    "imdb_link",
                    "imdb_id",
                    "status")
    list_editable = ("user",
                     "title_vf",
                     "title_vo",
                     "release_year",
                     "imdb_link",
                     "status")
    search_fields = ("user__pseudo",
                     "imdb_id",
                     "status")
    ordering = ("user", )


@admin.register(BluRayRequest)
class BluRayRequestAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_display = ("id",
                    "user",
                    "amazon_link",
                    "asin",
                    "status")
    list_editable = ("user",
                     "amazon_link",
                     "status")
    search_fields = ("user__pseudo",
                     "asin",
                     "status")
    ordering = ("user", )


@admin.register(DealRequest)
class DealRequestAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_display = ("id",
                    "link_to_user",
                    "link_to_bluray",
                    "bluray",
                    "link_to_amazon",
                    "asin",
                    "price",
                    "status")
    list_editable = ("bluray",
                     "price",
                     "status")
    search_fields = ("user__pseudo",
                     "asin",
                     "status")
    ordering = ("user", )

    def link_to_user(self, obj):
        link = reverse("admin:accounts_customuser_change", args=[obj.user.pk])
        return format_html('<a href="{}">{}</a>', link, obj.user)
    link_to_user.short_description = 'User'

    def link_to_bluray(self, obj):
        if obj.bluray:
            link = reverse("admin:blurays_bluray_change", args=[obj.bluray.pk])
            return format_html('<a href="{}">{}</a>', link, obj.bluray)
        return ""
    link_to_bluray.short_description = 'Blu-Ray'

    def link_to_amazon(self, obj):
        if obj.amazon_link:
            link = obj.amazon_link
            return format_html('<a href="{}">{}</a>', link, obj.amazon_link)
        return ""
    link_to_amazon.short_description = 'Amazon'
