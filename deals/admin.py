from django.contrib import admin

from .models import Deal


# Register your models here.
@admin.register(Deal)
class DealAdmin(admin.ModelAdmin):
    """
    A class inheriting from ModelAdmin to manage BluRay instances in the Admin
    interface.
    """
    list_per_page = 5
    list_display = ("id",
                    "bluray",
                    "amazon_aff_link",
                    "start_date",
                    "end_date",
                    "created_by",
                    "status",
                    "price")
    list_editable = ("bluray",
                     "amazon_aff_link",
                     "start_date",
                     "end_date",
                     "created_by",
                     "status",
                     "price")
    search_fields = ("bluray",
                     "start_date",
                     "end_date")
    ordering = ("bluray",)
