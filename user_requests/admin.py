from django.contrib import admin
from django.db.models import Q
from django.urls import reverse
from django.utils.html import format_html

from user_requests.models import PeopleRequest, MovieRequest, BluRayRequest, \
    DealRequest, PeopleRequestOpen, MovieRequestOpen, BluRayRequestOpen, \
    DealRequestOpen


# Register your models here.
@admin.register(PeopleRequest)
class PeopleRequestAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_per_page = 5
    list_display = ("id",
                    "user",
                    "link_to_people",
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(~Q(status="1"))

        return queryset

    def link_to_people(self, obj):
        if obj.people:
            link = reverse("admin:people_people_change", args=[obj.people.pk])
            return format_html('<a href="{}">{}</a>', link, obj.people)
        return ""
    link_to_people.short_description = 'People'


@admin.register(PeopleRequestOpen)
class PeopleRequestOpenAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_per_page = 5
    list_display = ("id",
                    "user",
                    "link_to_people",
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(status="1")

        return queryset

    def link_to_people(self, obj):
        if obj.people:
            link = reverse("admin:people_people_change", args=[obj.people.pk])
            return format_html('<a href="{}">{}</a>', link, obj.people)
        return ""
    link_to_people.short_description = 'People'


@admin.register(MovieRequest)
class MovieRequestAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_per_page = 5
    list_display = ("id",
                    "user",
                    "link_to_movie",
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(~Q(status="1"))

        return queryset

    def link_to_movie(self, obj):
        if obj.movie:
            link = reverse("admin:movies_movie_change", args=[obj.movie.pk])
            return format_html('<a href="{}">{}</a>', link, obj.movie)
        return ""
    link_to_movie.short_description = 'Movie'


@admin.register(MovieRequestOpen)
class MovieRequestOpenAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_per_page = 5
    list_display = ("id",
                    "user",
                    "link_to_movie",
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
    ordering = ("user",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(status="1")

        return queryset

    def link_to_movie(self, obj):
        if obj.movie:
            link = reverse("admin:movies_movie_change", args=[obj.movie.pk])
            return format_html('<a href="{}">{}</a>', link, obj.movie)
        return ""

    link_to_movie.short_description = 'Movie'


@admin.register(BluRayRequest)
class BluRayRequestAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_per_page = 5
    list_display = ("id",
                    "user",
                    "link_to_bluray",
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(~Q(status="1"))

        return queryset

    def link_to_bluray(self, obj):
        if obj.bluray:
            link = reverse("admin:blurays_bluray_change", args=[obj.bluray.pk])
            return format_html('<a href="{}">{}</a>', link, obj.bluray)
        return ""
    link_to_bluray.short_description = 'Blu-Ray'


@admin.register(BluRayRequestOpen)
class BluRayRequestOpenAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_per_page = 5
    list_display = ("id",
                    "user",
                    "link_to_bluray",
                    "amazon_link",
                    "asin",
                    "status")
    list_editable = ("user",
                     "amazon_link",
                     "status")
    search_fields = ("user__pseudo",
                     "asin",
                     "status")
    ordering = ("user",)

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(status="1")

        return queryset

    def link_to_bluray(self, obj):
        if obj.bluray:
            link = reverse("admin:blurays_bluray_change", args=[obj.bluray.pk])
            return format_html('<a href="{}">{}</a>', link, obj.bluray)
        return ""

    link_to_bluray.short_description = 'Blu-Ray'


@admin.register(DealRequest)
class DealRequestAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_per_page = 5
    list_display = ("id",
                    "link_to_deal",
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(~Q(status="1"))

        return queryset

    def link_to_deal(self, obj):
        if obj.deal:
            link = reverse("admin:deals_deal_change", args=[obj.deal.pk])
            return format_html('<a href="{}">{}</a>', link, obj.deal)
    link_to_deal.short_description = 'Deal'

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


@admin.register(DealRequestOpen)
class DealRequestOpenAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage People instances in the Admin
    interface.
    """
    list_per_page = 5
    list_display = ("id",
                    "link_to_deal",
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

    def get_queryset(self, request):
        queryset = super().get_queryset(request)
        queryset = queryset.filter(status="1")

        return queryset

    def link_to_deal(self, obj):
        if obj.deal:
            link = reverse("admin:deals_deal_change", args=[obj.deal.pk])
            return format_html('<a href="{}">{}</a>', link, obj.deal)
    link_to_deal.short_description = 'Deal'

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
